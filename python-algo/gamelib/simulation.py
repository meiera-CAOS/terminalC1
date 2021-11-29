import copy

import helper_functions
from .game_state import is_stationary
# from .unit import GameUnit
from .helper_functions import get_structures, get_mobile_units, get_all_units, get_shield_units, round_half_up
from .game_map import GameMap
from .global_variables import DEBUG, STATIONARY_UNITS
# from util

import logging

log = logging.getLogger(__name__)


def manage_pending_removal(game_obj, structure, player_idx):
    refund_val = 0
    if structure.pending_removal:
        loc = [structure.x, structure.y]
        refund_val += refund(game_obj, loc, player_idx=player_idx)  # refund to player
        game_obj.game_map.remove_unit(loc)  # remove from game map
        return refund_val
    else:
        return 0


def refund(game_obj, locations, player_idx=0):  # return refunded resource
    """Calculates refund of existing friendly structures in the given locations.

    Args:
        game_obj: the game object
        locations: A location or list of locations we want to remove structures from
        player_idx: The player who attempts to remove a structure

    Returns:
        The refunded SP for the removal
    """
    if type(locations[0]) == int:
        locations = [locations]
    refund_sum = 0.0
    for location in locations:
        if game_obj.contains_stationary_unit(location) and ((player_idx == 0 and location[1] < game_obj.HALF_ARENA)
                                                            or (player_idx == 1 and location[1] >= game_obj.HALF_ARENA)):
            # select game unit at location
            curr_unit = game_obj.contains_stationary_unit(location)
            # detect it's health ratio
            if curr_unit.unit_type == 0:
                print("WALL HEALTH: ", curr_unit.health, curr_unit.max_health)
            structure_value = round_half_up(curr_unit.cost[0] * (curr_unit.health / curr_unit.max_health) * 0.75, decimals=1)
            refund_sum = round_half_up(refund_sum + structure_value, decimals=1)
        else:
            game_obj.warn("Could not refund a unit from {}. Location has no structures or is enemy territory.".format(location))
    return refund_sum


def score_or_self_destruct(unit, frame):
    """Checks if mobile units having reached their destination (empty path) score or selfdesctruct and handle the cases

    Args:
        unit: the mobile unit
        frame: the turn of the round, (no self destruct damage < 5 to buildings).

    Returns:
        1 if the unit scored a damage to the opponent, 0 otherwise (sideffect of selfdestruction)
    """
    if DEBUG:  # check what flags are set (should be only one of either)
        assert((unit.self_destruct_flag and not unit.scores_next_frame) or
               (not unit.self_destruct_flag and unit.scores_next_frame))
    scores = 0
    unit.health = -1  # not targeted anymore.
    if unit.self_destruct_flag:
        if unit.type == "SI" or frame >= 5:
            unit.self_destruct_flag = 2  # deal self destruct damage this frame
    if unit.scores_next_frame:
        scores = 1
    return scores

#   SHIELD:
#   how does shield even work? bonus hp? Shield is bonus hp and is treated as health for the sake of targeting.
#   the y value is relative for each player


def advance_unit(game_obj, unit, frame):
    """Performs the move of mobile unit, handles scoring and self destruct

    Args:
        game_obj: game state
        unit: the mobile unit
        frame: the turn of the round, (no self destruct damage < 5 to buildings).

    Returns:
        1 if the unit scored
    """
    if not unit.path:
        return score_or_self_destruct(unit, frame)
    new_pos = unit.path.pop(0)  # move unit one step along it's path
    if GameMap.move_unit_on_map(game_obj.game_map, unit=unit, new_location=new_pos):
        unit.x, unit.y = new_pos  # set new position in unit attributes
    # if path is null after the move, check boarder: self_destruct or score on the next move!
    if not unit.path:  # checks if this was the last step of the unit
        pos = [unit.x, unit.y]
        edges = GameMap.get_all_edges()
        if pos in edges:  # check if position on edge or self destruct
            unit.scores_next_frame = True  # if it survives this rounds attacks
        else:  # set corresponding flag
            unit.self_destruct_flag = 1  # if it survives this rounds attacks
    return 0


