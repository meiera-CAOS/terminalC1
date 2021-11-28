from .game_state import GameState, is_stationary
from .unit import GameUnit
from .helper_functions import get_structures, get_mobile_units, get_all_units, round_half_up
from .game_map import GameMap
from .global_variables import DEBUG
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


#   SELF_DESTRUCT
#   The self-destruct only damages enemy units and has a range of 1.5.
#   The damage dealt to each affected enemy is equal to the starting health of the self-destructing unit.
#   However, self-destruct damage will only occur if the unit has moved at least 5 spaces before self-destructing.
#   Units will still attack on the frame that they self-destruct.
#   If units.self_destruct_flag == 2 it will deal damage on self destruct.
#   The unit still attacks in the frame where they will self-destruct (one frame after reaching the bottleneck)
#   is the unit still targetable? NO: the unit will not be attacked anymore the frame after it reached the self destructs.
#   idk what happens if the path is freed the frame it would self destruct, i believe it self destructs.

def attack():
    """Performs the attacks of all units in order of creation

    Args:
        args:

    Returns:
    """
    #  TODO: targeting and damage is in order of creation (keep track of creation order..?)
    #   is the order given my the order of the units in get_mobile_units / get_attacking_units
    #  never target a unit which is below 0 hp.


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
        if unit.health < 0:  # TODO: list has no health!
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

    # remove unit from mobile_units
    # remove unit from game state
    # todo remove unit from attacking units?

# TODO: to ensure no side effects to actual game state - call with game_obj object that's a deep copy of actually game object!


def simulate(game_obj):  # todo: indicate victory, loss, or tie. suppose you always lose the time tiebreaker.
    """Simulates the game frames after turns have been submitted to calculate the next game state.

    Args:
        game_obj: a GameState obj (includes newly deployed mobile units)

    Returns:
        simulated_game_state: the next GameState obj
        round_end_state: -1: loss, 0: ongoing, 1: win.
    """
    life_lost_p0, life_lost_p1 = 0, 0  # hits taken in this round of player 0 and opponent (p1).

    mobile_units = get_mobile_units(game_obj, both_players=True)
    frame = 0
    if mobile_units:
        frame =1
        # calculate paths for each unit and (?)store it in mobile_units dict
        for m_unit in mobile_units:
            m_unit.path = GameState.find_path_to_edge(game_obj, start_location=[m_unit.x, m_unit.y])[1:]  # exclude current pos from path.
        # simulate frames
        while mobile_units:  # while mobile units are on the board

            for unit in mobile_units:  # 1) Each unit takes a step, if it is time for them to take a step.
                scores = 0
                if unit.unit_type == "SI":  # interceptor
                    # interceptor moves at 4th frame for the first time, every 4 frames
                    assert unit.speed == 0.25  # 4
                    if frame > 1 and frame % 4 == 0:
                        scores = advance_unit(game_obj, unit, frame)
                else:
                    scores = advance_unit(game_obj, unit, frame)  # scout and demolisher move every frame,
                if scores:
                    if unit.player_index == 0:
                        life_lost_p1 += 1
                    else:  # unit.player_index == 1
                        life_lost_p0 += 1

            # for unit in attacking_units:  # ordered queue pointing to unit object?
                # 2) All units attack. See ‘Targeting’ in advanced info
            removed_structure = clean_up(game_obj)  # 3) Units that were reduced below 0 health are removed

            mobile_units = get_mobile_units(game_obj, both_players=True)  # update mobile units
            if removed_structure:
                for m_unit in mobile_units:  # if structure was removed: recompute path of mobile units.
                    m_unit.path = GameState.find_path_to_edge([m_unit.x, m_unit.y])[1:]
            frame += 1

    # use game_state.get_target to find target of units that can attack
    # use game_state.get_attackers to find stationary units threatening a given location
    # use game_map.get_locations_in_range to find coordinates to check if there is an enemy unit in range to attack
    # use game_map.distance_between_locations
    if DEBUG:
        print("Simulation frame: ", frame)

    ### AT END OF ROUND: Remove pending_remove structures and refund, increase resources for next round

    # set new HP
    game_obj.my_health -= life_lost_p0
    game_obj.enemy_health -= life_lost_p1

    # todo: check end state ongoing / win / loss. adapt return value and where it's called (tests).

    # for standing structures, for each player refund structures marked as pending_remove and remove from game_map
    structures = get_structures(game_obj)
    structures_p0 = structures[0]
    structures_p1 = structures[1]
    refund_p0, refund_p1 = 0, 0
    for structure in structures_p0:
        refund_p0 = round_half_up(refund_p0 + manage_pending_removal(game_obj, structure, player_idx=0), 1)
    for structure in structures_p1:
        refund_p1 = round_half_up(refund_p1 + manage_pending_removal(game_obj, structure, player_idx=1), 1)

    # add MP = 1 resources
    curr_mp_0 = game_obj.get_resource(resource_type=1, player_index=0)
    curr_mp_1 = game_obj.get_resource(resource_type=1, player_index=1)
    next_mp_0 = game_obj.project_future_MP(turns_in_future=1, player_index=0, current_MP=curr_mp_0)
    next_mp_1 = game_obj.project_future_MP(turns_in_future=1, player_index=1, current_MP=curr_mp_1)
    game_obj.set_resource(resource_type=1, amount=next_mp_0, player_index=0)
    game_obj.set_resource(resource_type=1, amount=next_mp_1, player_index=1)
    # add SP = 0 resources
    curr_sp_0 = game_obj.get_resource(resource_type=0, player_index=0)
    curr_sp_1 = game_obj.get_resource(resource_type=0, player_index=1)
    game_obj.set_resource(resource_type=0, amount=(curr_sp_0 + 5 + life_lost_p1 + refund_p0), player_index=0)
    game_obj.set_resource(resource_type=0, amount=(curr_sp_1 + 5 + life_lost_p0 + refund_p1), player_index=1)
    return game_obj

# TODO: return log message if simulation predicted different outcome than observed in online play.
# when running algo online, run simulation on effectively played turns (to verify).
# if observed next state differs from simulated last state: util.DEBUG_write('')
#   store states in logfile


