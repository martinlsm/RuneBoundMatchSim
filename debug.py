from match import *
from player import *

p1 = Player(10, 10, [], [])
p2 = Player(11, 11, [], [])

p1.add_token(( ("damage", 1), ("shield", 2) ))
p1.add_token(( ("shield", 2), ("surge" , 1) ))
p1.add_token(( ("agility", 1), ("shield", 1) ))

p2.add_token(( ("surge", 1), ("shield", 2) ))
p2.add_token(( ("shield", 2), ("damage" , 1) ))
p2.add_token(( ("agility", 1), ("damage", 2) ))

m = Match(p1, p2)
r = Round(m)
