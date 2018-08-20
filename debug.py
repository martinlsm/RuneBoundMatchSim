from match import *
from player import *
from tokens import *
from enemies import *
from heroes import *


def print_all_tokens(round_):
	for key in round_.tokens:
		print('Player {}:'.format(key))
		for i, tkn in enumerate(round_.tokens[key]):
			print('\tToken {}:'.format(i))
			print('\t\tside0: {}'.format(tkn.sides[0]))
			print('\t\tside1: {}'.format(tkn.sides[1]))
			print('\t\tActive side: {}'.format(tkn.active_side))

def debug_claw():
    p1 = Dreadbringer()
    p2 = UndeadHorde()

    m = Match(p1, p2)
    round_ = Round(m)

    round_.both_cast_tokens()

    while round_.tokens[1][3].active_side != 1 or round_.tokens[2][1].active_side != 0:
        round_.both_cast_tokens()

    ability = round_.get_ability(1, [3], 0)
    ability.cast(round_, 1)

    print_all_tokens(round_)


def debug_mind_meld():
    thorn = MasterThorn()
    thorn.add_token((TokenSide(SURGE, 2, False), TokenSide(SURGE, 2, False)))
    hybrid = DragonHybrid(act=2)

    m = Match(thorn, hybrid)
    round_ = Round(m)

    round_.both_cast_tokens()

    ability = round_.get_ability(1, [0], 0)
    ability.cast(round_, 1)
    print_all_tokens(round_)


    import pdb; pdb.set_trace()

if __name__ == '__main__':
    debug_mind_meld()
