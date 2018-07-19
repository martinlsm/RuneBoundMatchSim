from collections import namedtuple

DMG_PHYS = 'physical damage'
DMG_MAGIC = 'magic damage'
DMG_SKULL= 'skull damage'
SURGE = 'surge'
AGILITY = 'agility'
DOUBLE = 'double'
SHIELD = 'shield'
BLANK = 'blank'

TokenSide = namedtuple('TokenSide', ['token_type', 'value', 'is_golden'])