def give_shield(game, supports_list, player_index=0):
    """ checks for each support unit, looks for mobile units in range (
    that have not yet received the buff from this unit) to shield

    Args:
        game: game state obj
        supports_list: support units of one player
        player_index: the corresponding player
    """
    for shield in supports_list:
        if shield.upgraded:
            radius = 7
            if player_index == 0:
                shield_bonus = shield.y
            else:
                shield_bonus = 27 - shield.y
            shield_value = 2.0 + (0.34 * shield_bonus)
        else:
            radius = 3.5
            shield_value = 2.0
        friendly_units_in_range = game.game_map.get_units_in_range([shield.x, shield.y], radius, player_idx=player_index)
        m_units_in_range = [x for x in friendly_units_in_range if x.unit_type not in STATIONARY_UNITS]
        for m_unit in m_units_in_range:
            if [shield.x, shield.y] not in m_unit.shieldsFrom:  # check buff not already given
                m_unit.shieldsFrom.append([shield.x, shield.y])
                m_unit.health += shield_value
    return


def manage_shield(game, shield_units_dict):
    """ checks for each support unit, looks for mobile units in range (
    that have not yet received the buff from this unit) to shield

    Args:
        game: game state obj
        shield_units_dict: support units [0]: p0, [1]: p1
    """
    mobile_units = get_mobile_units(game, both_players=False)
    m_units_p0 = mobile_units[0]
    m_units_p1 = mobile_units[1]
    if not (m_units_p0 or m_units_p1):  # no mobile units
        return
    if m_units_p0:
        give_shield(game, shield_units_dict[0], player_index=0)
    if m_units_p1:
        give_shield(game, shield_units_dict[1], player_index=1)
    return


def target(game, unit):
    """finds target of attack for unit

    Args:
        game: game state obj
        unit: unit that looks for target to attack

    Returns:
        targeted unit or false if no unit was targeted.
    """
    player_id_of_unit = unit.player_index
    enemy_player_index = (player_id_of_unit + 1) % 2
    unit_loc = [unit.x, unit.y]
    # get all units within range
    enemy_units = game.game_map.get_units_in_range([unit.x, unit.y], unit.attackRange, enemy_player_index)
    enemy_units = [x for x in enemy_units if x.health > 0]  # remove all enemy_units with health below 0

    # if mobile units in range, target mobile unit
    if not enemy_units:
        return False
    if len(enemy_units) == 1:
        return enemy_units[0]
    else:  # multiple enemy units in range, check if there are mobile units, if yes reduce list to mobile units.
        enemy_mobile_units = [x for x in enemy_units if x.unit_type not in STATIONARY_UNITS]
        if enemy_mobile_units:
            if len(enemy_mobile_units) == 1:
                return enemy_mobile_units[0]
            enemy_units = enemy_mobile_units  # multiple enemy mobile units

        # pick nearest target(s)
        nearest_enemy_units = []
        nearest_distance = unit.attackRange + 1
        for e_unit in enemy_units:
            dist = game.game_map.distance_between_locations([e_unit.x, e_unit.y], unit_loc)
            if dist < nearest_distance:
                nearest_enemy_units = [e_unit]
                nearest_distance = dist
            elif dist == nearest_distance:
                nearest_enemy_units.append(e_unit)
        if DEBUG:
            assert nearest_enemy_units  # not empty
        if len(nearest_enemy_units) == 1:
            return nearest_enemy_units[0]

        # if multiple pick lowest health > 0 where shield is added to health already
        lowest_health = nearest_enemy_units[0].health
        lowest_health_units = [nearest_enemy_units[0]]
        for idx in range(1, len(nearest_enemy_units)):  # check remaining units for lowest health.
            n_unit = nearest_enemy_units[idx]
            if n_unit.health < lowest_health:
                lowest_health_units = [n_unit]
            elif n_unit.health == lowest_health:
                lowest_health_units.append(n_unit)
        if DEBUG:
            assert lowest_health > 0  # as filtered out at start of this function
        if len(lowest_health_units) == 1:
            return lowest_health_units[0]

        # multiple lowest health targets, choose y coordinate closest to your side
        closest_y_units = []
        closest_y_dist = 27
        if player_id_of_unit == 0:  # closest to 0
            y_side = 0
        else:  # closest to 27
            y_side = 27
        for c_unit in lowest_health_units:
            y_dist = abs(y_side - c_unit.y)
            if y_dist < closest_y_dist:
                closest_y_dist = y_dist
                closest_y_units = [c_unit]
            elif y_dist == closest_y_dist:
                closest_y_units.append(c_unit)
        if len(closest_y_units) == 1:
            return closest_y_units[0]

        # if multiple choose closest to edge,
        # keep only the first closest in memory, it will default to it in case of ties
        x_edge_1, x_edge_2 = [x_u for x_u in game.game_map.get_all_edges() if x_u[1] == closest_y_units[0].y]
        closest_x_dist = 15
        final_target = None  # there
        for x_unit in closest_y_units:
            x_dist = min(abs(x_unit.x - x_edge_1[0]), abs(x_unit.x - x_edge_2[0]))
            if x_dist < closest_x_dist:
                closest_x_dist = x_dist
                final_target = x_unit
        if DEBUG:
            assert final_target
        return final_target


