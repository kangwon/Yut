import abc

import reward_rule


class YutInterFace:

    @abc.abstractmethod
    def select_player(self, env, user):
        pass

    @abc.abstractclassmethod
    def select_node(self, env, player):
        pass


class HumanInterface(YutInterFace):

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

    def print_environ(self, env):
        print(self.template.format(*env.map.nodes))
        for user in env.users:
            print(f'{user}: [{", ".join([str(p) for p in user.staying_players])}] / [{", ".join([str(p) for p in user.goaled_players])}]')
        print(' '.join([str(s) for s in env.Yut.states]), env.Yut.display())

    def print_expect(self, env, user):
        p = reward_rule.get_max_reward_player(env, user.movable_players)
        print('Expedted:', p)

    def select_player(self, env, user):
        while True:
            self.print_environ(env)
            # self.print_expect(env, user)
            input_name = input(f'어떤 말을 움직이시겠습니까? {[p.name for p in user.movable_players]}: ').strip()
            try:
                selected_player = user.get_player(input_name)
                if selected_player.was_goaled:
                    raise ValueError()
                break
            except ValueError:
                print(f'{input_name}은 유효하지 않은 입력입니다.')
        return selected_player

    def select_node(self, env, player):
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


class RuleAIInterface(YutInterFace):

    def select_player(self, env, user):
        print(' '.join([str(s) for s in env.Yut.states]), env.Yut.display())
        print(f'어떤 말을 움직이시겠습니까? {[p.name for p in user.movable_players]}: ')
        p = reward_rule.get_max_reward_player(env, user.movable_players)
        print('Choice:', p)
        return p

    def select_node(self, env, player):
        print('어느 방향으로 움직이시겠습니까?')
        print('0: 돌아가는 방향')
        print('1: 빠른 방향')
        print('Choice:', 1)
        return player.node.nexts[1]
