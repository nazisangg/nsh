from Player import Player
from random import shuffle
import random
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys
import math
import time
import csv
import os


	
"""
	init the population
"""

_time=str(time.strftime('%Y-%m-%d_%H:%M:%S',time.localtime(time.time())))
print(_time)
print("Please type in the testing model: st(singleTest), mt(muitipleTest), rm(rewardModel)")
_models = sys.argv[1]
print("Please type in the strategy you would line to follow:")
print("Strategy you can choose: random, popular, fpopular, obstinate, mix，qlearning,rdexample,fbexample,obexample,rewardModel")
_strategy = sys.argv[2]
_popularperson = 0 
if _strategy == "fpopular" or _strategy == "rewardModel":
    print("please type in the number of player that will copy other strategies in each round")
_popularperson = int(sys.argv[3])
print("How many player will be in the game")
_playerNumber = int(sys.argv[4])
_fraction = 0
print("Please type in the group Limitation(F): ")
_F = int(sys.argv[5])
print("Please type in the Cost(cost): ")
_cost = int(sys.argv[6])
print("Please type in the pay-off threadhold(m)")
_M = int(sys.argv[7])
print("Please type in the size of group(N): ")
_N = int(sys.argv[8])
print("Please type in the running time:")
_runningTime = int(sys.argv[9])
print("Please type in the round of game:")
_gameround = int(sys.argv[10])


'''
    Input: strategyType, player Number, Population list
    Output: Population List[Player.players], cooperators[fraction.C], detectors[fraction.D].
'''
class game(object):
    def __init__(self, strategy, playerNumber, population, initSR= 5, initHR=4):
        self.__strategy = strategy
        self.__playerNumber = playerNumber
        self.__population = population
        self.__cooperators = []
        self.__defectors = []
        self.__lst = []
        self.__avReward = 0

    def set_strategy(self, newStrategy):
        self.__strategy = newStrategy
        
    def reset_cooperators(self):
        a= self.__cooperators[0]
        print (a)
        self.__cooperators =[a]

    def get_cooperators(self):
        return self.__cooperators

    def reset_defectors(self):
        a = self.__defectors[0]
        self.__defectors =[a]
        
    def get_defectors(self):
        return self.__defectors

    def get_population(self):
        return self.__population

    def csvDataBuilder(self,cooperator,rounds):
        lst = self.__lst
        lste = [cooperator[rounds],self.__avReward]
        lst.append(lste)

    def get_lst(self):
        return self.__lst

    def reset_lst(self):
        m = self.__lst[0]
        self.__lst = [m]

# calculate the average reward of each round.
    def average_reward(self):
        population = self.__population
        popsize = len(population)
        totalreward = 0
        for player in population:
            totalreward = totalreward + player.get_reward()
        self.__avReward = totalreward/popsize
# Used when multiple simulation is required
    def reuse_population(self):
        population = self.__population
        strategy = self.__strategy
        self.reset_cooperators()
        self.reset_defectors()
        for player in population:
            player.set_nextAction()
        
    def init_population(self):
        population = []
        cooperators = self.__cooperators
        defectors = self.__defectors
        _cooperator_count = 0
        _defector_count = 0
        for r in range(0,_playerNumber) :
            if ( random.random() <= 0.5 ) :
                startAction = 'C'
                _cooperator_count = _cooperator_count + 1	
            else :                                
                startAction = 'D'
                _defector_count = _defector_count + 1
    		
            player = Player(_playerNumber,startAction,0,0,_strategy)
            population.append(player)
            _fraction = (_cooperator_count / len(population))
            self.__population = population
        self.play_round(population,_N)

# set all nessary parameters to the player/strategy/qllearning class
        for player in population:
            player.get_strInstance().set_fraction(_fraction)
            player.get_strInstance().get_qlInstance().set_currentC(_cooperator_count)
            player.get_strInstance().get_fermiInstance().set_population(population)
            player.set_nextAction()
        cooperators.append( _cooperator_count / len(population) )        
        defectors.append( _defector_count / len(population) )
        self.average_reward()
        self.__lst.append([cooperators[0],self.__avReward])

