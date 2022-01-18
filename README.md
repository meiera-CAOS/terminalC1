# C1 Terminal Live Fall 2021 Europe Regional
This repository contains the C1GamesStarterKit skeleton and additional / modified code written for the C1 Terminal Live Fall 2021 Regional tournament by Steven Batillana and Adrian Meier. The competition spanned one week end of November 2021. The commits between the 24-29. Nov. 2021 represent our efforts, while earlier commits are related to the provided code skeleton. The files we worked on are located in the python_algo folder. The readme describing the code skeleton starts below from 'C1GamesStarterKit'.

## Problem statement
Terminal Live is an Al programming competition featuring over 30,000 of the world’s best engineers and data scientists. The Fall 2021 Terminal Live season included virtual events for hundreds of students at the most prestigious universities in the US, Canada, Europe and Asia. At each competition, teams coded algorithms for a tower defense-style strategy game, and competed head-to-head in a single-elimination tournament.

## Strategic approach
The most straightforward way to compete, is to hardcode a strategy: Use the resources to position stationary and mobile units. Once the stategy is uploaded, it starts playing games versus other strategies. Those games can be reviewed, and the algorithm is given a matchmaking rating. Thus one could iteratively improve the code and add conditions to decide between different (hardcoded) strategies.


We did not go this route. Instead we aimed at programming a general strategy, which would be able to adapt to the gamestate and thus to the opponents strategy. To achieve this, we planned to build a min-max algorithm: From a given gamestate, evaluate all (or a representative subset) of possible turns. For every outcome of turns, analyze the gamestate based on an objective function. The objective function should rate the gamestate based on which player is favored. A high score would represent a big advantage for our algorithm, a score close to zero an even game, and a negative score would indicate a disadvantaged position. The min-max Algorithm analyzed the two players turns sequentially. The opponent picks the turn which minimizes the score (maximizing their advantage), then we pick the turn maximizing our advantage. This can be calculated to a certain depth, where reaching some termination criteria we choose the line of play which leads to the best (longterm) outcome. Such an algorithm works well as a simple chess computer. There the players play sequentially. During their turns they move one of their figures with one of the corresponding legal moves.

One challenge proved to translate the min-max algorithm to the towerdefense setting. For one, both players decide on their next moves simultaneously. To optimize your own turn you have to anticipate the opponents turn (this information is hidden). Additionally, the set of possible turns is rather big. It corresponds to all possible combinations of spending (some of) the two resources, and possible positions those units can be placed. In extreme cases, even the order in which the units are placed may affect the outcome of a round due to tiebreaker rules in unit targeting. And finally the outcomes of the turns are not trivial to deduce. 

### min-max for simultaneous turns
To handle simultaneous play (and not knowing what the opponents next move would be) we thought to calculate a sequence of best response turns. We would start with player1 having a turn with no actions, and calculate the best turn for player2. Then calculate the best response for player1 to player2's previous optimum. Ideally, repeting this would lead to the objective function to converge. Then we would have found a local optimum / equilibrium, which would represent a set of turns which are robust against what the opposing player may play (and therefore a good strategic choice).

### Simulation
To calculate the outcome of any combination of the two players turns, we needed to simulate the game engine. This entailed a careful study of the rules and doing some reverse-engineering. While we finished the simulation before the end of the competition, we underestimated the necessary effort. The code for the simulation can be found in the file we added at python-algorithm/gamelib/simulation.py. To ensure correctness we coded the simulation with a test driven approach, the corresponding tests are at python-algorithm/test_simulation.py.

### Objective function
The choice of objective function can be seen as a parameter which influences how well the algorithm would perform. One needs to identify which metric best represents advantage. We choose a simple first function for each player of: a * life_total + b * structure_points, c * mobile_points + d * structure_score, where a,b,c,d are weights, life_total, mobile_points and structure_points are game resources and structure_score would be a score computed of the built structures in relation to their health. Once the other pieces of the algorithm would work, we wanted to finetune this function. For example we thought about using a logarithmic function weight for the health as the last health (from 1 to 0) decides if we win or lose while the difference from 29 to 30 health is maybe negligible. The objective function get_score() can be found at python-algorithm/gamelib/helper.py.

