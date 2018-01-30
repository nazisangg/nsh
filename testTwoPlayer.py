from Player import Player
from random import shuffle
import random
import matplotlib.pyplot as plt


	
"""
	init the population
"""
		
def init_population(population, cooperators, defectors):	
	
	for r in range(0,40) :
	
		if ( random.random() <= 0.5 ) :
			action = 'C'
		else :
			action = 'D'
		
		player = Player(action,0,0)
		population.append(player)
	
	#print('display init population')
	
	cooperator_count = 0
	defector_count = 0
	
	for player in population :
		#print( player)
		
		if player.get_action() == 'C' :
			cooperator_count = cooperator_count + 1
		else :
			defector_count = defector_count + 1	
			
	#print( cooperator_count / len(population) )
	#print( defector_count / len(population) )
	
	cooperators.append( cooperator_count / len(population) )
	defectors.append( defector_count / len(population) )
	

"""
    the actual game
"""

def play_2game(player1, player2) :
    #print( 'in play_game' )
    
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
	
	#print('after shuffle of population')
	
	#for player in population :
	#	print( player )
	
	#print('now playing a round of the game')
	
	popsize = len( population )
	#print( popsize )
			
	i = 0
	while ( i < popsize ) :
	    #print( i )
	    #print( population[i] )
	    #print( population[i+1] )
	    play_2game( population[i], population[i+1] )
	    i = i + 2

"""
	reproduction phase
"""

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
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1.0)
    plt.show()
	  
    
    
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
	    update_population(population, cooperators, defectors)
	
	#print( rounds )
	#print( cooperators )
	#print( defectors )
	
	for player in population :
		print( player)
		
	stat_plots(rounds, cooperators) 
	
	

	
main()


