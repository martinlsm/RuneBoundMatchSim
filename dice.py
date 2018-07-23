import random

WATER = 'water'
FOREST = 'forest'
MOUNTAIN = 'mountain'
HILLS = 'hills'
PLAINS = 'plains'

std_die = [ 
		    (PLAINS,), 
		    (PLAINS,),
			(PLAINS, FOREST),
			(MOUNTAIN, WATER),
			(WATER, FOREST, MOUNTAIN, HILLS, PLAINS), # Wild
			(FOREST, HILLS)
		  ]

def roll_dice(nbr):
	return [std_die[random.randint(0, 5)] for _ in range(nbr)] 


def explore(movespeed, terrain):
	print([x for x in roll_dice(movespeed) if terrain in x])
	return len([x for x in roll_dice(movespeed) if terrain in x])
