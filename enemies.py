import player
import surge


class Dreadbringer(player.Enemy):

	def __init__(self, act=1):
		super().__init__('Dreadbringer', 7, [] \
		, [surge.AbilityClaw(), surge.AbilityRegenerate(amount=2, cost=2) \
		, surge.AbilityBreatheFire()], act)


class UndeadHorde(player.Enemy):


	def __init__(self, act=1):
		super().__init__('Undead Horde', 3, [], [surge.AbilityRelentless(), surge.AbilitySwarm()], act)