# Calculate the reward of players in different groups
    def play_ngame(self, group) :
        groupsize = len(group)
        cooperator_count = 0
        for i, player in enumerate(group) :
            player.get_strInstance().set_F(_F)
            player.get_strInstance().set_cost(_cost)
            player.get_strInstance().set_M(_M)
            player.get_strInstance().set_groupSize(groupsize)
            if player.get_action() == 'C' :
                cooperator_count = cooperator_count + 1
        for player in group:
            player.get_strInstance().set_cooperatorCount(cooperator_count)
        F = _F       # if F > groupsize ---> all cooperators
        cost = _cost
    
        M = _M       # threshold for payoff
                # when M > 1 and  and k < M the situation is like N-Prisoner's dilemma
    
        sigma = 0
        delta_count = cooperator_count - M
    
        if delta_count < 0  :           # Heaviside function
            sigma = 0
        else :
            sigma = 1
    
    
        payD = ( cooperator_count * F / groupsize * cost) * sigma
    
        payC = payD - cost
        for player in group :
            if player.get_action() == 'C' :
                player.set_reward( payC )
            else :
                player.set_reward( payD )

# Randomly ditribute players into different groups
    def play_round(self,population,groupsize):

        shuffle(population)
        popsize = len( population )
		
        start = 0
        end = 0	
        i = 0
        while ( i < popsize ) :
            start = i
            end = start + groupsize
            group = population[start:end]
            self.play_ngame(group)
            i = i + groupsize

    def randomList(self,number,popsize):
        lst = []
        while len(lst)!=number:
            i = random.randint(0,popsize-1)
            if i not in lst:
                lst.append(i)
        return lst

    def inverse_action(self,action):
        act = None
        if action == 'C':
            act = 'D'
        else:
            act = 'C'
        return act 
        
    def yinong_update_population(self,rounds):
        population=self.__population
        cooperators=self.__cooperators
        defectors= self.__defectors
        popsize = len(population)
        if self.__strategy == "fermi":
            #print("here is fermi")
            update_population(population, cooperators, defectors)
        elif self.__strategy == "rewardModel":
            players = None
            fitness = 0
            for player in population:
                #print("lalalal",player.get_fitness())
                if player.get_reward() >= fitness:
                    #print(player.get_fitness())
                    fitness= player.get_reward()
                    players = player
            lst = self.randomList(_popularperson,popsize)
            i = 0
            while i<len(population):
                player = population[i]
                x = 0
                y = 0
                if i in lst:
                    rand = random.random()
                    action = players.get_action()
                    if action == "D" and players.get_reward() == 4.0:
                        x=x+1
                        print (x)
                    elif action == 'C':
                        y = y + 1
                        print (y)
                    inverseAction = self.inverse_action(players.get_action())
                    if rand < 0.1:
                        player.set_action(action)
                    else:
                        player.set_action(inverseAction)
                i=i+1
        elif _strategy == 'fpopular':# generate differnt lst every round
            # and fix the other startegy into one
            lst = self.randomList(_popularperson,popsize)
            i = 0
            while i<len(population):
                player = population[i]
                if i in lst:
                    player.set_strategyType('popular')
                    #player.set_nextAction()
                    player.set_action(player.get_nextAction())
                    #print('here')
                else:
                    player.set_strategyType('obstinate')
                    #player.set_nextAction()
                    player.set_action(player.get_nextAction())
                i=i+1
            i = 0
            #print(i,"1",_strategy)
        else:
            popsize = len(population)
            for player in population :
                #print(population)
    		#print( player )
                player.set_fitness(  player.get_reward() )
                player.set_rounds(rounds)
                if _strategy == 'qlearning' or _strategy == 'qlearning2':
                        #print("newreward is ",player.get_reward())
                        player.get_strInstance().get_qlInstance().set_newReward(player.get_reward())
                        player.get_strInstance().get_qlInstance().update_reward()
                player.set_action(player.get_nextAction())
        cooperator_count = 0
        defector_count = 0
    		
        for player in population :
    		#print( player )	
            if player.get_action() == 'C' :
                cooperator_count = cooperator_count + 1
            else :
                defector_count = defector_count + 1	
        fractions = cooperator_count/len(population)
        for player in population:
            #print(_fraction)
            player.get_strInstance().set_fraction(fractions)
            player.get_strInstance().get_qlInstance().set_currentC(cooperator_count)
            act = player.get_action()
            if act == 'C':                    
                stateName = player.get_action()+'_'+ str(cooperator_count-1) + 'C_' + str(len(population)-cooperator_count)+'D'
            elif act == 'D':
                stateName = player.get_action()+'_'+ str(cooperator_count) + 'C_' + str(len(population)-cooperator_count-1)+'D'
            player.get_strInstance().get_qlInstance().set_state(stateName)
            player.set_nextAction()
            if _strategy == 'fpopular':
                player.set_strategyType('fpopular')
        #print('2',_strategy)
    	
            #print(population)
        cooperators.append( cooperator_count / len(population) )
        defectors.append( defector_count / len(population) )
            
	

