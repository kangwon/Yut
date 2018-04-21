from player import User, Player
from map import Map
from yut import Yut


class Game:

    def __init__(self, template):
        self.template = template
        self.map = Map()
        self.users = [
            User('A', ['q', 'w', 'e', 'r']),
            User('B', ['a', 's', 'd', 'f']),
        ]
        self.turn = 0

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
            
            self.template.print_environ(self.map, self.users)

            Yut.throw()
            should_throw_one_more = Yut.should_throw_one_more() or should_throw_one_more
            print(' '.join([str(s) for s in Yut.states]), Yut.display())
            
            while True:
                input_name = input(f'어떤 말을 움직이시겠습니까? {[p.name for p in user.movable_players]}: ').strip()
                try:
                    selected_player = user.get_player(input_name)
                    if selected_player.was_goaled:
                        raise ValueError()
                    break
                except ValueError:
                    print(f'{input_name}은 유효하지 않은 입력입니다.')

            if selected_player.node and len(selected_player.node.nexts) >= 2:
                while True:
                    print('어느 방향으로 움직이시겠습니까?')
                    print('0: 돌아가는 방향')
                    print('1: 빠른 방향')
                    input_node = input('[0, 1]: ').strip()
                    try:
                        selected_node = selected_player.node.nexts[int(input_node)]
                        break
                    except (IndexError, ValueError):
                        print(f'{input_node}은 유효하지 않은 입력입니다.')
                should_throw_one_more = self.move(selected_player, Yut.value(), selected_node) or should_throw_one_more
            else:
                should_throw_one_more = self.move(selected_player, Yut.value()) or should_throw_one_more

            if user.is_win:
                print(f'Congratulation! The winner is {user.name}')
                break