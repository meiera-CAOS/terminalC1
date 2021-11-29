from unittest import TestCase
import json
from .gamelib import game_state
from .gamelib import simulation
from .gamelib import helper_functions
# from .gamelib.global_variables import
from .gamelib import unit

class Test(TestCase):

    def make_turn_0_map_europe_fall_2021(self):  # downloaded fall2021 config
        config = """
            {
              "seasonCompatibilityModeP1": 5,
              "seasonCompatibilityModeP2": 5,
              "debug":{
                "printMapString":false,
                "printTStrings":false,
                "printActStrings":false,
                "printHitStrings":false,
                "printPlayerInputStrings":false,
                "printBotErrors":true,
                "printPlayerGetHitStrings":false
              },
              "unitInformation": [
                {
                  "icon": "S3_filter",
                  "iconxScale": 0.4,
                  "iconyScale": 0.4,
                  "cost1": 0.5,
                  "getHitRadius":0.01,
                  "display":"Filter",
                  "shorthand":"FF",
                  "startHealth":12.0,
                  "unitCategory": 0,
                  "refundPercentage": 0.75,
                  "turnsRequiredToRemove": 1,
                  "upgrade": {
                    "cost1": 1.5,
                    "startHealth": 120.0
                  }
                },
                {
                  "icon": "S3_encryptor",
                  "iconxScale": 0.5,
                  "iconyScale": 0.5,
                  "cost1":4.0,
                  "getHitRadius":0.01,
                  "shieldPerUnit":3.0,
                  "display":"Encryptor",
                  "shieldRange":3.5,
                  "shorthand":"EF",
                  "startHealth":30.0,
                  "unitCategory": 0,
                  "shieldBonusPerY": 0.0,
                  "refundPercentage": 0.75,
                  "shieldDecay": 0.0,
                  "turnsRequiredToRemove": 1,
                  "upgrade": {
                    "cost1": 2,
                    "shieldRange": 7,
                    "shieldPerUnit":2,
                    "shieldBonusPerY": 0.34
                  }
                },
                {
                  "icon": "S3_destructor",
                  "iconxScale": 0.5,
                  "iconyScale": 0.5,
                  "attackDamageWalker":16.0,
                  "cost1":6.0,
                  "getHitRadius":0.01,
                  "display":"Destructor",
                  "attackRange":3.5,
                  "shorthand":"DF",
                  "startHealth":75.0,
                  "unitCategory": 0,
                  "refundPercentage": 0.75,
                  "turnsRequiredToRemove": 1,
                  "upgrade": {
                    "cost1":6.0,
                    "attackDamageWalker":32.0
                  }
                },
                {
                  "icon": "S3_ping",
                  "iconxScale": 0.7,
                  "iconyScale": 0.7,
                  "attackDamageTower":2.0,
                  "attackDamageWalker":2.0,
                  "playerBreachDamage":1.0,
                  "cost2":1.0,
                  "getHitRadius":0.01,
                  "display":"Ping",
                  "attackRange":3.5,
                  "shorthand":"PI",
                  "startHealth":15.0,
                  "speed":1,
                  "unitCategory": 1,
                  "selfDestructDamageWalker": 15.0,
                  "selfDestructDamageTower": 15.0,
                  "metalForBreach": 1.0,
                  "selfDestructRange": 1.5,
                  "selfDestructStepsRequired": 5
                },
                {
                  "icon": "S3_emp",
                  "iconxScale": 0.47,
                  "iconyScale": 0.47,
                  "attackDamageWalker":16.0,
                  "attackDamageTower":16.0,
                  "playerBreachDamage":1.0,
                  "cost2":3.0,
                  "getHitRadius":0.01,
                  "display":"EMP",
                  "attackRange":4.5,
                  "shorthand":"EI",
                  "startHealth":5.0,
                  "speed":1,
                  "unitCategory": 1,
                  "selfDestructDamageWalker": 5.0,
                  "selfDestructDamageTower": 5.0,
                  "metalForBreach": 1.0,
                  "selfDestructRange": 1.5,
                  "selfDestructStepsRequired": 5
                },
                {
                  "icon": "S3_scrambler",
                  "iconxScale": 0.5,
                  "iconyScale": 0.5,
                  "attackDamageWalker":20.0,
                  "playerBreachDamage":1.0,
                  "cost2":1.0,
                  "getHitRadius":0.01,
                  "display":"Scrambler",
                  "attackRange":4.5,
                  "shorthand":"SI",
                  "startHealth":40.0,
                  "speed":0.25,
                  "unitCategory": 1,
                  "selfDestructDamageWalker": 40.0,
                  "selfDestructDamageTower": 0.0,
                  "metalForBreach": 1.0,
                  "selfDestructRange": 9,
                  "selfDestructStepsRequired": 0
                },
                {
                  "display":"Remove",
                  "shorthand":"RM",
                  "icon": "S3_removal",
                  "iconxScale": 0.4,
                  "iconyScale": 0.4
                },
                {
                  "display":"Upgrade",
                  "shorthand":"UP",
                  "icon": "S3_upgrade",
                  "iconxScale": 0.4,
                  "iconyScale": 0.4
                }
              ],
              "timingAndReplay":{
                "waitTimeBotMax":35000,
                "playWaitTimeBotMax":40000,
                "waitTimeManual":1820000,
                "waitForever":false,
                "waitTimeBotSoft":5000,
                "playWaitTimeBotSoft":10000,
                "replaySave":1,
                "playReplaySave":0,
                "storeBotTimes":true,
                "waitTimeStartGame":3000,
                "waitTimeEndGame":3000
              },
              "resources":{
                "turnIntervalForBitCapSchedule":10,
                "turnIntervalForBitSchedule":10,
                "bitRampBitCapGrowthRate":5.0,
                "roundStartBitRamp":10,
                "bitGrowthRate":1.0,
                "startingHP":30.0,
                "maxBits":150.0,
                "bitsPerRound":5.0,
                "coresPerRound":5.0,
                "coresForPlayerDamage":1.0,
                "startingBits":5.0,
                "bitDecayPerRound":0.25,
                "startingCores":40.0
              },
              "misc":{
                "numBlockedLocations": 0,
                "blockedLocations": [
                ]
              }
            }
        """

        parsed_config = json.loads(config)

        global WALL, SUPPORT, TURRET, SCOUT, DEMOLISHER, INTERCEPTOR, MP, SP
        WALL = parsed_config["unitInformation"][0]["shorthand"]
        SUPPORT = parsed_config["unitInformation"][1]["shorthand"]
        TURRET = parsed_config["unitInformation"][2]["shorthand"]
        SCOUT = parsed_config["unitInformation"][3]["shorthand"]
        DEMOLISHER = parsed_config["unitInformation"][4]["shorthand"]
        INTERCEPTOR = parsed_config["unitInformation"][5]["shorthand"]
        MP = 1
        SP = 0

        # p1Stats":[30.0,40.0,5.0,0] = p1_health, p1_SP, p1_MP, p1_time
        turn_0 = """{"p2Units":[[],[],[],[],[],[],[]],"turnInfo":[0,0,-1],"p1Stats":[30.0,40.0,5.0,0],"p1Units":[[],[],[],[],[],[],[]],"p2Stats":[30.0,40.0,5.0,0],"events":{"selfDestruct":[],"breach":[],"damage":[],"shield":[],"move":[],"spawn":[],"death":[],"attack":[],"melee":[]}}"""

        state = game_state.GameState(json.loads(config), turn_0)
        state.suppress_warnings(True)
        return state

    def test_simulation_empty_turns(self):
        # simulate next game state when both players don't input anything
        game = self.make_turn_0_map_europe_fall_2021()
        # set MP and SP
        init_mp_p0, init_mp_p1 = 8, 5
        init_sp_p0, init_sp_p1 = 6, 40
        # set resources: MP has resource_type 1, SP:0
        game.set_resource(resource_type=MP, amount=init_mp_p0, player_index=0)
        game.set_resource(resource_type=MP, amount=init_mp_p1, player_index=1)
        game.set_resource(resource_type=SP, amount=init_sp_p0, player_index=0)
        game.set_resource(resource_type=SP, amount=init_sp_p1, player_index=1)
        future_mp_p0 = game.project_future_MP(turns_in_future=1, player_index=0, current_MP=game.get_resource(MP, 0))
        future_mp_p1 = game.project_future_MP(turns_in_future=1, player_index=1, current_MP=game.get_resource(MP, 1))

        # simulate
        sim_game_state = simulation.simulate(game)

        # assert correct new resource values
        self.assertEqual(sim_game_state.get_resource(resource_type=MP, player_index=0),
                         future_mp_p0, "MP resource p0")
        self.assertEqual(sim_game_state.get_resource(resource_type=MP, player_index=1),
                         future_mp_p1, "MP resource p1")
        self.assertEqual(sim_game_state.get_resource(resource_type=SP, player_index=0),
                         init_sp_p0 + 5, "SP resource p0")
        self.assertEqual(sim_game_state.get_resource(resource_type=SP, player_index=1),
                         init_sp_p1 + 5, "SP resource p1")
        self.assertEqual(sim_game_state.my_health, 30)

    def test_simulation_structure_deletion(self):
        # simulate next game state when structures get deleted.
        game = self.make_turn_0_map_europe_fall_2021()
        # set structures
        p0_sp_cost, p1_sp_cost, p_0_refund, p_1_refund = 0, 0, 0, 0

        # add structures p0
        turret_locations_p0 = [[0, 13], [27, 13], [8, 11], [19, 11]]
        game.attempt_spawn(TURRET, turret_locations_p0, player_idx=0)
        p0_sp_cost += 4*6  # cost of 4 turrets
        wall_locations_p0 = [[9, 13], [10, 13], [11, 13], [16, 13], [17, 13], [18, 13]]
        game.attempt_spawn(WALL, wall_locations_p0, player_idx=0)
        p0_sp_cost += 6*0.5  # cost of 6 walls
        assert(not game.contains_stationary_unit([9,13]).pending_removal)

        # upgrade structures p0
        upgrade_locations_p0 = [[8, 11], [9, 13], [10, 13], [11, 13], [16, 13]]
        num_upgrades = game.attempt_upgrade(upgrade_locations_p0, player_idx=0)
        # check the 6 locations are upgraded
        for loc in upgrade_locations_p0:
            assert game.contains_stationary_unit(loc).upgraded
        p0_sp_cost += 1*6 + 4*1.5  # cost to upgrade 2 turrets and 4 walls

        # refund structures p0
        game.attempt_remove([[8, 11], [0, 13], [9, 13], [10, 13], [17, 13], [18, 13]], player_idx=0)
        # upgraded turret, normal turret, 2 upgraded walls and 2 normal walls
        # refund = 0.75 * cost * health, rounded to nearest tenth of every unit individually then summed up
        # e.g three not upgraded walls (cost 0.5 each) refund for 0.4 each or 1.2 total
        p_0_refund += simulation.refund(game, [[8, 11], [0, 13], [9, 13], [10, 13], [17, 13], [18, 13]], player_idx=0)
        # refund of 9 + 4.5 + 2*1.5 + 2*0.4 = 17.3
        self.assertEqual(p_0_refund, 17.3, "p_0 refund calculation")

        # add structures p1
        support_locations_p1 = [[12, 20], [13, 20], [12, 19], [13, 19]]
        game.attempt_spawn(SUPPORT, support_locations_p1, player_idx=1)
        p1_sp_cost += 4 * 4
        # extended attempt spawn with player idx, to be allowed to spawn for both players.

        assert(game.contains_stationary_unit([12, 20]))
        assert(game.contains_stationary_unit([13, 20]))
        assert(game.contains_stationary_unit([12, 19]))
        self.assertEqual(game.contains_stationary_unit([13, 19]).unit_type, SUPPORT)

        # set health value of structure
        support_1 = game.contains_stationary_unit([12, 20])
        support_1.health = support_1.max_health / 2  # 15 of 30
        support_2 = game.contains_stationary_unit([13, 20])
        support_2.health = support_2.max_health / 3  # 10 of 30
        support_3 = game.contains_stationary_unit([13, 19])
        support_3.health = support_3.max_health * 2 / 5  # 12 of 30
        support_4 = game.contains_stationary_unit([12, 19])
        support_4.health = support_4.max_health / 6  # 5 of 30

        # upgrade structure
        game.attempt_upgrade([[12, 20], [13, 20]], player_idx=1)
        assert game.contains_stationary_unit([12, 20]).upgraded
        p1_sp_cost += 2*2

        # mark structures to be deleted
        game.attempt_remove([[12, 20], [13, 20], [12, 19], [13, 19]], player_idx=1)
        # upgraded at 15 and 10 hp, normal at 12 and 5 hp.
        p_1_refund += simulation.refund(game, [[12, 20], [13, 20], [12, 19], [13, 19]], player_idx=1)
        # refund of: 2.3 + 1.5 + 1.2 + 0.5 = 5.4
        self.assertEqual(p_1_refund, 5.5, "p_1 refund calculation")
        assert game.contains_stationary_unit([12, 20]).pending_removal
        # simulate
        sim_game_state = simulation.simulate(game)

        # assert correct new resource values (initial values 40 + turn + refund)
        self.assertEqual(40 - p0_sp_cost + 5 + p_0_refund,
                         sim_game_state.get_resource(resource_type=SP, player_index=0), "SP resource p0")
        self.assertEqual(40 - p1_sp_cost + 5 + p_1_refund,
                         sim_game_state.get_resource(resource_type=SP, player_index=1), "SP resource p1")
        self.assertEqual(sim_game_state.my_health, sim_game_state.enemy_health, 30)

        # assert not deleted structure at correct location
        remaining_turrets_pos = [[27, 13], [19, 11]]
        remaining_walls_pos = [[11, 13], [16, 13]]
        for tur in remaining_turrets_pos:
            self.assertEqual(sim_game_state.contains_stationary_unit(tur).unit_type, TURRET)
        for wal in remaining_walls_pos:
            self.assertEqual(sim_game_state.contains_stationary_unit(wal).unit_type, WALL)
        # assert deleted structures map empty
        newly_vacant_pos = [[8, 11], [0, 13], [9, 13], [10, 13], [17, 13],
                            [18, 13], [12, 20], [13, 20], [12, 19], [13, 19]]
        for vac in newly_vacant_pos:
            assert(not sim_game_state.contains_stationary_unit(vac))

    def test_get_mobile_units(self):
        # spawn mobile units and a structure and ensure you get a list of the mobile units.
        game = self.make_turn_0_map_europe_fall_2021()
        game.attempt_spawn(SCOUT, [0, 13], num=3, player_idx=0)
        game.attempt_spawn(INTERCEPTOR, [0, 13], player_idx=0)
        game.attempt_spawn(DEMOLISHER, [27, 14], player_idx=1)
        support_locations_p1 = [[12, 20], [13, 20], [12, 19], [13, 19]]
        game.attempt_spawn(SUPPORT, support_locations_p1, player_idx=1)
        mobile_units = helper_functions.get_mobile_units(game)
        self.assertEqual(len(mobile_units[0]), 4)
        self.assertEqual(len(mobile_units[1]), 1)

    def test_simulation_first_mobile_unit(self):
        # spawn two and one mobile units that runs across the field unimpeded and deal damage to the opposing player
        game = self.make_turn_0_map_europe_fall_2021()
        game.attempt_spawn(SCOUT, [0, 13], player_idx=0)  # PI
        game.attempt_spawn(INTERCEPTOR, [0, 13], player_idx=0)  # SI
        game.attempt_spawn(DEMOLISHER, [27, 14], player_idx=1)  # EI
        units = helper_functions.get_mobile_units(game)
        print(units)
        sim_game_state = simulation.simulate(game)

        # test MP values
        self.assertEqual(sim_game_state.get_resources(player_index=0), [47, 7.3])
        self.assertEqual(sim_game_state.get_resources(player_index=1), [46, 6.5])

        # test HP total
        self.assertEqual(sim_game_state.my_health, 29, "assert own life total")
        self.assertEqual(sim_game_state.enemy_health, 28, "assert enemy life total")

        # ensure no mobile units in state
        assert(not helper_functions.get_mobile_units(sim_game_state, both_players=True))

    def test_simulation_mobile_unit_vs_tower(self):
        # spawn multiple mobile units that runs into a turret,
        # balanced such that the turret and all but one mobile unit is destroyed
        game = self.make_turn_0_map_europe_fall_2021()
        game.attempt_spawn(TURRET, [13, 13], player_idx=0)
        game.set_resource(MP, amount=8, player_index=1)
        game.attempt_spawn(SCOUT, [21, 20], num=8, player_idx=1)
        sim_game = simulation.simulate(game)
        # assert HP of turret is correct. (barely survives: 36 = 8+7+6+5+4+3+2+1 attacks taken, 2dmg each, 3 hp)
        self.assertEqual(sim_game.contains_stationary_unit([13, 13]).health, 3)
        self.assertEqual(sim_game.my_health, 30, "assert own life total")
        self.assertEqual(sim_game.enemy_health, 30, "assert enemy life total")
        # assert no mobile units on map
        assert not helper_functions.get_mobile_units(sim_game, both_players=True)

    '''def test_simulation_mobile_units_vs_tower_and_wall(self):
        # test targeting of attacking and defensive structure
        assert False

    def test_mobile_unit_speed(self):
        # figure out a way to ensure that units move at appropriate speed.
        assert False

    def test_simulation_intercepting_mobile_units(self):
        # spawn mobile units that runs into each other and fight
        game = self.make_turn_0_map_europe_fall_2021()
        assert False

    def test_simulation_self_destruct_mobile_units(self):
        # spawn mobile units that run trigger self destruction
        game = self.make_turn_0_map_europe_fall_2021()
        assert False'''

    def test_simulation_shields(self):
        # spawn support structures and shields and ensure they affect units in range
        # (only once) and that they provide the right amount of shield (which interacts with damage as intended)
        game = self.make_turn_0_map_europe_fall_2021()
        # two upgraded shields at y = 13 + one upgraded at y = 6 -> turret needs two hits
        game.attempt_spawn(TURRET, [15, 14], player_idx=1)
        support_locations = [[11, 13], [12, 13], [11, 6]]
        game.attempt_spawn(SUPPORT, support_locations, player_idx=0)
        game.attempt_upgrade(support_locations, player_idx=0)
        game.attempt_spawn(SCOUT, [7, 6], num=5, player_idx=0)
        sim_game = simulation.simulate(game)

        # one scout dealt damage
        # tower has (5*2 + 4*2 + 3*2 + 2*2 + 1) * 2 damage = 58, 75-58 = 17 < 75/4
        self.assertEqual(sim_game.contains_stationary_unit([15, 14]).health, 17)
        self.assertEqual(sim_game.enemy_health, 29)

        # two upgraded shields at y = 14 + one at y = 27-7 -> turret needs three hits
        game = self.make_turn_0_map_europe_fall_2021()
        game.attempt_spawn(TURRET, [11, 13], player_idx=0)
        support_locations = [[16, 14], [17, 14], [17, 20]]
        game.attempt_spawn(SUPPORT, support_locations, player_idx=1)
        game.attempt_upgrade(support_locations, player_idx=1)
        game.attempt_spawn(SCOUT, [21, 20], num=5, player_idx=1)
        sim_game_2 = simulation.simulate(game)
        # tower has (5*3 + 4*3 + 3*3) * 2 damage = 72,-> 3 hp
        self.assertEqual(sim_game_2.contains_stationary_unit([11, 13]).health, 3)
        self.assertEqual(sim_game_2.my_health, 28)

    # todo: read rules again and check for forgotten feature of simulation.
