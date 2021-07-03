class Army:
    def __init__(self, spaceShip, spaceCruiser, spaceDestroyer, strategy):
        self.spaceShip = spaceShip
        self.spaceCruiser = spaceCruiser
        self.spaceDestroyer = spaceDestroyer
        self.strategy = strategy

    def __str__(self):
        return f'"S":{self.spaceShip}, "C":{self.spaceCruiser}, "D":{self.spaceDestroyer}, "F":{self.strategy}'
