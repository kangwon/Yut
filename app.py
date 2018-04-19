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
        if value <= 0:
            node = player.node
            peers = list(p for p in node.players if p.owner == player.owner)
            peers.append(player)
            preys = list(p for p in node.players if p.owner != player.owner)
            for peer in peers:
                peer.accompany(peers)
            for prey in preys:
                prey.node = None
            node.players = list(p for p in node.players if p.owner == player.owner)
            return
            return
        # prev = player.node.index if player.node else 'None'
        if next_node:
            player.set_node(next_node)
        elif player.node:
            if player.node.is_last:
                player.was_goal = True
            else:
                player.set_node(player.node.get_next())
        else:
            player.set_node(self.map.head)
        # print(prev, '->', player.node.index)
        self.move(player, value - 1)

    def play(self):
        while True:
            self.turn += 1
            user = self.users[(self.turn-1) % len(self.users)]
            
            self.template.print_environ(self.map, self.users)

            Yut.throw()
            print(' '.join([str(s) for s in Yut.states]), Yut.display())
            
            while True:
                input_name = input(f'어떤 말을 움직이시겠습니까? {[p.name for p in user.players]}: ').strip()
                try:
                    selected_player = user.get_player(input_name)
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
                self.move(selected_player, Yut.value(), selected_node)
            else:
                self.move(selected_player, Yut.value())

            if user.is_win:
                print(f'Congratulation! {user.name}')
                break



class Template:

    template = """
    {14} . . . . {13} . . . . {12} . . . . {11} . . . . {10} . . . . {9}       Finished: {29}
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

    def print_environ(self, map, users):
        print(self.template.format(*map.nodes))
        for user in users:
            print(f'{user}: {", ".join([str(p) for p in user.players if p.node is None])}')


if __name__ == '__main__':
    template = Template()
    game = Game(template)
    game.play()