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
	"""
	Parent class of all surge abilities.
	This class covers all functionality needed for any token, except the tokens
	effect itself. The param_headers attribute is a list of all the data the
	ability needs to execute. After the ability is constructed, the
	request_params method should be called, which returns a generator of all
	parameters the ability needs. fill_parameters repeatedly until the ability
	has all parameters defined. The ability can then be cast properly.
	"""

	def __init__(self, name, param_headers=[TARGET_PLAYER], cost=1):
		"""
		This is the base constructor for all extending sub classes and
		should not be used directly.

		For param_headers parameter, look at the pre-defined alternatives above.

		Args:
			name (str): The name of the ability
			param_headers (list<str>): The parameters the token needs.
			cost (int): The number of surge symbols needed to cast the ability.
		"""
		self.name = name
		self.cost = cost
		self.used = False
		self.params = dict(zip(param_headers, [None] * len(param_headers)))
	

	def fill_parameter(self, param_header, value):
		"""
		Defines a parameter for the ability.
		Call request_params to examine what the ability needs for execution.
		
		Args:
			param_header (str): The parameter's name.
			value: TODO
		"""
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


class AbilityDirectDamage(SurgeAbility):

	def __init__(self, name, damage, cost):
		super().__init__(name, [], cost)
		self.damage = damage

	def effect(self, round_, caster):
		target = 1 + (caster % 2)
		round_.damage_player(target, self.damage, tokens.DMG_MAGIC)


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
			return damage_players_wrapper
		round_.damage_player = decorate_reflect(round_.damage_player)


class AbilityBarrier(SurgeAbility):

	# Dragon Hybrid
	def __init__(self):
		super().__init__('Barrier', param_headers=[], cost=2)

	def effect(self, round_, caster):
		target = 1 + (caster % 2)
		for tkn in round_.tokens[target]:
			if tkn.get_current_side() == tokens.Token.SIDE0 or tkn.get_current_side() == tokens.Token.SIDE1:
				tkn.remove()

