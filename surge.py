import tokens
import match

class SurgeAbilityException(Exception):
	pass


TARGET_PLAYER = 'target player'
TARGET_SINGLE_TOKEN = 'target token'
TARGET_MULTIPLE_TOKENS = 'target tokens'
COUNTER_TOKEN = 'counter token'
COUNTER_MULTIPLE_TOKENS = 'counter tokens' 
target_ordering = [
	TARGET_PLAYER,
	TARGET_SINGLE_TOKEN,
	TARGET_MULTIPLE_TOKENS,
	COUNTER_TOKEN,
	COUNTER_MULTIPLE_TOKENS
]

class SurgeAbility:

	def __init__(self, name, param_headers=[TARGET_PLAYER], cost=1):
		self.name = name
		self.cost = cost
		self.used = False
		self.params = dict(zip(param_headers, [None] * len(param_headers)))
	

	def fill_parameter(self, param_header, value):
		self.params[param_header] = value


	def request_params(self):
		for param_name in target_ordering:
			if not param_name in self.params:
				continue
			while self.params[param_name] == None:

				yield param_name


	def cast(self, round_, caster):
		if self.used:
			raise SurgeAbilityException('Ability must be reset before recast.')
		if match.STATUS_SILENCED in round_.status_conditions[caster]:
			raise SurgeAbilityException('Caster is silenced')
		self.used = True
		self.effect(round_, caster)
	
	
	def reset(self):
		self.used = False
		for key in self.params:
			self.params[key] = None


class AbilityRelentless(SurgeAbility):

	# Undead Horde
	def __init__(self):
		super().__init__('Relentless', [TARGET_SINGLE_TOKEN])

	def effect(self, round_, caster):
		tkn = round_.tokens[caster]
		if tkn.active_side != tokens.SPENT:
			raise SurgeAbilityException('Target token is not spent.')
		tkn.recast(force=True)


class AbilitySwarm(SurgeAbility):

	# Undead Horde
	def __init__(self):
		super().__init__('Swarm', [])

	def effect(self, round_, caster):
		target = 1 + (caster % 2)
		round_.status_conditions[target].append(match.STATUS_SILENCED)


class AbilityRegenerate(SurgeAbility):

	def __init__(self, amount, cost):
		super().__init__('Regenerate', [], cost)
		self.amount = amount

	def effect(self, round_, caster):
		round_.heal_player(caster, self.amount)


class AbilityBreatheFire(SurgeAbility):

	# Dreadbringer 
	def __init__(self):
		super().__init__('Breathe Fire', [], cost=3)

	def effect(self, round_, caster):
		target = 1 + (caster % 2)
		round_.damage_player(target, 5, tokens.DMG_MAGIC)


class AbilityClaw(SurgeAbility):

	# Dreadbringer
	def __init__(self):
		super().__init__('Claw', [])
	
	def effect(self, round_, caster):
		target = 1 + (caster % 2)
		for tkn in round_.tokens[target]:
			if tkn.get_current_side() == Token.SHIELD:
				tkn.remove()


class MindMeld(SurgeAbility):

	# Master Thorn
	def __init__(self):
		super().__init__('Mind Meld', param_headers=[], cost=2)

	def effect(self, round_, caster):
		target = 1 + (caster % 2)
		def decorate_reflect(func):
			def damage_players_wrapper(round_, player, amount, dmg_type):
				func(round_, player, amount, dmg_type)
				round_.damage_player(target, amount, tokens.DMG_MAGIC)
		round_.damage_player = decorate_reflect(round_.damage_player)
