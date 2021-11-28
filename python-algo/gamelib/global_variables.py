import json

DEBUG = True

STATIONARY_UNITS = ['FF', 'EF', 'DF']
ATK_UNITS = ['DF', 'PI', 'EI', 'SI']

string_config = """
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

config = json.loads(string_config)

UNIT_TYPE_TO_INDEX = {}
WALL = config["unitInformation"][0]["shorthand"]
UNIT_TYPE_TO_INDEX[WALL] = 0
SUPPORT = config["unitInformation"][1]["shorthand"]
UNIT_TYPE_TO_INDEX[SUPPORT] = 1
TURRET = config["unitInformation"][2]["shorthand"]
UNIT_TYPE_TO_INDEX[TURRET] = 2
SCOUT = config["unitInformation"][3]["shorthand"]
UNIT_TYPE_TO_INDEX[SCOUT] = 3
DEMOLISHER = config["unitInformation"][4]["shorthand"]
UNIT_TYPE_TO_INDEX[DEMOLISHER] = 4
INTERCEPTOR = config["unitInformation"][5]["shorthand"]
UNIT_TYPE_TO_INDEX[INTERCEPTOR] = 5
REMOVE = config["unitInformation"][6]["shorthand"]
UNIT_TYPE_TO_INDEX[REMOVE] = 6
UPGRADE = config["unitInformation"][7]["shorthand"]
UNIT_TYPE_TO_INDEX[UPGRADE] = 7

ALL_UNITS = [SCOUT, DEMOLISHER, INTERCEPTOR, WALL, SUPPORT, TURRET]
STRUCTURE_TYPES = [WALL, SUPPORT, TURRET]

ARENA_SIZE = 28
HALF_ARENA = int(ARENA_SIZE / 2)
MP = 1
SP = 0
