from player import User, Player
from map import Map
from yut import Yut


def print_environ(map_, users):
    print(map_)
    for user in users:
        print(f'{user}: {", ".join([str(p) for p in user.players if p.node is None])}')


def move(map_, player, value, next_node=None):
    if value <= 0:
        return
    # prev = player.node.index if player.node else 'None'
    if next_node:
        player.set_node(next_node)
    elif player.node:
        player.set_node(player.node.get_next())
    else:
        player.set_node(map_.head)
    # print(prev, '->', player.node.index)
    move(map_, player, value - 1)


if __name__ == '__main__':
    map_ = Map()

    users = [
        User('A', ['q', 'w', 'e', 'r']),
        User('B', ['a', 's', 'd', 'f']),
    ]

    turn = 0

    while True:
        turn += 1
        user = users[(turn-1) % len(users)]
        
        print_environ(map_, users)

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
            move(map_, selected_player, Yut.value(), selected_node)
        else:
            move(map_, selected_player, Yut.value())

        if user.is_win:
            print(f'Congratulation! {user.name}')
            break
