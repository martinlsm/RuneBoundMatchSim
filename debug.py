from match import *
from player import *
from tokens import *


def print_all_tokens(round_):
	for key in round_.tokens:
		print('Player {}:'.format(key))
		for i, tkn in enumerate(round_.tokens[key]):
			print('\tToken {}:'.format(i))
			print('\t\tside0: {}'.format(tkn.sides[0]))
			print('\t\tside1: {}'.format(tkn.sides[1]))
			print('\t\tActive side: {}'.format(tkn.active_side))

p1 = Player('Hero', 10)
p2 = Enemy('Enemy', 8, act=1)

p1.add_token((TokenSide(DMG_PHYS, 1, True), TokenSide(SHIELD, 2, False)))
p1.add_token(( TokenSide(SHIELD, 2, False), TokenSide(SURGE , 1, False)))
p1.add_token(( TokenSide(AGILITY, 1, False), TokenSide(SHIELD, 1, True)))

m = Match(p1, p2)
r = Round(m)
