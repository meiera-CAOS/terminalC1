from unittest import TestCase
import json
from .gamelib import game_state
from .gamelib import simulation

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
        # p1Stats":[30.0,40.0,5.0,0] = p1_health, p1_SP, p1_MP, p1_time
        turn_0 = """{"p2Units":[[],[],[],[],[],[],[]],"turnInfo":[0,0,-1],"p1Stats":[30.0,40.0,5.0,0],"p1Units":[[],[],[],[],[],[],[]],"p2Stats":[30.0,40.0,5.0,0],"events":{"selfDestruct":[],"breach":[],"damage":[],"shield":[],"move":[],"spawn":[],"death":[],"attack":[],"melee":[]}}"""

        state = game_state.GameState(json.loads(config), turn_0)
        state.suppress_warnings(True)
        return state

    def test_simulation_empty_turns(self):
        # simulate next game state when both players don't input anything
        game = self.make_turn_0_map_europe_fall_2021()
        print("MP of player 0 after init = ", game.get_resource(1, 0))
        print("SP of player 0 after init = ", game.get_resource(0, 0))
        print("my health", game.my_health)
        # set MP and SP
        init_mp_p0, init_mp_p1 = 8, 5
        print(init_mp_p0, init_mp_p1)
        init_sp_p0, init_sp_p1 = 6, 40
        # set resources: MP has resource_type 1, SP:0
        game.set_resource(resource_type=1, amount=init_mp_p0, player_index=0)
        game.set_resource(resource_type=1, amount=init_mp_p1, player_index=1)
        print("MP of player 0 after set_resource = ", game.get_resource(1, 0))
        game.set_resource(resource_type=0, amount=init_sp_p0, player_index=0)
        game.set_resource(resource_type=0, amount=init_sp_p1, player_index=1)
        future_mp_p0 = game.project_future_MP(turns_in_future=1, player_index=0, current_MP=game.get_resource(1, 0))
        print("MP of player 0 after project_future = ", future_mp_p0)
        future_mp_p1 = game.project_future_MP(turns_in_future=1, player_index=1, current_MP=game.get_resource(1, 1))
        # simulate
        sim_game_state = simulation.simulate(game)
        print("simulated MP after project_future = ", sim_game_state.get_resource(resource_type=1, player_index=0))

        # assert correct new resource values
        self.assertEqual(sim_game_state.get_resource(resource_type=1, player_index=0),
                         future_mp_p0, "MP resource p0")
        self.assertEqual(sim_game_state.get_resource(resource_type=1, player_index=1),
                         future_mp_p1, "MP resource p1")
        self.assertEqual(sim_game_state.get_resource(resource_type=0, player_index=0),
                         init_sp_p0 + 5, "SP resource p0")
        self.assertEqual(sim_game_state.get_resource(resource_type=0, player_index=1),
                         init_sp_p1 + 5, "SP resource p1")

        # ensure gamestate is identical other than the resources increasing
        # TODO: compare health
        # TODO: compare stationary units