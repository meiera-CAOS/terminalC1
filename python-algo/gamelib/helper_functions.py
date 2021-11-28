import itertools
from copy import deepcopy

from .game_state import is_stationary
import random
import numpy as np
import math


'''
def get_attacking_units(game_state):
    """
    This goes through the current game_map and returns the structures that are currently on the game map
    :param game_state: Current GameState object
    :return:           Returns a dict where key is the player id and values their current attack units on the game map
    """
    game_map = game_state.game_map._GameMap__map  # list of list, cf. game_map __empty_grid function
    # 0 = us
    # 1 = adversary
    attack_units = {0: [], 1: []}
    for x, x_item in enumerate(game_map):
        for y, units in enumerate(x_item):
            if units:
                for unit in units:    
                    if unit: # todo: check unit turret or mobile
                        if unit[0].player_index == 0:
                            attack_units[0].append(unit)
                        else:
                            attack_units[1].append(unit)
    return attack_units
'''


def round_half_up(n, decimals=0):
    multiplier = 10 ** decimals
    return math.floor(n*multiplier + 0.5) / multiplier


def get_all_units(game_state, both_players=False):
    """
    This goes through the current game_map and returns the structures that are currently on the game map
    :param game_state: Current GameState object
    :return:           Returns a dict where key is the player id and values their current structures on the game map
    """
    game_map = game_state.game_map._GameMap__map  # list of list, cf. game_map __empty_grid function
    # 0 = us
    # 1 = adversary
    if not both_players:
        all_units = {0: [], 1: []}
    else:
        all_units = []
    for x, x_item in enumerate(game_map):
        for y, units in enumerate(x_item):
            if units:
                for unit in units:
                    if not both_players:
                        if unit.player_index == 0:
                            all_units[0].append(unit)
                        else:
                            all_units[1].append(unit)
                    else:
                        all_units.append(unit)
    return all_units


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


def get_current_structures(game_state):
    all_structures = get_structures(game_state)
    my_structures = all_structures[0]
    walls = []
    turrets = []
    supports = []
    for structure in my_structures:
        if structure.unit_type == 'FF':
            walls.append(structure)
        elif structure.unit_type == 'DF':
            turrets.append(structure)
        else:
            supports.append(structure)
    return walls, turrets, supports


def get_mobile_units(game_state, both_players=False):
    """
    This goes through the current gamget_mobile_unitse_map and returns the mobile units that are currently on the game map
    :param
        game_state: Current GameState object
        both_players: Boolean, if True return a list of all mobile units, if false return a dict with player_id as keys
    :return:           Returns a dict where key is the player id and values their current structures on the game map
    """
    game_map = game_state.game_map._GameMap__map  # list of list, cf. game_map __empty_grid function
    # 0 = us
    # 1 = adversary
    if not both_players:
        mobile_units = {0: [], 1: []}
    else:
        mobile_units = []
    for x, x_item in enumerate(game_map):
        for y, units in enumerate(x_item):
            if units and not is_stationary(units[0].unit_type):
                # y_item is a mobile unit or list of mobile units
                for unit in units:
                    if not both_players:
                        if unit.player_index == 0:
                            mobile_units[0].append(unit)
                        else:
                            mobile_units[1].append(unit)
                    else:
                        mobile_units.append(unit)
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
        # TODO: - pass SP into this get_score function
        # SP = 0
        structure_score += structure_unit.health / structure_unit.max_health * structure_unit.cost[0]

    hp = game_state.my_health if player_id == 0 else game_state.enemy_health
    sp, mp = game_state.get_resources(player_index=player_id)

    # TODO: - do we want to ceiling to the structure_score to ensure it doesn't focus only on structure building
    score = alpha * hp + beta * sp + gamma * mp + delta * structure_score
    return score


def get_all_coordinates(game_state):
    # game_map = game_state.game_map._GameMap__map
    game_map = game_state.game_map

    left_border0 = lambda _y: -_y + 13
    right_border0 = lambda _y: _y + 14
    my_coordinates = []
    for x, y in itertools.product(range(game_map.ARENA_SIZE), range(game_map.HALF_ARENA)):
        if 0 <= y < game_map.HALF_ARENA and left_border0(y) <= x <= right_border0(y):
            my_coordinates.append((x, y))

    left_border1 = lambda _y: _y - 14
    right_border1 = lambda _y: -_y + 41
    enemy_coordinates = []
    for x, y in itertools.product(range(game_map.ARENA_SIZE), range(game_map.HALF_ARENA)):
        if game_map.HALF_ARENA <= y < game_map.ARENA_SIZE and left_border1(y) <= x <= right_border1(y):
            enemy_coordinates.append((x, y))

    return {0: my_coordinates, 1: enemy_coordinates}