######## Strat of main function and plot #########


# implement of fermi function
def update_population(population, cooperators, defectors) :
	popsize = len(population)
	for player in population :
		#print( player )
		player.set_fitness(  player.get_reward() ) # player.get_fitness() +
		#print( player )
		comp_index = random.randint(0,popsize-1)
		rand = random.random()
		player.update_action_fermi( population[comp_index], rand )
	cooperator_count = 0
	defector_count = 0
	for player in population :
		if player.get_action() == 'C' :
			cooperator_count = cooperator_count + 1
		else :
			defector_count = defector_count + 1
	cooperators.append( cooperator_count / len(population) )
	defectors.append( defector_count / len(population) )


# Class of Save files in CSV automaticly
class fileSaver(object):
    def __init__(self,txt):
        self.__time = str(time.strftime('%Y-%m-%d_%H-%M-%S',time.localtime(time.time())))
        s1 = os.getcwd()
        s2 = '/csv/real/'
        self.__filename = s1+s2+txt+'_'+ str(_N) + '_' + str(_gameround) + '.csv'
        with open(self.__filename, 'w') as f:
            f_csv=csv.writer(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
            f_csv.writerow(['Cooperate Rate', 'Average Reward'])
    
    def fileSaving(self, data):
        filename = self.__filename
        i = 0
        with open(filename, 'a') as f:
            f_csv=csv.writer(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
            for line in data:
                f_csv.writerow(line)

def stat_plots(rounds, cooperators) :
    plt.plot(rounds, cooperators, linewidth=1.0)
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1.0)
    s1 = os.getcwd()
    s2 = '/result/'
    txt = _models+'_'+_strategy +'_'+ str(_playerNumber) +'_'+ str([_F,_cost,_M,_N])+'_'+str(_gameround)
    filename = s1+s2+txt+'_'+_time+'.png'
    plt.savefig(filename)
    #plt.show()
	  
def stat_plots2(rounds, cooperators,strategy) :
    plt.plot(rounds, cooperators, linewidth=1.0, label = "groupszie" + str(strategy))
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1.0)  

def threeD_plot(rounds,cooperators, para):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_ylabel('Time')
    ax.set_zlabel('% Cooperators')
    ax.set_xlabel('para')
    plt.plot(para, rounds, cooperators, marker="o", linewidth=1.0)
    plt.show()

"""
    main function
"""
def totalRoundBuilder(runningtimes):
    totalRound=[]
    while runningtimes > 0:
        totalRound.append(0)
        runningtimes = runningtimes-1
    print(totalRound, len(totalRound))
    return totalRound
#totalRoundBuilder(10)

def markerBuilder(runningtimes):
    totalRound=[]
    while runningtimes > 0:
        totalRound.append([])
        runningtimes = runningtimes-1
    print(totalRound, len(totalRound))
    return totalRound


# Funtion of run same strategy for multiple time
def multiTimeRunner(runningtimes):
    random.seed()
    rounds = []
    totalRound = totalRoundBuilder(5)
    markerList = markerBuilder(5)
    population = []
    gameslist = []
    i=0
    divider = runningtimes
    fileName = _models + '_' + str(_playerNumber)+'_'+ str([_F,_cost,_M,_N,_runningTime])
    saver = fileSaver(fileName)
    i = 0
    while runningtimes > 0:
        saver.fileSaving([['round: '+str(runningtimes),0]])
        if i == 0:
            games = game(_strategy,_playerNumber,population)
            gameslist.append(games)
            games.init_population()
            rounds.append(0)
        else:
            games.reset_cooperators()
            games.reset_defectors()
            games.reset_lst()
            rounds =[0]
        for roundx in range(1,5) :
            games.play_round(population,_N)
            rounds.append( roundx )
            games.yinong_update_population(roundx)
            cooperators = games.get_cooperators()
            games.average_reward()
            games.csvDataBuilder(cooperators,roundx)
        runningtimes = runningtimes-1
        i=i+1
        cooperators = games.get_cooperators()
        for n, i in enumerate(totalRound):
                totalRound[n]=i+cooperators[n]
                markerList[n].append(cooperators[n])
        saver.fileSaving(games.get_lst())
    for n, i in enumerate(totalRound):
        totalRound[n]= i / divider
    for n,i in enumerate(markerList):
        plt.annotate(listConverter(i), xy=(rounds[n],totalRound[n]),
                     xytext = (rounds[n]-0.3,totalRound[n]+0.05), arrowprops=dict(facecolor='black', shrink=0.01))
    stat_plots(rounds, totalRound)


