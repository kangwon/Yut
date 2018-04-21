class Template:

    template = """
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

    def print_environ(self, map, users):
        print(self.template.format(*map.nodes))
        for user in users:
            print(f'{user}: [{", ".join([str(p) for p in user.staying_players])}] / [{", ".join([str(p) for p in user.goaled_players])}]')

    # for debug
    def print_companies(self, users):
        for u in users:
            for p in u.players:
                print(p, 'companies', p.company)


    def select_player(self, user):
        while True:
            input_name = input(f'어떤 말을 움직이시겠습니까? {[p.name for p in user.movable_players]}: ').strip()
            try:
                selected_player = user.get_player(input_name)
                if selected_player.was_goaled:
                    raise ValueError()
                break
            except ValueError:
                print(f'{input_name}은 유효하지 않은 입력입니다.')
        return selected_player

    def select_node(self, player):
        while True:
            print('어느 방향으로 움직이시겠습니까?')
            print('0: 돌아가는 방향')
            print('1: 빠른 방향')
            input_node = input('[0, 1]: ').strip()
            try:
                selected_node = player.node.nexts[int(input_node)]
                break
            except (IndexError, ValueError):
                print(f'{input_node}은 유효하지 않은 입력입니다.')
        return selected_node


"""
o . . . . o . . . . o . . . . o . . . . o . . . . o
. .                                             . .
.   .                                         .   .
.     .                                     .     .
.       o                                 o       .
o         .                             .         o
.           .                         .           .
.             .                     .             .
.               o                 o               .
.                 .             .                 .
o                   .         .                   o
.                     .     .                     .
.                       . .                       .
.                        o                        .
.                     .     .                     .
o                   .         .                   o
.                 .             .                 .
.               o                 o               .
.             .                     .             .
.           .                         .           .
o         .                             .         o
.       o                                 o       .
.     .                                     .     .
.   .                                         .   .
. .                                             . .
o . . . . o . . . . o . . . . o . . . . o . . . . o
"""