def get_structure_combination(SP_budget_constraint):
    # TODO: - replace with constants straight accessing the game-configs.json
    #       - get SP_budget_constraint from the game_state
    wall_cost = 0.5
    turret_cost = 6
    support_cost = 4
    # TODO: - declare this no_structure in a proper global fashion or derive it from the game-configs.json
    no_structures = 3

    def budget_function(wall_weight, turret_weight, support_weight):
        return wall_weight * wall_cost + turret_weight * turret_cost + support_weight * support_cost

    # TODO: - recursive (with memory) implementation might be computationally more efficient
    #       - check: https://stackoverflow.com/questions/38611467/python-get-every-possible-combination-of-weights-for-a-portfolio
    # Assuption: we won't have a SP >= 100, i.e. we assume SP < 100
    possible_weights = []
    for combination in itertools.product(range(100), repeat=no_structures):
        projected_budget = budget_function(*combination)
        if projected_budget == SP_budget_constraint:
            possible_weights.append(combination)

    return possible_weights


def get_upgrade_structure_combination(SP_budget_constraint):
    # TODO: - replace with constants straight accessing the game-configs.json
    #       - get SP_budget_constraint from the game_state
    wall_upgrade_cost = 1.5
    turret_upgrade_cost = 6
    support_upgrade_cost = 2
    # TODO: - declare this no_structure in a proper global fashion or derive it from the game-configs.json
    no_structures = 3

    def budget_function(wall_weight, turret_weight, support_weight):
        return wall_weight * wall_upgrade_cost\
               + turret_weight * turret_upgrade_cost\
               + support_weight * support_upgrade_cost

    # TODO: - recursive (with memory) implementation might be computationally more efficient
    #       - check: https://stackoverflow.com/questions/38611467/python-get-every-possible-combination-of-weights-for-a-portfolio
    # Assuption: we won't have a SP >= 100, i.e. we assume SP < 100
    possible_weights = []
    for combination in itertools.product(range(100), repeat=no_structures):
        projected_budget = budget_function(*combination)
        if projected_budget == SP_budget_constraint:
            possible_weights.append(combination)

    return possible_weights


# def combination_generator(game_state, player_id=0):
def structure_build_combination_generator(game_state, player_id=0, no_samples=10, new_structure_budget_share=1.0):
    # Assume we want to use up all available MP and SP
    # TODO: - create all possible structure combination based on current game state
    #       ---- make it a constant that gets only computed once
    #       - create all possible combination of starting points for the mobile units
    #       ---- use game_map.get_edge_locations(quadrant_description=game_map.BOTTOM_LEFT)
    #       ---- use game_map.get_edge_locations(quadrant_description=game_map.BOTTOM_RIGHT)
    #       ---- make it a constant that gets only computed once
    # Assumptions: - restrict SUPPORTS to y < 8 [not implemented yet]
    # TODO: - make sure we only run this function once per game since the game_map will stay
    #         the same throuought the game
    all_coordinates = get_all_coordinates(game_state) # {0: List(my_coordinates), 1: List(enemy_coordinates)}
    all_structures = get_structures(game_state)       # {0: List(my_structures), 1: List(enemy_structures)}
    my_coordinates = all_coordinates[0]
    my_structures = all_structures[0]

    my_structure_coordinates = []
    for structure in my_structures:
        my_structure_coordinates.append((structure.x, structure.y))

    free_spots_on_board = list(set(my_coordinates) - set(my_structure_coordinates))
    no_available_slots = len(free_spots_on_board)

    # This gives us all combinations on how to allocate our budget to strucure units, i.e. we spend
    # all our budget on building structure units
    SP_budget_constraint = game_state.get_resources(player_index=player_id)[0] # returns [Float, Float] list where the first entry is SP the second is MP
    possible_weights_list = get_structure_combination(SP_budget_constraint=new_structure_budget_share*SP_budget_constraint)

    ### This builts new structure units on random but free spots
    game_state_list = []
    for weights in possible_weights_list:
        wall_weight, turret_weight, support_weight = weights
        no_structure_units = wall_weight + turret_weight + support_weight
        # 'wall' = 'FF'; 'turret' = 'DF'; 'support' = 'EF'
        to_place = ['FF'] * wall_weight + ['DF'] * turret_weight + ['EF'] * support_weight

        for _ in range(no_samples):
            new_game_state = deepcopy(game_state)
            wall_locations = []
            turret_locations = []
            support_locations = []
            for i, placement in enumerate(random.sample(population=range(no_available_slots), k=no_structure_units)):
                x, y = free_spots_on_board[placement]
                if i < wall_weight:
                    wall_locations.append([x, y])
                elif wall_weight <= i < wall_weight + turret_weight:
                    turret_locations.append([x, y])
                else:
                    support_locations.append([x, y])
            if wall_locations:
                new_game_state.attempt_spawn(unit_type='FF', locations=wall_locations, num=1, player_idx=player_id)
            if turret_locations:
                new_game_state.attempt_spawn(unit_type='DF', locations=turret_locations, num=1, player_idx=player_id)
            if support_locations:
                new_game_state.attempt_spawn(unit_type='EF', locations=support_locations, num=1, player_idx=player_id)
            game_state_list.append(new_game_state)

    # print('#' * 10 + ' my_coordinates: {}, my_structure_coords: {}, free_spots: {}, possible_weights: {}, weight_n_permuts: {}, perms: {}'.format(len(my_coordinates), len(my_structure_coordinates), len(free_spots_on_board), len(possible_weights_list), len(weight_permutations), len(permutations)))
    return game_state_list


