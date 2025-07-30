HUMAN_IN_ROOM_MAP = [
    ['##', '##', '##', '##', '##', '##', '##'],
    ['##', 'vR', 'BK', '  ', '  ', '  ', '##'],
    ['##', '  ', '##', '##', '##', '##', '##'],
    ['##', '  ', 'BD', 'vH', '##', '  ', '##'],
    ['##', 'GG', '##', '##', '##', '  ', '##'],
    ['##', '  ', '  ', '  ', '  ', '  ', '##'],
    ['##', '##', '##', '##', '##', '##', '##']
]

MAP_METADATA = {
    "name": "Human in a 1x1 Room",
    "description": "A map where the human is trapped in a 1x1 room, and the robot must open the door. Optimized for training.",
    "size": (7, 7),
    "max_steps": 200,
    "human_goals": {"human_0": (4, 1)},
}

def get_map():
    """Return the map layout and metadata."""
    return HUMAN_IN_ROOM_MAP, MAP_METADATA