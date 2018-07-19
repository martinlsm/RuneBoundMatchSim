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

class Token:

	def __init__(self, side1, side2):
		self.sides = (side1, side2)
		self.active_side = -1
	
	
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
		self.active_side = -1

	
	def __add__(self, other):
		if self.active_side == -1 or other.active_side == -1:
			raise ValueError('Tokens must be cast before added.')
		tkn1 = self.sides[self.active_side]
		if type(other) == int:
			return tkn1.value + other
		tkn2 = other.sides[other.active_side]
		if tkn1.token_type != tkn2.token_type:
			raise ValueError('Can not add token sides from different categories.')
		return tkn1.value + tkn2.value


	def __radd__(self, other):
		return self.__add__(other)
