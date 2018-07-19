import random


class Match:
	
	def __init__(self, player1, player2):
		self.player1 = player1
		self.player2 = player2
	
	
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
		if self.player1.current_hp <= 0 and self.player2.current_hp <= 0:
		    return 0
		if self.player2.current_hp <= 0:
		    return 1
		if self.player1.current_hp <= 0:
		    return 2
		else:
		    return -1


class Round:

	def __init__(self, match):
		self.match = match
		def _setup_tokens(player):
			tkns = []
			for (side_1, side_2) in player.tokens:
				tkns.append((side_1, side_2, -1))
			return tkns
		self.p1_tokens = _setup_tokens(match.player1)
		self.p2_tokens = _setup_tokens(match.player2)
	

	def both_cast_tokens(self):
		def _cast_all(token_list):
			for i, tkn in enumerate(self.p1_tokens):
				token_list[i] = (tkn[:2] , random.randint(1, 2))
		_cast_all(self.p1_tokens)
		_cast_all(self.p2_tokens)

