import random
from collections import namedtuple

DMG_PHYS = 'physical damage'
DMG_MAGIC = 'magic damage'
DMG_SKULL= 'skull damage'
SURGE = 'surge'
AGILITY = 'agility'
DOUBLE = 'double'
SHIELD = 'shield'
BLANK = 'blank'

TokenSide = namedtuple('TokenSide', ['token_type', 'value', 'is_golden'])


enemy_token_sides = [ \
				(TokenSide(DMG_SKULL, 1, False), TokenSide(BLANK, 0, True)) \
			  , (TokenSide(SHIELD, 1, False), TokenSide(DMG_SKULL, 1, False)) \
			  , (TokenSide(AGILITY, 0, False), TokenSide(DMG_SKULL, 1, False)) \
			  , (TokenSide(DMG_SKULL, 1, True), TokenSide(SURGE, 1, False)) \
			  , (TokenSide(DOUBLE, 0, False), TokenSide(BLANK, 0, True)) \
			  , (TokenSide(DMG_SKULL, 2, False), TokenSide(SURGE, 1, True)) \
					]

def generate_enemy_tokens(act_number):
	return [Token(*sides) for sides in enemy_token_sides[0:act_number+4]]
		

class Token:

	SIDE0 = 0
	SIDE1 = 1
	UNCAST = -1
	SPENT = -2
	LOCKED = -3

	def __init__(self, side1, side2):
		self.sides = (side1, side2)
		self.active_side = Token.UNCAST
	
	
	def flip(self):
		if self.active_side not in range(2):
			raise ValueError('The token does not have an active side.')
		self.active_side = (1 + self.active_side) % 2
		return self.sides[self.active_side]
	

	def get_initiative(self):
		return int(self.sides[self.active_side].is_golden)


	def get_current_side(self):
		return self.sides[self.active_side]
	

	def cast(self):
		self.active_side = random.randint(0, 1)


	def spend(self):
		self.active_side = Token.SPENT

	
	def __add__(self, other):
		if self.active_side in range(0, 1):
			if type(other) == int:
				return tkn1.value + other
			tkn1 = self.sides[self.active_side]
			tkn2 = other.sides[other.active_side]
			if other.active_side not in range(0, 1):
				raise ValueError('Tokens must be cast before added.')
			if tkn1.token_type != tkn2.token_type:
				raise ValueError('Can not add token sides from different categories.')
			return tkn1.value + tkn2.value
		else:
			raise ValueError('Token must be cast before added.')


	def __radd__(self, other):
		return self.__add__(other)
