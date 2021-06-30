import random
from .request import Request


class BattleAlgo:

	@staticmethod
	# The function takes care of defining a json containing the attacker's parameters
	def define_attack(report):
		attacker = {}
		for key, value in report.items():
			if key == "attacker":
				attacker = value
		return attacker

	@staticmethod
	# The function takes care of defining a json containing the parameters of the defender
	def define_defender(report):
		defender = {}
		for key, value in report.items():
			if key == "defender":
				defender = value
		return defender

	@staticmethod
	def battle(attacker, defender):
		focus, adv = BattleAlgo.deploy(attacker['F'], defender['F'])  # see deploy()
		attacker_alive = True										  # attacking fleet has at least one ship
		defender_alive = True										  # defending fleet has at least one ship
		attacker_losses = 0											  # attacking fleet has taken no casualties
		defender_losses = 0											  # defending fleet has taken no casualties
		battle_report = {}  										  # set up the report dictionary

		# The following block runs the 0-th turn, where only 'focus' ships of the 'adv' side can attack.
		if adv == 'a':
			# successful rolls by attacker on the focus ship type
			attacker_hits = BattleAlgo.roll_to_hit(focus, attacker[focus])
			# defender takes casualties
			defender_alive, def_losses = BattleAlgo.remove_casualties(defender, attacker_hits)
		if adv == 'd':
			# successful rolls by defender on the focus ship type
			defender_hits = BattleAlgo.roll_to_hit(focus, defender[focus])
			# attacker takes casualties
			attacker_alive, att_losses = BattleAlgo.remove_casualties(attacker, defender_hits)
		if adv == 'n':
			# both players roll to hit on the focus ship type
			attacker_hits = BattleAlgo.roll_to_hit(focus, attacker[focus])
			defender_hits = BattleAlgo.roll_to_hit(focus, defender[focus])
			attacker_alive, att_losses = BattleAlgo.remove_casualties(attacker, defender_hits)  # and take casualties
			defender_alive, def_losses = BattleAlgo.remove_casualties(defender, attacker_hits)
		battle_report[0] = {'a': attacker_losses, 'd': defender_losses}			# register casualties in the report

		# The following block runs the main battle.
		# initialize round count
		count = 1
		# while both fleets still have at least one ship
		while attacker_alive and defender_alive:
			# initialize hit count at the beginning of each combat round
			attacker_hits = 0
			defender_hits = 0
			for ship_type in attacker.keys():
				attacker_hits += BattleAlgo.roll_to_hit(ship_type, attacker[ship_type])  # attacker's successful rolls
			for ship_type in defender.keys():
				defender_hits += BattleAlgo.roll_to_hit(ship_type, defender[ship_type])  # defender's successful rolls
			# attacker takes casualties
			attacker_alive, att_losses = BattleAlgo.remove_casualties(attacker, defender_hits)
			# defender takes casualties
			defender_alive, def_losses = BattleAlgo.remove_casualties(defender, attacker_hits)
			# register casualties in the report
			battle_report[count] = {'a': att_losses, 'd': def_losses}
			# Next combat round
			count += 1

		if attacker_alive:
			result = True, attacker, battle_report
		else:
			result = False, defender, battle_report  # defender wins if both fleets have 0 ships (very unlikely)
		return result

	# According to the battle formation chosen by each side, deploy() assigns focus to a ship type (B, C or D)
	# and benefits either attacker, defender or none of them.
	# This affects the special turn at the beginning of the battle.
	@staticmethod
	def deploy(attacker_f, defender_f):
		if (attacker_f == 1) and (defender_f == 1):
			return 'B', 'n'  							# battleships focus
		if (attacker_f == 1) and (defender_f == 2):
			return 'C', 'd'	 							# cruisers focus, defender's advantage
		if (attacker_f == 1) and (defender_f == 3):
			return 'B', 'a'  							# battleships focus, attacker's advantage
		if (attacker_f == 2) and (defender_f == 1):
			return 'C', 'a'  							# cruisers focus, attacker's advantage
		if (attacker_f == 2) and (defender_f == 2):
			return 'C', 'n'  							# cruisers focus
		if (attacker_f == 2) and (defender_f == 3):
			return 'D', 'd'  							# destroyers focus, defender's advantage
		if (attacker_f == 3) and (defender_f == 1):
			return 'B', 'd'  							# battleships focus, defender's advantage
		if (attacker_f == 3) and (defender_f == 2):
			return 'D', 'a'  							# destroyers focus, attacker's advantage
		if (attacker_f == 3) and (defender_f == 3):
			return 'D', 'n'  							# destroyers focus

	@staticmethod
	def roll_to_hit(ship, n):  # Gets a ship type (B, C or D) and the number of ships of that type
		hits = 0
		# each ship...
		for i in range(n):
			# ...rolls 2 six-sided dice and sums the results
			roll = random.randrange(1, 7) + random.randrange(1, 7)
			if ship == 'B':
				if roll >= 5:  						# battleships get a hit with a result of 5+
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
			elif fleet['B'] > 0:    					# if there are battleships in the fleet
				fleet['B'] -= 1							# remove 1
			else:										# if the fleet is empty
				return False, i							# mark it as defeated and report casualties
		if (fleet['B'] == 0) \
			and (fleet['C'] == 0) \
			and (fleet['D'] == 0):
			return False, n
		return True, n


# Main program
if __name__ == "__main__":
	inputFE = '{"attacker":{"type":"human",' \
				'"name":"player x",' \
				'"mail":"player@mail.com",' \
				'"army":{"B":5,"C":7,"D":1,"F":1},' \
				'"planet":"Venus"},' \
				'"defender":{"type":"virtual",' \
				'"name":"computer 1",' \
				'"army":{"B":4,"C":8,"D":9,"F":1},' \
				'"planet":"Mercury"}}'
	request = Request(inputFE)
	attacker_dict = BattleAlgo.define_attack(request.request)
	defender_dict = BattleAlgo.define_defender(request.request)
	print(BattleAlgo.battle(attacker_dict, defender_dict))
