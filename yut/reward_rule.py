import copy
from itertools import chain

from player import Player


# Indices of nodes
"""
    {14} . . . . {13} . . . . {12} . . . . {11} . . . . {10} . . . . {9}
    . .                                             . .
    .   .                                         .   .
    .     .                                     .     .
    .       {26}                                 {22}       .
    {15}         .                             .         {8}
    .           .                         .           .
    .             .                     .             .
    .               {25}                 {23}               .
    .                 .             .                 .
    {16}                   .         .                   {7}
    .                     .     .                     .
    .                       . .                       .
    .                        {24}                        .
    .                     .     .                     .
    {17}                   .         .                   {6}
    .                 .             .                 .
    .               {27}                 {21}               .
    .             .                     .             .
    .           .                         .           .
    {18}         .                             .         {5}
    .       {28}                                 {20}       .
    .     .                                     .     .
    .   .                                         .   .
    . .                                             . .
    {19} . . . . {0} . . . . {1} . . . . {2} . . . . {3} . . . . {4}
"""


INDEX_REWARD_MAP = [
    1, 2, 3, 4, 9, 
    6, 7, 8, 9, 14,
    11, 12, 13, 14, 15,
    16, 17, 18, 19, 20,
    10, 11, 
    15, 16, 
    17,
    13, 14, 
    18, 19,
]


VALUE_PROBABILITY_MAP = {
    1: 4/16,
    2: 6/16,
    3: 4/16,
    4: 1/16,
    5: 1/16,
}


# class VirtualPlayer(Player):

#     def __enter__(self, player):
#         copied_player = copy.deepcopy(player)
#         self.owner = copied_player.owner
#         self.name = copied_player.name
#         self.was_goaled = copied_player.was_goaled
#         self.node = copied_player.node
#         self.company = copied_player.company
#         self.traces = copied_player.traces
#         return self

#     def __exit__(self):
#         if self.node:
#             self.node.players.remove(self)

#     def __hash__(self):
#         return self.name.__hash__()


def move_recur(head, player, value, next_node=None):
    # after move
    if value <= 0:
        return
    
    if next_node:
        player.move(next_node)
    elif player.node:
        player.move(player.get_next_node())
    else:
        player.move(head)
    
    move_recur(head, player, value - 1)


def move_virtually(head, player, value, next_node=None):
    virtual_player = copy.deepcopy(player)
    move_recur(head, virtual_player, value, next_node)
    return virtual_player


def get_position_reward(player):
    node = player.node

    # 자리 점수
    if node:
        position_reward = INDEX_REWARD_MAP[node.index]
        # reward for potential
        if node.index in (0, 1, 2, 3):
            position_reward += 0.2
        elif node.index in (4, 20, 21):
            position_reward += 0.3
        elif node.index in (5, 6, 7, 8):
            position_reward += 0.1
    else:
        position_reward = 21 if player.was_goaled else 0

    return position_reward


def get_hunting_reward(player):
    node = player.node

    # 잡아 먹음 점수
    if node:
        preys = list(p for p in node.players if p.owner != player.owner)
        hunting_reward = sum([get_position_reward(prey) for prey in preys] + [0])
        # 한 번 더 던지는 것에 대한 가산점
        if hunting_reward > 0:
            hunting_reward += 3
    else:
        hunting_reward = 0

    return hunting_reward


def get_hunted_expectation(env, player):
    # 잡아 먹힘 기댓값
    hunted_expectation = 0
    if player.node:
        other_users = [u for u in env.users if u != player.owner]
        other_players = chain.from_iterable([u.players for u in other_users])
        for p in other_players:
            available_nexts = p.node.nexts if p.node else [None]
            for value, prob in VALUE_PROBABILITY_MAP.items():
                for next_node in available_nexts:
                    virtual_player = move_virtually(env.map.head, p, value, next_node)
                    if player.node == virtual_player.node:
                        hunted_expectation += prob * get_position_reward(player)
                    if virtual_player.node:
                        virtual_player.node.players.remove(virtual_player)

    return hunted_expectation


def get_reward(env, player):
    position_reward = get_position_reward(player)
    hunting_reward = get_hunting_reward(player)
    hunted_expectation = get_hunted_expectation(env, player)
    return position_reward + hunting_reward - hunted_expectation


def get_max_reward_player(env, players):
    rewards = []
    
    current_rewards = {player: get_reward(env, player) for player in players}

    for player in players:
        tmp = []
        available_nexts = player.node.nexts if player.node else [None]
        for next_node in available_nexts:
            virtual_player = move_virtually(env.map.head, player, env.Yut.value(), next_node)
            expected_reward = get_reward(env, virtual_player)
            for p, r in current_rewards.items():
                if p.name == virtual_player.name:
                    continue
                # 업힘 점수
                elif virtual_player.node and virtual_player.node == p.node:
                    expected_reward += 21
                else:
                    expected_reward += r
            tmp.append(expected_reward)
            if virtual_player.node:
                virtual_player.node.players.remove(virtual_player)
        rewards.append(max(tmp))
    print(rewards)
    return players[rewards.index(max(rewards))]
