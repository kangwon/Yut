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
        return all([p.was_goaled for p in self.players])

    @property
    def staying_players(self):
        return [str(p) for p in self.players if not p.was_goaled and p.node is None]

    @property
    def movable_players(self):
        return [p for p in self.players if not p.was_goaled]

    @property
    def goaled_players(self):
        return [p for p in self.players if p.was_goaled]

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
        self.was_goaled = False
        self.node = None
        self.company = []
        self.traces = []    # Not include current node

    def __str__(self):
        return self.name

    def __hash__(self):
        return self.name.__hash__()

    def get_next_node(self):
        return self.node.get_next(self.traces)

    def set_node(self, node):
        if self.node:
            self.traces.append(self.node.index)
            self.node.players.remove(self)
        self.node = node
        if node:
            node.players.append(self)

    def move(self, next_node):
        # for debug
        # prev = self.node.index if self.node else 'None'
        if self.was_goaled:
            return
        # 골인 처리
        if self.node and self.node.is_last:
            self.was_goaled = True
            self.set_node(None)
        else:
            self.set_node(next_node)
        # for debug
        # print(prev, '->', self.node.index if self.node else 'None')

    def accompany(self, players):
        peers = list(players)
        while self in peers:
            peers.remove(self)
        self.company = peers
