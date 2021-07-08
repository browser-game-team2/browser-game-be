import random


class Army:

    def __init__(self):
        self.space_ship = random.randint(1, 100)
        self.space_cruiser = random.randint(1, 100)
        self.space_destroyer = random.randint(1, 100)
        self.strategy = random.randint(1, 3)

    def __str__(self):
        return f'"S":{self.space_ship}, "C":{self.space_cruiser}, "D":{self.space_destroyer}, "F":{self.strategy}'

    # generate input like FE
    @staticmethod
    def creation_input_like_fe(army_attacker, army_defender):
        if not isinstance(army_attacker, Army) and not isinstance(army_defender, Army):
            raise ValueError("Object error")
        input_like_fe = '{"attacker":{"type":"human",' \
                        '"name":"player x",' \
                        '"mail":"player@mail.com",' \
                        '"army":{' + f'{army_attacker}' + '},' \
                        '"planet":"Venus"},' \
                        '"defender":{"type":"virtual",' \
                        '"name":"computer 1",' \
                        '"army":{' + f'{army_defender}' + '},' \
                        '"planet":"Mercury"}}'
        return input_like_fe


class SpaceShip:

    def __init__(self):
        self.price = 5


class SpaceCruiser:

    def __init__(self):
        self.price = 2


class SpaceDestroyer:

    def __init__(self):
        self.price = 1