### Calculating possible combinations of turns
We started writing some functions to enumerate all possible combinations of legal turns. Those functions (combination_generator) can be found at python-algorithm/gamelib/helper.py. However, it quickly became apparent that we would never be able to bruteforce all combination within the 5seconds planning time for every round. 
- First, instead of calculating all combination we would calculate a randomized subset of combinations. This way reducing the complexity but keeping a broad range of options.
- Second, split the structure resources into two pools. The first pool represents budget which is allocated to build our main structure setup (follows a hardcoded blueprint). Finding this blueprint would be something to learn from repeated play and analyzing opponents strategies. The second pool would be budget for which we calculate the adaptive structure placement based on min-max.
- Third, instead of evaluating arbitrary combinations of turns build a set of strategies and evaluate which strategy scores best. The set of strategies could look something like [defense1, defense2, defense3, attack_structures1, ..., score1, attempt_win]. Where each of those names represents a hardcoded plan which is then adapted to the available resources and gamestate.

## Conclusion
Given the limited time frame, we were too ambitious with our general approach. Unfortunately, we didn't manage to submit a strategy taking advantage of our simulation and min-max approach within time. In hindsight starting to play the game and building a hardcoded strategy upon which to improve is advisable. This way at least we would have a product ready to submit at any moment. For similar competitions with a longer time horizon however, adaptive strategies should prevail. It's improbably for a hardcoded strategy to manage many different gamestates well. We took the risk to attempt such a solution with the little time we had, and while we didn't win, we enjoyed the teamwork and the challenge!
___
# C1GamesStarterKit

Welcome to the C1 Terminal Starter Kit! The repository contains a collection of scripts and 
language-specific starter algos, to help you start your journey to develop the ultimate algo.

For more details about competitions and the game itself please check out our
[main site](https://terminal.c1games.com/rules).

## Manual Play

We recommend you familiarize yourself with the game and its strategic elements, by playing manually,
before you start your algo. Check out [the playground](https://terminal.c1games.com/playground).

## Algo Development

To test your algo locally, you should use the test_algo_[OS] scripts in the scripts folder. Details on its use is documented in the README.md file in the scripts folder.

For programming documentation of language specific algos, see each language specific README.
For documentation of the game-config or the json format the engine uses to communicate the current game state, see json-docs.html

For advanced users you can install java and run the game engine locally. Java 10 or above is required: [Java Development Kit 10 or above](http://www.oracle.com/technetwork/java/javase/downloads/jdk10-downloads-4416644.html).

All code provided in the starterkit is meant to be used as a starting point, and can be overwritten completely by more advanced players to improve performance or provide additional utility.

## Windows Setup

If you are running Windows, you will need Windows PowerShell installed. This comes pre-installed on Windows 10.
Some windows users might need to run the following PowerShell commands in adminstrator mode (right-click the 
PowerShell icon, and click "run as administrator"):
    
    `Set-ExecutionPolicy Unrestricted`
    
If this doesn't work try this:
    
    `Set-ExecutionPolicy Unrestricted CurrentUser`
    
If that still doesn't work, try these below:
    
    `Set-ExecutionPolicy Bypass`
    `Set-ExecutionPolicy RemoteSigned`
    
And don't forget to run the PowerShell as admin.

## Uploading Algos

Simply select the folder of your algo when prompted on the [Terminal](https://terminal.c1games.com) website. Make sure to select the specific language folder such as "python-algo" do not select the entire starterkit itself.

## Troubleshooting

For detailed troubleshooting help related to both website problems and local development check out [the troubleshooting section](https://terminal.c1games.com/rules#Troubleshooting).

#### Python Requirements

Python algos require Python 3 to run. If you are running Unix (Mac OS or Linux), the command `python3` must run on 
Bash or Terminal. If you are running Windows, the command `py -3` must run on PowerShell.
   
#### Java Requirements

Java algos require the Java Development Kit. Java algos also require [Gradle]
(https://gradle.org/install/) for compilation.
   
## Running Algos

To run your algo locally or on our servers, or to enroll your algo in a competition, please see the [documentation 
for the Terminal command line interface in the scripts directory](https://github.com/correlation-one/AIGamesStarterKit/tree/master/scripts)
