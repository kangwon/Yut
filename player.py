class User:

    def __init__(self, user_name, player_names):
        self.name = user_name

        if len(set(player_names)) != 4:
            raise ValueError(f'player_names must be a list of 4 distinguishable strings: {player_names}')
        self.players = [Player(self, name) for name in player_names]

    def __str__(self):
        return self.name

    @property
    def is_win(self):
        return all([p.was_goal for p in self.players])

    def get_player(self, name):
        candidates = [p for p in self.players if p.name == name]
        if not candidates:
            raise ValueError(f'There is no such player: {name}')
        if len(candidates) != 1:
            raise Exception(f'Something is wrong: {candidates}, {self.players}')
        return candidates[0]


class Player:

    def __init__(self, owner, name):
        self.owner = owner
        self.name = name
        self.was_goal = False
        self.node = None

    def __str__(self):
        return self.name

    def set_node(self, node):
        if self.node:
            self.node.players.remove(self)
        node.players.append(self)
        self.node = node
