import random

import tokens


STATUS_SILENCED = 'silenced'


def validate_category(tokens, category):
	for tkn in tokens:
		if tkn.active_side in range(2) and tkn.get_current_side().token_type == category:
			continue
		return False
	return True


def select_by_category(list_of_tokens, indices, category):
	tkns_filtered = [list_of_tokens[i] for i in indices]
	if not validate_category(tkns_filtered, category):
		raise ValueError('At least one token is not of the right category "{}"'.format(category))
	return tkns_filtered


class Match:
	
	def __init__(self, player1, player2):
		self.players = {1:player1 , 2:player2}
	

	def resolve_direct_abilites(self):
		pass

	
	def resolve_flee_phase(self, p1_try_retreat, p2_try_retreat):
		pass
	
	
	def check_for_winner(self):
		"""
			0 : match ended as draw
			1 : player 1 won the match
			2 : player 2 won the match
		   -1 : match is not yet finished
		"""
		if self.players[1].current_hp <= 0 and self.players[2].current_hp <= 0:
		    return 0
		if self.players[2].current_hp <= 0:
		    return 1
		if self.players[1].current_hp <= 0:
		    return 2
		else:
		    return -1


class Round:

	def __init__(self, match):
		self.match = match
		def _setup_tokens(player):
			return [tokens.Token(*sides) for sides in player.token_sides]
		self.tokens = {1:_setup_tokens(match.players[1]), 2:_setup_tokens(match.players[2])}
		self.status_conditions = {1:[], 2:[]}


	def both_cast_tokens(self):
		def _cast_all(token_list):
			for tkn in token_list:
				tkn.cast()
		_cast_all(self.tokens[1])
		_cast_all(self.tokens[2])


	def damage_player(self, player_index, amount, dmg_type):
		self.players[player_index].reduce_hp(amount)

	
	def heal_player(self, player_index, amount):
		self.players[player_index].restore_hp(amount)


	def apply_status_condition(player, status):
		self.status_conditions[player] = status

	
	def agility_token(self, caster, target, spent_token_index, target_token_index):
		"""Attempts to resolve an agility symbol which flips or recasts a token.

		Args:
			caster (int): The index {1, 2} of the casting player.
			target (int): The index {1, 2} of the target player.
			spent_token_index (int): The index of the token to be used.
			target_token_index (int): The index of the token to be targeted.
		"""
		if not validate_category([self.tokens[caster][spent_token_index]], tokens.AGILITY):
			raise ValueError('The spent token is not from the right category.')
		if caster == target:
			if spent_token_index == target_token_index:
				raise ValueError('The agility token cannot target itself.')
			self.tokens[target][target_token_index].flip()
		else:
			self.tokens[target][target_token_index].cast(recast=True)
		self.tokens[caster][spent_token_index].spend()


	def damage_token(self, caster, spent_token_indices, dmg_category, target_block_indices=[], blockable=True):
		"""Attempts to resolve a number of damage tokens of the same type to damage the opposing player.

		Args:
			caster (int): The index {1, 2} of the casting player.
			spent_token_indices (list<int>): A list of the indices of the tokens to be used as damage source.
			dmg_category (str): The constant (in token module) to be used as the damage type.
			target_block_indices (list<int>): A list of the indices of the tokens to be used for blocking.
			blockable (bool): True if the attack is blockable, otherwise false.
		"""
		target = 1 + (caster % 2)
		dmg_tokens = select_by_category(self.tokens[caster], spent_token_indices, dmg_category)
		block_tokens = []
		if blockable:
			block_tokens = select_by_category(self.tokens[target], target_block_indices, tokens.SHIELD)
		self.damage_player(target, max(0, sum(dmg_tokens) - sum(block_tokens)), dmg_category)
		for tkn in dmg_tokens + block_tokens:
			tkn.spend()
	

	def double_token(self, caster, spent_token_index, target_token_index):
		if validate_category([self.tokens[caster][spent_token_index]], tokens.DOUBLE) \
	      and self.tokens[caster][target_token_index].active_side in range(2) \
		  and target_token_index != spent_token_index:
			self.tokens[caster][target_token_index].double()
			self.tokens[caster][spent_token_index].spend()

	
	def get_ability(self, caster, spent_token_indices, surge_index):
		pc = self.match.players[caster]
		ability = self.match.players[caster].surge_abilities[surge_index]
		tkns = select_by_category(self.tokens[caster], spent_token_indices, tokens.SURGE)
		if sum(tkns) >= ability.cost:
			return ability
