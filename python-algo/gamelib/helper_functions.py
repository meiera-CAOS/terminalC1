import itertools
from .game_state import is_stationary


def get_structures(game_state):
    """
    This goes through the current game_map and returns the structures that are currently on the game map
    :param game_state: Current GameState object
    :return:           Returns a dict where key is the player id and values their current structures on the game map
    """
    game_map = game_state.game_map._GameMap__map  # list of list, cf. game_map __empty_grid function
    # 0 = us
    # 1 = adversary
    structures = {0: [], 1: []}
    for x, x_item in enumerate(game_map):
        for y, unit in enumerate(x_item):
            if unit and is_stationary(unit[0].unit_type):
                # y_item is a structure
                if unit[0].player_index == 0:
                    structures[0].append(unit[0])
                else:
                    structures[1].append(unit[0])

    return structures


def get_mobile_units(game_state):
    """
    This goes through the current game_map and returns the mobile units that are currently on the game map
    :param game_state: Current GameState object
    :return:           Returns a dict where key is the player id and values their current structures on the game map
    """
    game_map = game_state.game_map._GameMap__map  # list of list, cf. game_map __empty_grid function
    # 0 = us
    # 1 = adversary
    mobile_units = {0: [], 1: []}
    for x, x_item in enumerate(game_map):
        for y, units in enumerate(x_item):
            if units and not is_stationary(units[0].unit_type):
                # y_item is a mobile unit or list of mobile units
                for unit in units:
                    if unit.player_index == 0:
                        mobile_units[0].append(unit)
                    else:
                        mobile_units[1].append(unit)

    return mobile_units


def get_score(game_state, player_id=0, weights=None):
    """
    Computes score of player_id
    :param game_state: Current game state
    :param player_id:  Player ID who's score we want to compute (defaults to player 0)
    :param weights:    Weight of the score components (defaults to weighting hp double)
    :return:           Returns a score that is a linear combination of health points (hp),
                       structure points (sp), mobile points (mp), and structure_score based
                       on what structure, incl. their health, is currently on the game map
    """
    if not weights:
        alpha = 2.0
        beta = 1.0
        gamma = 1.0
        delta = 1.0
    else:
        alpha, beta, gamma, delta = weights

    structures = get_structures(game_state)
    if player_id == 0:
        player0_structures = structures[0] # this is a list containing player0's current structures
    else:
        player0_structures = structures[1]
    structure_score = 0
    for structure_unit in player0_structures:
        structure_score += structure_unit.health / structure_unit.max_health * structure_unit.cost[SP]

    hp = game_state.my_health if player_id == 0 else game_state.enemy_health
    sp, mp = game_state.get_resources(player_index=player_id)

    # TODO: - do we want to ceiling to the structure_score to ensure it doesn't focus only on structure building
    score = alpha * hp + beta * sp + gamma * mp + delta * structure_score
    return score


def combination_generator(self, game_state):
    # Assume we want to use up all available MP and SP
    # TODO: - create all possible structure combination based on current game state
    #       ---- compute all valid coordinations
    #       ---- make it a constant that gets only computed once
    #       ---- y < game_map.HALF_ARENA and startx <= x <= endx
    #       - create all possible combination of starting points for the mobile units
    #       ---- use game_map.get_edge_locations(quadrant_description=game_map.BOTTOM_LEFT)
    #       ---- use game_map.get_edge_locations(quadrant_description=game_map.BOTTOM_RIGHT)
    #       ---- make it a constant that gets only computed once
    all_structures = self.get_structures(game_state)
    structures = all_structures[self.PLAYER0]
    # Assumptions: - restrict supports to Y < 8
    coordinates_raw = list(itertools.product(range(game_state.HALF_ARENA), range(game_state.ARENA_SIZE)))
    return