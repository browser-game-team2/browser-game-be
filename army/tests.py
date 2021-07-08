from django.test import TestCase
from .army_package.army import Army


# Create your tests here.
class ArmyTestCase(TestCase):
    def setUp(self):
        self.army = Army()
        self.attacker = Army()
        self.defender = Army()

    def test_army(self):
        self.assertIsInstance(self.army.space_ship, int)
        self.assertIn(self.army.strategy, [1, 2, 3])
        self.assertNotIn(self.army.strategy, [0, 4])

    def test_creation_input_like_fe(self):
        self.assertRaises(ValueError, Army.creation_input_like_fe, self.attacker, self.attacker)