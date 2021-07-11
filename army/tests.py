from django.test import TestCase
from .army_package.army import Army, SpaceShip, SpaceCruiser, SpaceDestroyer


# Create your tests here.
class ArmyTestCase(TestCase):
    def setUp(self):
        self.army = Army()
        self.attacker = Army()
        self.defender = Army()
        self.space_ship = SpaceShip()
        self.space_cruiser = SpaceCruiser()
        self.space_destroyer = SpaceDestroyer()

    def test_army(self):
        self.assertIsInstance(self.army.space_ship, int)
        self.assertIsInstance(self.army.space_cruiser, int)
        self.assertIsInstance(self.army.space_destroyer, int)
        self.assertIn(self.army.strategy, [1, 2, 3])

    def test_creation_input_like_fe(self):
        self.assertRaises(ValueError, Army.creation_input_like_fe, {}, {})
        self.assertIsInstance(self.army.creation_input_like_fe(self.attacker, self.defender), str)

    def test_space_price(self):
        self.assertIsInstance(self.space_ship.price, int)
        self.assertIsInstance(self.space_cruiser.price, int)
        self.assertIsInstance(self.space_destroyer.price, int)