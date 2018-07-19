

class Player:

	def __init__(self, max_hp, current_hp, setup_abilities, surge_abilities):
		self.max_hp = max_hp
		self.current_hp = current_hp
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