def attack(game, unit):
    """Performs the attacks of all units in order of creation

    Args:
        game: game state obj
        unit: unit that performs attack

    Returns:
        attacked unit or false if no unit was attacked.
    """
    player_id_of_unit = unit.player_index
    enemy_player_index = (player_id_of_unit + 1) % 2

    # targeting for normal attack:
    target_unit = target(game, unit)
    if target_unit:  # if there is a target, deal damage to target apropriate to target type.
        if target_unit.unit_type in STATIONARY_UNITS:
            target_unit.health -= unit.damage_f
        else:
            target_unit.health -= unit.damage_i

    if unit.self_destruct_flag == 2:  # do self destruct damage to all enemy units within selfdestruct range
        # flag is only set for 5 steps or inerceptors
        # I don't see the attributes for self destruct range / etc so I hard code it1.5.
        sd_damage = unit.max_health
        if unit.unit_type == "SI":  # interceptor
            sd_range = 9
            enemy_targets = game.game_map.get_units_in_range([unit.x, unit.y], sd_range, enemy_player_index)
            enemy_mobile_targets = enemy_targets = [x for x in enemy_targets if x.unit_type not in STATIONARY_UNITS]
        else:
            sd_range = 1.5
            enemy_targets = game.game_map.get_units_in_range([unit.x, unit.y], sd_range, enemy_player_index)
        for e_target in enemy_targets:  # deal damage to all enemy targets in range
            e_target.health -= sd_damage

    if not target_unit:
        return False
    else:
        return target_unit


def clean_up(game_obj):
    """Remove all structures and mobile units with health below 0

    Args:
        game_obj: the current game state

    Returns:
        Boolean indicating if a structure was removed
    """
    removed_structure = False
    all_units = get_all_units(game_obj, both_players=True)
    '''if DEBUG:
        print("clean_up, number of units found to verify: ", len(all_units))'''
    for unit in all_units:
        '''if DEBUG and isinstance(unit, list):
            print("expected unit, got list: ", unit)'''
        if unit.health <= 0:
            if is_stationary(unit.unit_type):
                removed_structure = True
                GameMap.remove_unit(game_obj.game_map, [unit.x, unit.y])
                if DEBUG:  # check that structure is not in game state any longer
                    if game_obj.contains_stationary_unit([unit.x, unit.y]):
                        log.warning("clean_up, removing stationary unit from map did not remove it from game state.")
            else:
                # remove mobile unit
                removed_mobile_unit = GameMap.remove_mobile_unit(game_obj.game_map, unit)
                if DEBUG:
                    '''print("clean up: mobile unit to be removed: ", unit)
                    print("removal success: ", removed_mobile_unit)'''
                if not removed_mobile_unit:
                    log.warning("### clean_up, didn't find mobile unit to remove in game map.")
                    if DEBUG:
                        assert False
    return removed_structure


