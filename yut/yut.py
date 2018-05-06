import random


class Yut:

    # 0: 납작한 면
    # 1: 둥근 면
    states = [0, 0, 0, 0]

    @classmethod
    def throw(cls):
        cls.states = [random.choice([0, 1]) for _ in range(4)]

    @classmethod
    def display(cls):
        if 4 - sum(cls.states) == 1:
            return '도'
        if 4 - sum(cls.states) == 2:
            return '개'
        if 4 - sum(cls.states) == 3:
            return '걸'
        if 4 - sum(cls.states) == 4:
            return '윷'
        if 4 - sum(cls.states) == 0:
            return '모'

    @classmethod
    def value(cls):
        if sum(cls.states) == 4:
            return 5
        return 4 - sum(cls.states)

    @classmethod
    def should_throw_one_more(cls):
        return sum(cls.states) == 0 or sum(cls.states) == 4
