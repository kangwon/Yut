from player import Player
from map import Map
from yut import Yut


class GameEnvironment:

    def __init__(self, map_, users, Yut):
        self.map = map_
        self.users = users
        self.Yut = Yut


class Game:

    def __init__(self, users):
        self.map = Map()
        self.users = users
        self.turn = 0
        self.env = GameEnvironment(self.map, self.users, Yut)

    def move(self, player, value, next_node=None):
        for c in player.company:
            self.move_recur(c, Yut.value(), next_node)
        self.move_recur(player, Yut.value(), next_node)

        should_throw_one_more = False

        if player.node:
            self.handle_company(player)
            should_throw_one_more = self.handle_hunting(player)

        return should_throw_one_more

    def move_recur(self, player, value, next_node=None):
        # after move
        if value <= 0:
            return
        
        if next_node:
            player.move(next_node)
        elif player.node:
            player.move(player.get_next_node())
        else:
            player.move(self.map.head)
        
        self.move_recur(player, value - 1)

    # 업힘 처리
    def handle_company(self, player):
        peers = list(p for p in player.node.players if p.owner == player.owner)
        for peer in peers:
            peer.accompany(peers)

    # 잡아 먹힘 처리
    def handle_hunting(self, player):
        preys = list(p for p in player.node.players if p.owner != player.owner)
        for prey in preys:
            prey.accompany([])
            prey.node = None
        player.node.players = list(p for p in player.node.players if p.owner == player.owner)
        return bool(preys)

    def play(self):
        should_throw_one_more = False

        while True:
            if not should_throw_one_more:
                self.turn += 1
                user = self.users[(self.turn-1) % len(self.users)]
            
            should_throw_one_more = False

            Yut.throw()
            should_throw_one_more = Yut.should_throw_one_more() or should_throw_one_more

            selected_player = user.interface.select_player(self.env, user)

            if selected_player.node and len(selected_player.node.nexts) >= 2:
                selected_node = user.interface.select_node(self.env, selected_player)
                should_throw_one_more = self.move(selected_player, Yut.value(), selected_node) or should_throw_one_more
            else:
                should_throw_one_more = self.move(selected_player, Yut.value()) or should_throw_one_more

            if user.is_win:
                print(f'Congratulation! The winner is {user.name}')
                break