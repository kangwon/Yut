from game import Game
from player import User
from interface import HumanInterface, RuleAIInterface


if __name__ == '__main__':
    human_interface = HumanInterface()
    ai_interface = RuleAIInterface()
    users = [
        User('A', ['q', 'w', 'e', 'r'], human_interface),
        User('B', ['a', 's', 'd', 'f'], ai_interface),
    ]
    game = Game(users)
    game.play()
