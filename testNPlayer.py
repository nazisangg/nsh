from Player import Player
from random import shuffle
import random
import matplotlib.pyplot as plt
import sys
import math
import time


	
"""
	init the population
"""
_time=str(time.strftime('%Y-%m-%d',time.localtime(time.time())))

print("Please type in the strategy you would line to follow:")
print("Strategy you can choose: random, popular, obstinate, mix，qlearning")
_strategy = sys.stdin.readline().strip('\n')
print("How many player will be in the game")
_playerNumber = int(sys.stdin.readline())
_filename = _strategy+'_'+str(_playerNumber)+'_'+_time+'.csv'
print(_filename)
_fraction = 0
'''
print("Please type in the reward of Hare")
_hareReward = int(sys.stdin.readline())
print("Please type in the reward of Stag")
_stagReward = int(sys.stdin.readline())
'''
		
def init_population(population, cooperators, defectors):
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
# set all nessary parameters to the player/strategy/qllearning class
    for player in population:
        player.get_strInstance().set_fraction(_fraction)
        player.get_strInstance().get_qlInstance().set_currentC(_cooperator_count)
        player.set_nextAction()
##################################################################                
    cooperators.append( _cooperator_count / len(population) )        
    defectors.append( _defector_count / len(population) )
	


def play_ngame(group) :
    #print( 'in play_ngame' )
    
    groupsize = len(group)
    #print('groupsize= ', groupsize)
    #print('')
    
    cooperator_count = 0
    
    for i, player in enumerate(group) :
        print(i, player)
        
        if player.get_action() == 'C' :
            cooperator_count = cooperator_count + 1
            
    #print('cooperator_count=', cooperator_count)
    
    F = 5       # if F > groupsize ---> all cooperators
    cost = 1
    
    M = 1       # threshold for payoff
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
    
    
    
"""
    the actual 2 player game
"""

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
            
            
	
"""
	playing a round of the game
"""

def play_round(population) :

	shuffle(population)

	# randomly combat the population list
	
	#print('after shuffle of population')
	
	#for player in population :
	#	print( player )
	
	#print('now playing a round of the game')
	
	popsize = len( population )
	#print( popsize )
		
	start = 0
	end = 0	
	i = 0
	while ( i < popsize ) :
	    #print( i )
	    #print( population[i] )
	    #print( population[i+1] )
	    
	    start = i
	    end = start + 5
	    
	    group = population[start:end]
	    play_ngame( group )
	    
	    i = i + 5

"""
	reproduction phase
"""


def yinong_update_population(population,cooperators,defectors):
        	
	#print('updating fitness values')
	
    popsize = len(population)
    
    for player in population :
		#print( player )
        player.set_fitness(  player.get_reward() )
        if _strategy == 'qlearning':
                player.get_strInstance().get_qlInstance().set_newReward(player.get_reward())
                player.get_strInstance().get_qlInstance().update_reward()
		# player.get_fitness() +
		#print( player )
        comp_index = random.randint(0,popsize-1)
        rand = random.random()
        other = population[comp_index]
        beta = 1
        fitDelta = player.get_fitness() - other.get_fitness()
        prob = 1.0 / ( 1.0 + math.exp( -1 * beta * fitDelta ) )
        print('prob= ', prob)                       
        if( prob > rand ) :
            other.set_action( other.get_nextAction() )

    cooperator_count = 0
    defector_count = 0
		
    for player in population :
		#print( player )	
        if player.get_action() == 'C' :
            cooperator_count = cooperator_count + 1
        else :
            defector_count = defector_count + 1	
			
	#print( cooperator_count / len(population) )
	#print( defector_count / len(population) )
	
    for player in population:
        player.get_strInstance().set_fraction(_fraction)
        player.get_strInstance().get_qlInstance().set_currentC(cooperator_count)
        player.set_nextAction()
	
    cooperators.append( cooperator_count / len(population) )
    defectors.append( defector_count / len(population) )
	

        


def update_population(population, cooperators, defectors) :
	
	#print('updating fitness values')
	
	popsize = len(population)
    
	for player in population :
		#print( player )
		player.set_fitness(  player.get_reward() ) # player.get_fitness() +
		#print( player )
		comp_index = random.randint(0,popsize-1)
		rand = random.random()
		player.update_action_fermi( population[comp_index], rand )
	
	
	#print('new population details')
	
	cooperator_count = 0
	defector_count = 0
		
	for player in population :
		#print( player )
			
		if player.get_action() == 'C' :
			cooperator_count = cooperator_count + 1
		else :
			defector_count = defector_count + 1	
			
	#print( cooperator_count / len(population) )
	#print( defector_count / len(population) )
	
	cooperators.append( cooperator_count / len(population) )
	defectors.append( defector_count / len(population) )
	

def stat_plots(rounds, cooperators) :
    plt.plot(rounds, cooperators, marker="o", linewidth=1.0)
#    plt.plot(rounds,defectors,marker= "ro", linewidth=1.0))
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1.0)
    plt.show()

def stat_plots1(rounds, cooperators) :
    plt.plot(rounds, cooperators, marker="o", linewidth=1.0)
#    plt.plot(rounds,defectors,marker= "ro", linewidth=1.0))
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1.0)
#    plt.show()
    
def stat_plots2(rounds, cooperators,defectors) :
    plt.plot(rounds, cooperators, marker="o", linewidth=1.0)
    plt.plot(rounds,defectors,marker="o", linewidth=1.0)
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1.0)
#    plt.show()
	  
    
    
"""
    main function
"""

def main():
    
	random.seed()
	
	rounds = []
	cooperators = []
	defectors = []
	
	population = []
	
	init_population(population, cooperators, defectors)
	rounds.append(0)
	"""
	play_round(population)
	
	update_population(population)
	"""
	
	for round in range(1,20) :
	    print( 'round' , round )
	    play_round(population)
	    rounds.append( round )
	    yinong_update_population(population,cooperators,defectors)
	    #update_population(population, cooperators, defectors)
	
	#print( rounds )
	#print( cooperators )
	#print( defectors )
	
	for player in population :
		print( player)
		
	#stat_plots(rounds, cooperators)
	stat_plots1(rounds, cooperators)
	stat_plots1(rounds, defectors)
	plt.show()
	
	

	
main()


