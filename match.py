import random

import token


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
		if self.tokens[caster][spent_token_index].get_current_side().token_type != token.AGILITY:
			raise ValueError('The spent token is not from the right category.')
		if caster == target and spent_token_index == target_token_index:
				raise ValueError('The agility token cannot target itself.')
		self.tokens[target][target_token_index].flip()
		self.tokens[caster][spent_token_index].spend()


