import random
from .request import Request


class Battle:

	def __init__(self, request):
		self.attacker = request.challengers_armies['attacker']  # parameters of the attacker
		self.defender = request.challengers_armies['defender']  # parameters of the defender
		self.focus, self.advantage = self.deploy()
		self.special_round = self.play_special_round()
		self.winner = None  # True or False
		self.army_winner = None	 # example: {"S": 2, "C": 0, "D": 0, "F": 2}
		self.main_battle = self.play_main_battle()
		self.final_report = self.generate_final_report()

	# According to the battle formation chosen by each side, deploy() assigns focus to a ship type (B, C or D)
	# and benefits either attacker, defender or none of them.
	# This affects the special turn at the beginning of the battle.
	def deploy(self):
		combinations_focus_advantage = {
			'11': ('S', 'n'),  # spaceships focus
			'12': ('C', 'd'),  # cruisers focus, defender's advantage
			'13': ('S', 'a'),  # spaceships focus, attacker's advantage
			'21': ('C', 'a'),  # cruisers focus, attacker's advantage
			'22': ('C', 'n'),  # cruisers focus
			'23': ('D', 'd'),  # destroyers focus, defender's advantage
			'31': ('S', 'd'),  # spaceships focus, defender's advantage
			'32': ('D', 'a'),  # destroyers focus, attacker's advantage
			'33': ('D', 'n'),  # destroyers focus
		}
		return combinations_focus_advantage[str(self.attacker['F']) + str(self.defender['F'])]

	def play_special_round(self):
		attacker_losses = 0  # attacking fleet has taken no casualties
		defender_losses = 0  # defending fleet has taken no casualties
		# The following block runs the 0-th turn, where only 'focus' ships of the 'advantage' side can attack.
		if self.advantage == 'a':
			# successful rolls by attacker on the focus ship type
			attacker_hits = Battle.roll_to_hit(self.focus, self.attacker[self.focus])
			# defender takes casualties
			defender_alive, defender_losses = Battle.remove_casualties(self.defender, attacker_hits)
		elif self.advantage == 'd':
			# successful rolls by defender on the focus ship type
			defender_hits = Battle.roll_to_hit(self.focus, self.defender[self.focus])
			# attacker takes casualties
			attacker_alive, attacker_losses = Battle.remove_casualties(self.attacker, defender_hits)
		elif self.advantage == 'n':
			# both players roll to hit on the focus ship type
			attacker_hits = Battle.roll_to_hit(self.focus, self.attacker[self.focus])
			defender_hits = Battle.roll_to_hit(self.focus, self.defender[self.focus])
			# and take casualties
			attacker_alive, attacker_losses = Battle.remove_casualties(self.attacker, defender_hits)
			defender_alive, defender_losses = Battle.remove_casualties(self.defender, attacker_hits)
		special_round_report = {0: {'a': attacker_losses, 'd': defender_losses}}  # register casualties in the report
		return special_round_report

	def play_main_battle(self):
		# The following block runs the main battle.
		main_battle_report = {}
		attacker_alive = True  # attacking fleet has at least one ship
		defender_alive = True  # defending fleet has at least one ship
		# initialize round count
		count = 1
		# while both fleets still have at least one ship
		while attacker_alive and defender_alive:
			# initialize hit count at the beginning of each combat round
			attacker_hits = 0
			defender_hits = 0
			for ship_type in self.attacker.keys():
				attacker_hits += Battle.roll_to_hit(ship_type, self.attacker[ship_type])  # attacker's successful rolls
			for ship_type in self.defender.keys():
				defender_hits += Battle.roll_to_hit(ship_type, self.defender[ship_type])  # defender's successful rolls
			# attacker takes casualties
			attacker_alive, attacker_losses = Battle.remove_casualties(self.attacker, defender_hits)
			# defender takes casualties
			defender_alive, defender_losses = Battle.remove_casualties(self.defender, attacker_hits)
			# register casualties in the report
			main_battle_report[count] = {'a': attacker_losses, 'd': defender_losses}
			# Next combat round
			count += 1
		if attacker_alive:
			self.winner = True
			self.army_winner = self.attacker
		else:
			self.winner = False
			self.army_winner = self.defender
		return main_battle_report

	def generate_final_report(self):
		return {
			'winner': self.winner,
			'army': self.army_winner,
			'report': {**self.special_round, **self.main_battle}
		}

	@staticmethod
	def roll_to_hit(ship, n):  # Gets a ship type (S, C or D) and the number of ships of that type
		hits = 0
		# each ship...
		for i in range(n):
			# ...rolls 2 six-sided dice and sums the results
			roll = random.randrange(1, 7) + random.randrange(1, 7)
			if ship == 'S':
				if roll >= 5:  						# spaceships get a hit with a result of 5+
					hits += 1
			if ship == 'C':
				if roll >= 7:  						# cruisers get a hit with a result of 7+
					hits += 1
			if ship == 'D':
				if roll >= 9:  						# destroyers get a hit with a result of 9+
					hits += 1
		return hits

	# Removes n ships from a fleet
	@staticmethod
	def remove_casualties(fleet, n):
		for i in range(n):								# for each hit taken
			if fleet['D'] > 0:							# if there are destroyers in the fleet
				fleet['D'] -= 1							# remove 1
			elif fleet['C'] > 0:    					# if there are cruisers in the fleet
				fleet['C'] -= 1							# remove 1
			elif fleet['S'] > 0:    					# if there are spaceships in the fleet
				fleet['S'] -= 1							# remove 1
			else:										# if the fleet is empty
				return False, i							# mark it as defeated and report casualties
		if (fleet['S'] == 0) \
			and (fleet['C'] == 0) \
			and (fleet['D'] == 0):
			return False, n
		return True, n


# Main program
if __name__ == "__main__":
	inputFE = '{"attacker":{"type":"human",' \
				'"name":"player x",' \
				'"mail":"player@mail.com",' \
				'"army":{"S":5,"C":7,"D":1,"F":1},' \
				'"planet":"Venus"},' \
				'"defender":{"type":"virtual",' \
				'"name":"computer 1",' \
				'"army":{"S":4,"C":8,"D":9,"F":1},' \
				'"planet":"Mercury"}}'

	request_obj = Request(inputFE)
	current_battle = Battle(request_obj)
	attacker_dict = current_battle.attacker
	defender_dict = current_battle.defender
	print(current_battle.final_report)
