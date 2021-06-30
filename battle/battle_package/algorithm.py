import random
import json
from typing import Tuple
from battle.battle_package.request import Request


class BattleAlgo:

	@staticmethod
	#  The function takes care of defining a json containing the attacker's parameters
	def defineAttack(report):
		at = {}
		for key, value in report.items():
			if key == "at":
				at = value
		return at

	@staticmethod
	#The function takes care of defining a json containing the parameters of the defender
	def defineDefender(report):
		de = {}
		for key, value in report.items():
			if key == "de":
				de = value
		return de

	@staticmethod
	def battle(at = dict, de = dict):
		focus, adv = BattleAlgo.deploy(at['F'], de['F'])	# see deploy()
		attAlive = True		# attacking fleet has at least one ship
		defAlive = True		# defending fleet has at least one ship
		attLosses = 0		# attacking fleet has taken no casualties
		defLosses = 0		# defending fleet has taken no casualties
		battleReport = {}	# set up the report dictionary

		# The following block runs the 0-th turn, where only 'focus' ships of the 'adv' side can attack.
		if adv == 'a':
			attHits = BattleAlgo.rollToHit(focus, at[focus])					# successful rolls by attacker on the focus ship type
			defAlive, defLosses = BattleAlgo.removeCasualties(de, attHits)		# defender takes casualties
		if adv == 'd':
			defHits = BattleAlgo.rollToHit(focus, de[focus])					# successful rolls by defender on the focus ship type
			attAlive, attLosses = BattleAlgo.removeCasualties(at, defHits)		# attacker takes casualties
		if adv == 'n':
			attHits = BattleAlgo.rollToHit(focus, at[focus])					# both players roll to hit on the focus ship type
			defHits = BattleAlgo.rollToHit(focus, de[focus])
			attAlive, attLosses = BattleAlgo.removeCasualties(at, defHits)		# ...and take casualties
			defAlive, defLosses = BattleAlgo.removeCasualties(de, attHits)
		battleReport[0] = {'a': attLosses, 'd': defLosses}			# register casualties in the report

		# The following block runs the main battle.
		count = 1						# initialize round count
		while attAlive and defAlive:	# while both fleets still have at least one ship
			attHits = 0					# initialize hit count at the beginning of each combat round
			defHits = 0
			for shipType in at:
				attHits += BattleAlgo.rollToHit(shipType, at[shipType])		# attacker's successful rolls
			for shipType in de:
				defHits += BattleAlgo.rollToHit(shipType, de[shipType])		# defender's successful rolls
			attAlive, attLosses = BattleAlgo.removeCasualties(at, defHits) 	# attacker takes casualties
			defAlive, defLosses = BattleAlgo.removeCasualties(de, attHits)		# defender takes casualties
			battleReport[count] = {'a': attLosses, 'd': defLosses}	# register casualties in the report
			count += 1												# Next combat round

		if attAlive:
			result =  True, at, battleReport
		else:
			result = True, at, battleReport	# defender wins if both fleets have 0 ships (very unlikely)

		return result

	@staticmethod
	def deploy(atF = int, deF = int):										# According to the battle formation chosen by each side,
		if (atF == 1) and (deF == 1):										# deploy() assigns focus to a ship type (B, C or D)
			return ('B', 'n')	# battleships focus							# and benefits either attacker, defender or none of them.
		if (atF == 1) and (deF == 2):										# This affects the special turn at the beginning of the battle.
			return ('C', 'd')	# cruisers focus, defender's advantage
		if (atF == 1) and (deF == 3):
			return ('B', 'a')	# battleships focus, attacker's advantage
		if (atF == 2) and (deF == 1):
			return ('C', 'a')	# cruisers focus, attacker's advantage
		if (atF == 2) and (deF == 2):
			return ('C', 'n')	# cruisers focus
		if (atF == 2) and (deF == 3):
			return ('D', 'd')	# destroyers focus, defender's advantage
		if (atF == 3) and (deF == 1):
			return ('B', 'd')	# battleships focus, defender's advantage
		if (atF == 3) and (deF == 2):
			return ('D', 'a')	# destroyers focus, attacker's advantage
		if (atF == 3) and (deF == 3):
			return ('D', 'n')	# destroyers focus

	@staticmethod
	def rollToHit(ship = str, n = int):		# Gets a ship type (B, C or D) and the number of ships of that type
		hits = 0
		for i in range(n):		# each ship...
			roll = random.randrange(1, 7) + random.randrange(1, 7) 	# ...rolls 2 six-sided dice and sums the results
			if ship == 'B':
				if roll >= 5:	# battleships get a hit with a result of 5+
					hits += 1
			if ship == 'C':
				if roll >= 7:	# cruisers get a hit with a result of 7+
					hits += 1
			if ship == 'D':
				if roll >= 9:	# destroyers get a hit with a result of 9+
					hits += 1
		return hits

	@staticmethod
	def removeCasualties(fleet = dict, n = int):	# Removes n ships from a fleet
		for i in range(n):		# for each hit taken
			if fleet['D'] > 0:		# if there are destroyers in the fleet
				fleet['D'] -= 1			# remove 1
			elif fleet['C'] > 0:	# if there are cruisers in the fleet
				fleet['C'] -= 1			# remove 1
			elif fleet['B'] > 0:	# if there are battleships in the fleet
				fleet['B'] -= 1			# remove 1
			else:					# if the fleet is empty
				return False, i			# mark it as defeated and report casualties
		if (fleet['B'] == 0) and (fleet['C'] == 0) and (fleet['D'] == 0):
			return False, n
		return True, n


#test
if __name__ == "__main__":
	inputFE = '{"attacker":{"type":"human","name":"player x","mail":"player@mail.com","army":{"B":5,"C":7,"D":1,"F":1},\
		"planet":"Venus"},"defender":{"type":"virtual","name":"computer 1","army":{"B":4,"C":8,"D":9,"F":1},"planet":"Mercury"}}'
	request = Request.defineBattle(inputFE)
	at = BattleAlgo.defineAttack(request)
	de = BattleAlgo.defineDefender(request)
	print(BattleAlgo.battle(at, de))
