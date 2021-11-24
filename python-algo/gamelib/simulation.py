import game_state
import game_map
import util


"""
tracks board state for each frame of the round to determine the resulting game state
@game_obj: deepcopy of self to simulate. current understanding is that it contains the players turns and the board state 
@return: output resulting game state when there are no more mobile units on the field.
"""
# TODO: ensure no side effects to actual game state - call with game_obj object that's a deep copy of actualy game object!


def simulate(game_obj):
    life_lost_p0, life_lost_p1 = 0, 0  # hits taken in this round of player 0 and opponent (p1).

    # while mobile units are on the board
    """
    1) Each unit takes a step, if it is time for them to take a step.
    2) All units attack. See ‘Targeting’ in advanced info
    3) Units that were reduced below 0 health are removed
    """

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
    game_obj.set_resource(resource_type=0, amount=(curr_sp_0 + 5 + life_lost_p1), player_index=0)
    game_obj.set_resource(resource_type=0, amount=(curr_sp_1 + 5 + life_lost_p0), player_index=1)
    return game_obj


# use game_state.find_path_to_edge for pathing, update on destruction of stationary units
# use game_state.get_target to find target of units that can attack
# use game_state.get_attackers to find stationary units threatening a given location
# use game_map.get_locations_in_range to find coordinates to check if there is an enemy unit in range to attack
# use game_map.distance_between_locations
# game_map.add_unit
# game_map.remove_unit
# simulate removal of structures which get removed.

# TODO: return log message if simulation predicted different outcome than observed in online play.
# when running algo online, run simulation on effectively played turns (to verify).
# if observed next state differs from simulated last state: util.debug_write('')
#   store states in logfile

# TODO: unit test simulation

