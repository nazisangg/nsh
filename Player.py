import math
import random
from Strategy import Strategy


class Player(object):
    
    
    """ Player class details """
    
    counter = 0         # used to count instances
    
    def __init__(self, playerNumber, action='C', reward=0.0, fitness=0.0, strategyType= 'random') :
        """ Create a new Player with action, reward, fitness """
        self.__action = action
        self.__strInstance = Strategy(playerNumber)
        self.__strInstance.set_strategyType(strategyType)
        self.__strInstance.set_currentAction(action)
        self.__reward = reward
        self.__rounds = 0
        self.__fitness = fitness
        self.__nextAction = None
        self.__strategyType = strategyType
        # while init, a temperoy next action will be generate.
        # it is not good for pupular one
        #self.set_nextAction()
        #self.__strategy = Strategy(strategyType, None)
        # set unique instance count (class variable used)
        type(self).counter += 1    
        self.__uniqueId =  type(self).counter
    
    def __str__(self) :
         """ toString() """
         return  str(self.__uniqueId) + ': (' + str(self.__action) + ',' \
         + str(self.__reward) + ',' + str(self.__fitness)  + ')'

    def get_strInstance(self):
        return self.__strInstance


    def set_nextAction(self):
        strategyType = self.get_strategyType()
        strategy = self.__strInstance
        #strategy.set_strategyType(strategyType)
        new_action =strategy.StrategyPick()
        #print('current action is:', self.__action)
        self.__nextAction = new_action
        #print('next action will be:', self.__nextAction)
        
    def get_nextAction(self):
        return self.__nextAction
    
    def set_strategyType(self, new_strategy):
        self.__strategyType = new_strategy
        self.__strInstance.set_strategyType(new_strategy)

    def get_strategyType(self):
        return self.__strategyType
    
    def set_fitness(self, new_fitness) :
        #self.__fitness = new_fitness
#        self.__fitness = self.__fitness + new_fitness
        try:
            self.__fitness = (self.__fitness + new_fitness)/self.__rounds
        except:
            self.__fitness = self.__fitness + new_fitness
        self.__strInstance.get_fermiInstance().set_fitness(self.__fitness)
        
    def get_fitness(self) :
        return self.__fitness
    def set_rounds(self, rounds):
        self.__rounds = rounds
         
    def set_reward(self, new_reward) :
        
        self.__reward = new_reward
        
    def get_reward(self) :
        return self.__reward
             
# Every time the play ground change the real action of player
# it needs to generate a new possiable next action for use 
    def set_action(self, new_action) :
        self.__action = new_action
        self.__strInstance.set_currentAction(new_action)
        self.set_nextAction()
        
    def get_action(self) :
        return self.__action
                          
    def update_action_fermi(self, other, rand) :
        #""" update action using fermi function """
        
        
        #print('in fermi')
        #print( self )
        #print( other )
        
        beta = 1    # beta --> 0 random/neutral  beta >> 1  reduces to a step function
        
        
        #self.set_fitness(1)
        #other.set_fitness(2)
        
        fitDelta = self.__fitness - other.__fitness
        #print(fitDelta)
        
        #eee = math.exp(1)
        #print(eee)
        
        prob = 1.0 / ( 1.0 + math.exp( -1 * beta * fitDelta ) )
    
        print('prob= ', prob)
        
        #rand = random.random()
        
        #print(rand)
        
        if( prob > rand ) :
        	other.set_action( self.get_action() )	

        #print('after update')
        #print( self )
        #print( other )
        
     
    


    @classmethod
    def PlayerInstances(cls) :
        return cls, Player.counter

'''
p=Player()
#print(Player().get_action())
#print(Player().get_strategyType())
p.set_nextAction()
i=0
while i<20:
    p.set_nextAction()
    print(p.get_nextAction())
    i=i+1

'''
