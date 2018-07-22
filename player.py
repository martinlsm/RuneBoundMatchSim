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