def simulate(game_obj, game_turn=0):  # todo: indicate victory, loss, or tie. suppose you always lose the time tiebreaker.
    # todo: speedup by updating the different lists (mobile units, all units, attacking units) instead of querying...
    """Simulates the game frames after turns have been submitted to calculate the next game state.

    Args:
        game_obj: a GameState obj (includes newly deployed mobile units)

    Returns:
        simulated_game_state: the next GameState obj
        round_end_state: -1: loss, 0: ongoing, 1: win.
    """
    game = copy.deepcopy(game_obj)
    life_lost_p0, life_lost_p1 = 0, 0  # hits taken in this round of player 0 and opponent (p1).
    frame = 0

    mobile_units = get_mobile_units(game, both_players=True)
    shield_units_dict = get_shield_units(game, both_players=False)  # dict key = player_idx
    manage_shield(game, shield_units_dict)

    if mobile_units:
        frame = 1
        for m_unit in mobile_units:  # calculate paths for mobile units
            m_unit.path = game.find_path_to_edge(start_location=[m_unit.x, m_unit.y])[1:]  # exclude current pos from path.
        # simulate frames
        while mobile_units:  # while mobile units are on the board

            for unit in mobile_units:  # 1) Each unit takes a step, if it is time for them to take a step.
                scores = 0
                if unit.unit_type == "SI":  # interceptor
                    # interceptor moves at 4th frame for the first time, every 4 frames
                    assert unit.speed == 0.25  # 4
                    if frame > 1 and frame % 4 == 0:
                        scores = advance_unit(game, unit, frame)
                else:
                    scores = advance_unit(game, unit, frame)  # scout and demolisher move every frame,
                if scores:
                    if unit.player_index == 0:
                        life_lost_p1 += 1
                    else:  # unit.player_index == 1
                        life_lost_p0 += 1

            # check for new shields to be given
            manage_shield(game, shield_units_dict)

            atk_units = helper_functions.get_attacking_units(game, both_players=True)
            for unit in atk_units:  # assume order is correct ;)
                attack(game, unit)  # decide on target, deal damage

            removed_structure = clean_up(game)  # 3) Units that were reduced below 0 health are removed

            mobile_units = get_mobile_units(game, both_players=True)  # update mobile units
            if removed_structure:
                for m_unit in mobile_units:  # if structure was removed: recompute path of mobile units.
                    m_unit.path = game.find_path_to_edge([m_unit.x, m_unit.y])[1:]
            frame += 1

    # use game_state.get_target to find target of units that can attack
    # use game_state.get_attackers to find stationary units threatening a given location
    # use game_map.get_locations_in_range to find coordinates to check if there is an enemy unit in range to attack
    # use game_map.distance_between_locations
    if DEBUG:
        print("Simulation frame: ", frame)

    ### AT END OF ROUND: Remove pending_remove structures and refund, increase resources for next round

    # set new HP
    game.my_health -= life_lost_p0
    game.enemy_health -= life_lost_p1

    # 0: ongoing, -1: lost, 1: won
    we_win = 0
    if game.my_health <= 0:  # always lose ties (computation time)
        we_win = -1
    elif game.enemy_health <= 0:
        we_win = 1
    if game_turn == 100:
        we_win = -1
        if game.my_health > game.enemy_health:
            we_win = 1

    # for standing structures, for each player refund structures marked as pending_remove and remove from game_map
    structures = get_structures(game)
    structures_p0 = structures[0]
    structures_p1 = structures[1]
    refund_p0, refund_p1 = 0, 0
    for structure in structures_p0:
        refund_p0 = round_half_up(refund_p0 + manage_pending_removal(game, structure, player_idx=0), 1)
    for structure in structures_p1:
        refund_p1 = round_half_up(refund_p1 + manage_pending_removal(game, structure, player_idx=1), 1)

    # add MP = 1 resources
    curr_mp_0 = game.get_resource(resource_type=1, player_index=0)
    curr_mp_1 = game.get_resource(resource_type=1, player_index=1)
    next_mp_0 = game.project_future_MP(turns_in_future=1, player_index=0, current_MP=curr_mp_0)
    next_mp_1 = game.project_future_MP(turns_in_future=1, player_index=1, current_MP=curr_mp_1)
    game.set_resource(resource_type=1, amount=next_mp_0, player_index=0)
    game.set_resource(resource_type=1, amount=next_mp_1, player_index=1)
    # add SP = 0 resources
    curr_sp_0 = game.get_resource(resource_type=0, player_index=0)
    curr_sp_1 = game.get_resource(resource_type=0, player_index=1)
    game.set_resource(resource_type=0, amount=(curr_sp_0 + 5 + life_lost_p1 + refund_p0), player_index=0)
    game.set_resource(resource_type=0, amount=(curr_sp_1 + 5 + life_lost_p0 + refund_p1), player_index=1)
    return game, we_win

