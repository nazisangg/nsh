from random import shuffle
import random
import math
class fermi(object):

    def __init__(self,population=[], F=5 , cost=1, M=1, strategyList=["random"]):
        self.__population = population
        self.__strategyDic = self.initStrategyDic(strategyList)
        #self.__player = Player(1)
        self.__action = 'C'
        self.__F = F
        self.__cost = cost
        self.__M = M
        self.__fitness = 0

    def initStrategyDic(self, strategyList):
        dic = {}
        for i in strategyList:
            dic[i]=0
        return dic
    
    def set_fitness(self,fitness):
        self.__fitness = fitness
        
    def set_action(self, nextAction):
        print('nextAction: ', nextAction)
        self.__action = nextAction

    def get_action(self):
        return self.__action
    
    def set_population(self,newPlayer):
        self.__player = newPlayer
        
    def set_population(self, newPopulation):
        self.__population = newPopulation
    def set_parameters(self, f,cost , m):
        self.__F = f
        self.__cost = cost
        self.__M = m
    def play_round(self):
        population = self.__population
        shuffle(population)
        popsize = len( population )		
        start = 0
        end = 0	
        i = 0
        while ( i < popsize ) :
            print( 'here here her')
            start = i
            end = start + 5
            group = population[start:end]
            self.play_ngame(group)
            i = i + 5

    def play_ngame(self, group) :
        groupsize = len(group)   
        cooperator_count = 0
    
        for i, player in enumerate(group) :
            print(i, player)
 #           player.get_strInstance().set_F(_F)
#            player.get_strInstance().set_cost(_cost)
#            player.get_strInstance().set_M(_M)
#            player.get_strInstance().set_groupSize(groupsize)
        
            if player.get_action() == 'C' :
                cooperator_count = cooperator_count + 1

        for player in group:
            player.get_strInstance().set_cooperatorCount(cooperator_count)
    #print('cooperator_count=', cooperator_count)
    
        F = self.__F       # if F > groupsize ---> all cooperators
        cost = self.__cost
    
        M = self.__M       # threshold for payoff
                # when M > 1 and  and k < M the situation is like N-Prisoner's dilemma
    
        sigma = 0
        delta_count = cooperator_count - M
    
        if delta_count < 0  :           # Heaviside function
            sigma = 0
        else :
            sigma = 1
    
    
        payD = ( cooperator_count * F / groupsize * cost) * sigma
    
        payC = payD - cost

        print('payC is : ',payC)
    
        for player in group :
            if player.get_action() == 'C' :
                player.set_reward( payC )
            else :
                player.set_reward( payD )

    def update_action_fermi(self,other, rand):
        #""" update action using fermi function """
        beta = 1    # beta --> 0 random/neutral  beta >> 1  reduces to a step function
        
        
        fitDelta = self.__fitness - other.get_fitness()

        prob = 1.0 / ( 1.0 + math.exp( -1 * beta * fitDelta ) )
    
        print('prob= ', prob)
        
        if( prob > rand ) :
        	other.set_action( self.get_action() )


    def random_example(self):
        population = self.__population
        popsize = len(population)
        for player in population:
            #self.play_round()
            # player.set_fitness(  player.get_reward() ) # player.get_fitness() +
            comp_index = random.randint(0,popsize-1)
            rand = random.random()
            self.update_action_fermi( population[comp_index], rand )

    def fb_example(self):
        population = self.__population
        for player in population:
            player.set_fitness(  player.get_reward()) 
            strategy = player.get_strategyType()
            self.__strategyDic[strategy] = self.__strategyDic[strategy] + 1
        stategy = "x"
        maxvalue=0
        for item in self.__strategyDic:
            if self.__strategyDic[item]>maxvalue:
                stategy = item
                maxvalue = self.__strategyDic[item]
                
    def ob_example(self):
        population = self.__population
        player = self.__player
        other = player
        maxReward = 0

        for player in population:
            if player.get_reward(self) > maxReward:
                maxReward = player.get_reward(self)
                other = player
        rand = random.random()
        player.update_action_fermi(other,rand)
                
