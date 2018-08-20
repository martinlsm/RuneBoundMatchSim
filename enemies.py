import player
import surge
import tokens


class Dreadbringer(player.Enemy):

    def __init__(self, act=1):
        super().__init__('Dreadbringer', 7, [],
               [surge.AbilityClaw(), surge.AbilityDirectHeal('Regenerate', amount=2, cost=2)
               ,surge.AbilityDirectDamage('Breathe Fire', amount=5, cost=3, damage_type=tokens.DMG_SKULL)], act
        )


class UndeadHorde(player.Enemy):

    def __init__(self, act=1):
        super().__init__('Undead Horde', 3, [], [surge.AbilityRelentless(), surge.AbilitySwarm()], act)


class DragonHybrid(player.Enemy):

    def __init__(self, act=1):
        super().__init__('Dragon Hybrid', 6, [],
            [surge.AbilityDirectDamage('Slice', amount=2, damage_type=tokens.DMG_SKULL, cost=3)
            ,surge.AbilityBarrier()]
        )


class BarrowWyrm(player.Enemy):

    def __init__(self, act=1):
        super().__init__('Barrow Wyrm', 8, [],
               [surge.AbilityBoneArmor()
               ,surge.AbilityDirectDamage('Brutal Strike', amount=2, damage_type=tokens.DMG_SKULL, cost=2)
               ,surge.AbilityDirectHeal('Undying', amount=4, cost=3)]
        )