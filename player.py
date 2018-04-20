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
        return [str(p) for p in self.players if p.node is None]

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

    def __str__(self):
        return self.name

    def set_node(self, node):
        if self.node:
            self.node.players.remove(self)
        self.node = node
        if node:
            node.players.append(self)
        self.take_company(node)

    def move(self, next_node):
        # for debug
        prev = self.node.index if self.node else 'None'
        # 골인 처리
        if self.node.is_last:
            self.was_goaled = True
            self.set_node(None)
        else:
            self.set_node(next_node)
        # for debug
        print(prev, '->', self.node.index if self.node else 'None')

    # 동행을 데려가는 함수
    def take_company(self, node):
        for c in self.company:
            if c.node:
                c.node.players.remove(c)
            c.node = node
            if node:
                node.players.append(c)

    def accompany(self, players):
        peers = list(players)
        peers.remove(self)
        self.company = peers
