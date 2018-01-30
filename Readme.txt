testNPlayers.py:
########################################
This is the file that contains all running logic

Please run work.sh to start simulation

If you need to change parameters, please change them in work.sh
########## Parameters ##################
Possiable Strategies :
Random: random ;
Copy the most frequent action(with out wright fish): popular ;
Frequent base social learning: fpopular;
Never change action: obstinate;
Mixed with all methods: mix;
Qlearning:qlearning;
Qlearning with softmax: qlearning2
Reward base social learning: rewardModel
Fermi strategy: fermi

Run model: 
Run the game for 1 time with N rounds and particular strategy: st
Run multiple Strategies : mt
Run same stategies for several times : rm


######################################################

csvReader.py
######################################################
This is the file that calculate the average of csv data

you can directly run the file and type in parameters

########## Parameters ##################
Run model:
Calculate average: main1

filename: runmodel_strategy_population_groupsize