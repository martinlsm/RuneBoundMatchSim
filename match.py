import random

import token

def validate_category(tokens, category):
	print('tokens = {}'.format(tokens))
	print('category = {}'.format(category))
	for tkn in tokens:
		if tkn.active_side in range(0, 1) and tkn.get_current_side().token_type == category:
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
			return [token.Token(*sides) for sides in player.token_sides]
		self.tokens = {1:_setup_tokens(match.players[1]), 2:_setup_tokens(match.players[2])}


	def both_cast_tokens(self):
		def _cast_all(token_list):
			for tkn in token_list:
				tkn.cast()
		_cast_all(self.tokens[1])
		_cast_all(self.tokens[2])

	
	def agility_token(self, caster, target, spent_token_index, target_token_index):
		"""Attempts to resolve an agility symbol which flips or recasts a token.

		Args:
			caster (int): The index {1, 2} of the casting player.
			target (int): The index {1, 2} of the target player.
			spent_token_index (int): The index of the token to be used.
			target_token_index (int): The index of the token to be targeted.
		"""
		if not validate_category([self.tokens[caster][spent_token_index]], token.AGILITY):
			raise ValueError('The spent token is not from the right category.')
		if caster == target:
			if spent_token_index == target_token_index:
				raise ValueError('The agility token cannot target itself.')
			self.tokens[target][target_token_index].flip()
		else:
			self.tokens[target][target_token_index].cast()
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
			block_tokens = select_by_category(self.tokens[target], target_block_indices, token.SHIELD)
		self.match.players[target].reduce_hp(max(0, sum(dmg_tokens) - sum(block_tokens)))
		for tkn in dmg_tokens + block_tokens:
			tkn.spend()

