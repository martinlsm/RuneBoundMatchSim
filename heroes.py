import player
import surge

class MasterThorn(player.Hero):

	def __init__(self):
		super().__init__(
			name='Master Thorn',
			max_hp=8, 
			surge_abilities=[surge.MindMeld()],
			attributes=[0,3,2],
			hand_size=4,
			movespeed=3)

