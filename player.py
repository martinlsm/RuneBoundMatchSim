import random

import token


class Player:

	def __init__(self, name, max_hp, setup_abilities=[], surge_abilities=[]):
		self.name = name
		self.max_hp = max_hp
		self.current_hp = max_hp
		self.setup_abilities = setup_abilities
		self.surge_abilities = surge_abilities
		self.token_sides = []
	

	def restore_hp(self, amount):
		self.current_hp = min(self.current_hp + amount, self.max_hp)

	
	def reduce_hp(self, amount):
		self.current_hp = max(0, self.current_hp - amount)


	def add_token(self, token_sides):
		"""Adds a combat token to the player's collection.
		Args:
			token (tuple<TokenSide>): A tuple with length 2 containing the two sides of the token.
		"""
		self.token_sides.append(token_sides)


class Enemy(Player):

	def __init__(self, name, max_hp, setup_abilities=[], surge_abilities=[], act=1):
		super().__init__(name, max_hp, setup_abilities, surge_abilities)
		for sides in token.enemy_token_sides[0:4+act]:
			super().add_token(sides)


class Hero(Player):

	BODY = 0
	MIND = 1
	SPIRIT = 2

	def __init__(self, name, max_hp, setup_abilities=[], surge_abilities=[], attributes=[0,0,0], hand_size=0):
		super().__init__(name, max_hp, setup_abilities, surge_abilities)
		self.attributes = attributes
		self.hand_size = hand_size


	def attribute_test(self, stat_index):
		return random.random() > 0.6**self.attributes[stat_index]
	
	
	def exert(self):
		if self.hand_size > 0:
			self.hand_size -= 1
			return True
		else:
			return False

