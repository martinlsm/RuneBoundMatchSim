from surge import *

class DummyAbility(SurgeAbility):

	def __init__(self, param_headers=[TARGET_PLAYER, COUNTER_TOKEN]):
		super().__init__('Dummy Ability', param_headers)

	
	def effect(self, round_, caster):
		print('Casting Dummy ability on {}, which counters with the token {}' \
				.format(self.params[TARGET_PLAYER], self.params[COUNTER_TOKEN]))

if __name__ == '__main__':
	dummy = DummyAbility()
