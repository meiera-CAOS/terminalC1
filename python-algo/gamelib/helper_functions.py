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
            if unit:
                # y_item is a unit
                if unit[0].player_index == 0:
                    structures[0].append(unit[0])
                else:
                    structures[1].append(unit[0])

    return structures

