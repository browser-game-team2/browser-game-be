from django.test import TestCase
from .battle_package.algorithm import Battle
from .battle_package.request import Request


class BattleTestCase(TestCase):

    def setUp(self) -> None:
        self.inputFE = '{"attacker": {"type": "human", ' \
                               '"name": "player x", ' \
                               '"mail": "player@mail.com", ' \
                               '"army": {"S": 5, "C": 7, "D": 1, "F": 1}, ' \
                               '"planet": "Venus"}, ' \
                               '"defender": {"type": "virtual", ' \
                               '"name": "computer 1", ' \
                               '"army": {"S": 4, "C": 8, "D": 9, "F": 1}, ' \
                               '"planet": "Mercury"}}'
        self.request = Request(self.inputFE)
        self.battle = Battle(self.request)

    def test_battle_attacker(self):
        self.assertIsInstance(self.battle.attacker, dict)
        self.assertEqual(len(self.battle.attacker), 4)
        self.assertIn('S', self.battle.attacker.keys())
        self.assertIn('C', self.battle.attacker.keys())
        self.assertIn('D', self.battle.attacker.keys())
        self.assertIn('F', self.battle.attacker.keys())
        self.assertIsInstance(self.battle.attacker['S'], int)
        self.assertIsInstance(self.battle.attacker['C'], int)
        self.assertIsInstance(self.battle.attacker['D'], int)
        self.assertIsInstance(self.battle.attacker['F'], int)

    def test_battle_defender(self):
        self.assertIsInstance(self.battle.defender, dict)
        self.assertEqual(len(self.battle.defender), 4)
        self.assertIn('S', self.battle.defender.keys())
        self.assertIn('C', self.battle.defender.keys())
        self.assertIn('D', self.battle.defender.keys())
        self.assertIn('F', self.battle.defender.keys())
        self.assertIsInstance(self.battle.defender['S'], int)
        self.assertIsInstance(self.battle.defender['C'], int)
        self.assertIsInstance(self.battle.defender['D'], int)
        self.assertIsInstance(self.battle.defender['F'], int)

    def test_battle_winner(self):
        self.assertIsInstance(self.battle.winner, bool)
        self.assertIsInstance(self.battle.army_winner, dict)
        self.assertEqual(len(self.battle.army_winner), 4)
        self.assertIn('S', self.battle.army_winner.keys())
        self.assertIn('C', self.battle.army_winner.keys())
        self.assertIn('D', self.battle.army_winner.keys())
        self.assertIn('F', self.battle.army_winner.keys())
        self.assertIsInstance(self.battle.army_winner['S'], int)
        self.assertIsInstance(self.battle.army_winner['C'], int)
        self.assertIsInstance(self.battle.army_winner['D'], int)
        self.assertIsInstance(self.battle.army_winner['F'], int)

    def test_battle_special_round(self):
        self.assertIn(self.battle.focus, ['S', 'C', 'D'])
        self.assertIn(self.battle.advantage, ['a', 'd', 'n'])
        self.assertIsInstance(self.battle.special_round, dict)
        self.assertEqual(len(self.battle.special_round), 1)
        self.assertIn(0, self.battle.special_round.keys())
        self.assertIsInstance(self.battle.special_round[0], dict)
        self.assertIn('a', self.battle.special_round[0].keys())
        self.assertIn('d', self.battle.special_round[0].keys())
        self.assertIsInstance(self.battle.special_round[0]['a'], int)
        self.assertIsInstance(self.battle.special_round[0]['d'], int)

    def test_battle_main_battle(self):
        self.assertIsInstance(self.battle.main_battle, dict)
        self.assertGreaterEqual(len(self.battle.main_battle), 1)
        for i in range(len(self.battle.main_battle)):
            self.assertIsInstance(self.battle.main_battle[i+1], dict)
            self.assertIn('a', self.battle.main_battle[i+1].keys())
            self.assertIn('d', self.battle.main_battle[i+1].keys())
            self.assertIsInstance(self.battle.main_battle[i+1]['a'], int)
            self.assertIsInstance(self.battle.main_battle[i+1]['d'], int)
