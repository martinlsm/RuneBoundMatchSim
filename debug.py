from match import *
from player import *
from token import *

p1 = Player(10, 10, [], [])
p2 = Player(11, 11, [], [])

p1.add_token((TokenSide(DMG_PHYS, 1, True), TokenSide(SHIELD, 2, False) ))
p1.add_token(( TokenSide(SHIELD, 2, False), TokenSide(SURGE , 1, False) ))
p1.add_token(( TokenSide(AGILITY, 1, False), TokenSide(SHIELD, 1, True) ))

p2.add_token(( TokenSide(SURGE, 1, False), TokenSide(SHIELD, 2, True) ))
p2.add_token(( TokenSide(SHIELD, 2, False), TokenSide(DMG_SKULL , 1, False) ))
p2.add_token(( TokenSide(AGILITY, 1, True), TokenSide(DMG_PHYS, 2, False) ))

m = Match(p1, p2)
r = Round(m)
