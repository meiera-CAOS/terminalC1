from .game_state import GameState
from .unit import GameUnit
from .helper_functions import get_structures, get_mobile_units
from .game_map import get_all_edges
# from util


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
            structure_value = round(curr_unit.cost[0] * (curr_unit.health / curr_unit.max_health) * 0.75, 1)
            refund_sum = round(refund_sum + structure_value, 1)
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
    # todo
    # check what flag is set (should be only one of both)
    # if both or none is set - warn
    hit_edge = 0
    if unit.self_destruct_next_frame and (unit.type ==  "SI" or frame >= 5):
        # self_destruct
    if unit.scores_next_frame:
        hit_edge += 1
        # score
    return hit_edge

#  TODO: The self-destruct only damages enemy units and has a range of 1.5.
#   The damage dealt to each affected enemy is equal to the starting health of the self-destructing unit.
#   However, self-destruct damage will only occur if the unit has moved at least 5 spaces before self-destructing.
#   Units will still attack on the frame that they self-destruct.
#   The unit still attacks in the frame where they will self-destruct (one frame after reaching the bottleneck)
#   is the unit still targetable? NO: the unit will not be attacked anymore the frame it selfdestructs.
#   how does shield even work? bonus hp? Shield is bonus hp and is treated as health for the sake of targeting.

def advance_unit(unit):
    if not unit.path:
        score_or_self_destruct(unit)  # todo
        return
    # move unit one step along it's path
    new_pos = unit.path.pop(0)
    # if path is null after the move, check boarder / either self_destruct or deal 1 damage to opponent on the next move!
    if not unit.path:
        pos = [unit.x, unit.y]
        edges = get_edges()  # returns pos of edges on the 4 edges (in 4 lists)
        all_edges = []  # build a list of all edges
        if pos in get_edges()[1] or pos in
        # check if position on edge or selfdestruct
        # set corresponding flag.

"""
tracks board state for each frame of the round to determine the resulting game state
@game_obj: deepcopy of self to simulate. current understanding is that it contains the players turns and the board state 
@return: output resulting game state when there are no more mobile units on the field.
"""
# TODO: to ensure no side effects to actual game state - call with game_obj object that's a deep copy of actually game object!


def simulate(game_obj):
    life_lost_p0, life_lost_p1 = 0, 0  # hits taken in this round of player 0 and opponent (p1).

    # while mobile units are on the board
    """
    1) Each unit takes a step, if it is time for them to take a step.
    2) All units attack. See ‘Targeting’ in advanced info
    3) Units that were reduced below 0 health are removed
    """
    mobile_units = get_mobile_units(game_obj)
    if mobile_units:
        # calculate paths for each unit and (?)store it in mobile_units dict
        for m_unit in mobile_units:
            m_unit.path = GameState.find_path_to_edge(m_unit.path[0])  # if final step is not an edge, it's a self destruct path
        # simulate frames
        frame = 0
        while mobile_units:
            for unit in mobile_units:
                if unit.unit_type == "SI":
                    assert unit.speed == 0.25  # 4
                    if frame > 1 and frame % 4 == 0:
                        advance_unit(unit)
                else:
                    advance_unit(unit)

                # check if unit takes a step, if yes move it
                # scout and demolisher move every frame, interceptor moves at 4th frame for the first time, every 4 frames
                # if unit reaches enemy boarder (needs one more step or just to arrive?)
                    # deal one damage, remove unit (immedeately or will it attack / take damage?)
                # if unit reaches self destruct point
            for unit in mobile_units: # and for turrets
                # todo: check if in range of attackers and if in range of targets (how does targeting work?)
                # todo: all units attack (update units hp), if leq 0 add to list to remove at end of combat
                # (with simultaneous attacks, do some units attack same target even if damage is overkill?)
                # todo: remove all destroyed units
                # if structure leq 0 set boolean to recompute pathing for mobile units.

    # use game_state.find_path_to_edge for pathing, update on destruction of stationary units
    # use game_state.get_target to find target of units that can attack
    # use game_state.get_attackers to find stationary units threatening a given location
    # use game_map.get_locations_in_range to find coordinates to check if there is an enemy unit in range to attack
    # use game_map.distance_between_locations
    # use game_state.attempt_spawn / attempt_remove / attempt_upgrade
    # contains_stationary_unit
    # game_map.add_unit
    # game_map.remove_unit
    # simulate removal of structures which get removed.

    ### AT END OF ROUND: Remove pending_remove structures and refund, increase resources for next round

    # for standing structures, for each player refund structures marked as pending_remove and remove from game_map
    structures = get_structures(game_obj)
    structures_p0 = structures[0]
    structures_p1 = structures[1]
    refund_p0, refund_p1 = 0, 0
    for structure in structures_p0:  # TODO: make sure that those are only structures!
        refund_p0 = round(refund_p0 + manage_pending_removal(game_obj, structure, player_idx=0), 1)
    for structure in structures_p1:
        refund_p1 = round(refund_p1 + manage_pending_removal(game_obj, structure, player_idx=1), 1)

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
# if observed next state differs from simulated last state: util.debug_write('')
#   store states in logfile