def _attempt_upgrade(game_state, units, unit_weight, player_id=0):
    if units:
        counter = 0
        random.shuffle(units)
        for unit in units:
            game_state.attempt_upgrade(locations=[unit.x, unit.y], player_idx=player_id)
            counter += 1
            if counter < unit_weight:
                return game_state


def structure_upgrade_combination_generator(game_state_list, player_id=0, upgrade_structure_budget_share=0.25):
    upgraded_game_states = []
    for new_game_state in game_state_list:
        SP_budget_constraint = new_game_state.get_resources(player_index=player_id)[0]  # returns [Float, Float] list where the first entry is SP the second is MP
        # Include constraint where we don't allocate more upgrades than we have structures for [should be taken care of by game_state.attempt_upgrade()]
        possible_weights_list = get_upgrade_structure_combination(SP_budget_constraint=upgrade_structure_budget_share*SP_budget_constraint)
        for weights in possible_weights_list:
            wall_weight, turret_weight, support_weight = weights
            walls, turrets, supports = get_current_structures(new_game_state)  # List(wall_structures), List(turret_structures), List(support_structures)
            new_game_state = _attempt_upgrade(new_game_state, walls, wall_weight, player_id=player_id)
            new_game_state = _attempt_upgrade(new_game_state, turrets, turret_weight, player_id=player_id)
            new_game_state = _attempt_upgrade(new_game_state, supports, support_weight, player_id=player_id)
        upgraded_game_states.append(new_game_state)

    # print('#' * 10 + ' my_coordinates: {}, my_structure_coords: {}, free_spots: {}, possible_weights: {}, weight_n_permuts: {}, perms: {}'.format(len(my_coordinates), len(my_structure_coordinates), len(free_spots_on_board), len(possible_weights_list), len(weight_permutations), len(permutations)))
    return upgraded_game_states


# Add checker is_stationary to all functions (cf. above) [is taken care of]
def random_remove_structure(game_state_list, removal_pct=0.10, player_id=0):
    updated_game_states = []
    for new_game_state in game_state_list:
        all_structures = get_structures(new_game_state)  # {0: List(my_structures), 1: List(enemy_structures)}
        my_structures = all_structures[0]
        random.shuffle(my_structures)
        no_structures = len(my_structures)
        removal_target = np.ceil(removal_pct * no_structures)

        removal_locations = []
        if my_structures:
            # print('#' * 10 + ' type(my_structures): {}, len(my_structures): {}'.format(type(my_structures), len(my_structures)))
            for i, structure in enumerate(my_structures):
                if i < removal_target:
                    removal_locations.append([structure.x, structure.y])
            new_game_state.attempt_remove(locations=removal_locations, player_idx=player_id)
            updated_game_states.append(new_game_state)

    return updated_game_states


def combination_generator(game_state, no_samples=10, new_structure_budget_share=0.75, removal_pct=0.10, player_id=0):
    new_game_states = structure_build_combination_generator(game_state, player_id=player_id, no_samples=no_samples, new_structure_budget_share=new_structure_budget_share)
    upgraded_game_states = structure_upgrade_combination_generator(game_state_list=new_game_states , player_id=player_id, upgrade_structure_budget_share=1.0 - new_structure_budget_share)
    updated_game_states = random_remove_structure(game_state_list=upgraded_game_states, removal_pct=removal_pct, player_id=player_id)

    # TODO: - do the same for mobile units
    return updated_game_states