def listConverter(lst):
    strings = 'The list is: '
    for i in lst:
        strings = strings + ','+str(i)
    return strings

#
def multipleprintout(strategyList):
    strategyList = [2,3,4,5,6,7,8,9]
    strategy = "rewardModel"
    random.seed()
    rounds = []
    population = []
    i=0
    #games = game(_strategy,_playerNumber,population)
    fileName = _models + '_' + str(_playerNumber)+'_'+ str(strategyList)
    saver = fileSaver(fileName)
    for k in strategyList:
        random.seed()
        rounds = []
        txt = _models + '_' + str(_playerNumber) + '_' + _strategy
        saver = fileSaver(txt)
        population = []
        games = game(_strategy, _playerNumber, population)
        games.init_population()
        population = games.get_population()
        rounds.append(0)
        """
        play_round(population)

        update_population(population)
        """

        for roundx in range(1, 500):
            # print( 'round' , roundx )
            games.play_round(population,k)
            rounds.append(roundx)
            games.yinong_update_population(roundx)
            cooperators = games.get_cooperators()
            games.average_reward()
            games.csvDataBuilder(cooperators, roundx)
        cooperators = games.get_cooperators()
        saver.fileSaving(games.get_lst())
        print(cooperators[2],cooperators[499])
        stat_plots2(rounds, cooperators, k)
        i=i+1
    plt.legend()
    plt.show()

'''
    This is the funtion that test one particular strategy,  save plot CSV automaticly
'''
def main():
    
	random.seed()
	rounds = []
	txt = _models + '_' + str(_playerNumber)+'_'+ _strategy
	saver = fileSaver(txt)
	population = []
	games = game(_strategy,_playerNumber,population)
	games.init_population()
	population = games.get_population()
	rounds.append(0)
	for roundx in range(1,500) :
	    #print( 'round' , roundx )
	    games.play_round(population,_N)
	    rounds.append( roundx )
	    games.yinong_update_population(roundx)
	    cooperators = games.get_cooperators()
	    games.average_reward()
	    games.csvDataBuilder(cooperators,roundx)
	cooperators = games.get_cooperators()
	saver.fileSaving(games.get_lst())
	stat_plots(rounds, cooperators)

	

def play_2game(player1, player2) :
    #print( 'in play_2game' )
    
    payR = 1.0
    payT = 0.5
    payS = -0.5
    payP = 0
    
    """
    # Stag Hunt Rewards   R > T > P > S
    
     
    payR = 3.0
    payT = 1.0
    payS = 0.0
    payP = 1.0
    """
    
    """
    # Prisoner's Dilemma Rewards   T > R > P > S
    
    payR = 3.0
    payT = 4.0
    payS = 0.0
    payP = 1.0

    """
    
    #print(player1)
    #print(player1.get_action() )
    #print(player2)
    #print(player2.get_action() )
        
    if player1.get_action() == 'C' :
        if player2.get_action() == 'C' :
            #print('CC')
            player1.set_reward( payR )
            player2.set_reward( payR )
        else :
            #print('CD')   
            player1.set_reward( payS )
            player2.set_reward( payT )
    else :
        if player2.get_action() == 'D' :
            #print('DC')
            player1.set_reward( payT )
            player2.set_reward( payS )
        else :
            #print('DD')
            player1.set_reward( payP )
            player2.set_reward( payP )
            
            
		
#main()
#multipleprintout(['random','popular'])
#multiTimeRunner(2)
'''
    Main Function    
'''

if __name__ == '__main__':
    if _models == 'st':
        main()
    elif _models == 'mt':
        multipleprintout(['random','popular'])
    elif _models == 'rm':
        multiTimeRunner(_runningTime)
    elif _models == 'test':
        pass
    

