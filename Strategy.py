import random
from qlearningStrategy import qlearningStrategy
from fermi import fermi



class Strategy(object):
    '''
        The Strategy of user
    '''
    def __init__(self, playerNumber, strategyType = 'random', currentAction='C', nextAction= None, fraction = 0.5):
        ''' Create a strategy with different type'''
        self.__strategyType = strategyType
        self.__nextAction = nextAction
        self.__fraction = fraction
        self.__currentAction = currentAction
        self.__qlInstance = qlearningStrategy(playerNumber)
        self.__fermiInstance = fermi()
        self.__F = 5
        self.__cost = 1
        self.__M = 1
        self.__cooperatorCount = 0
        self.__groupSize = 0

    def set_groupSize(self, newSize):
        self._groupSize = newSize
    def set_cooperatorCount(self, newCount):
        self.__cooperatorCount = newCount
    def set_F(self,newF):
        self.__F = newF
        
    def set_cost(self,cost):
        self.__cost = cost
        
    def set_M(self, newM):
        self.__M = newM
    
    def get_qlInstance(self):
        return self.__qlInstance
    def get_fermiInstance(self):
        return self.__fermiInstance
    def set_currentAction(self, currentAction):
        if currentAction == 'C' or currentAction == 'D':
            self.__currentAction = currentAction
        else:
            print("your current action is not in correct format, your current action is: ", currentAction)

    def get_currentAction(self):
        return self.__currentAction
    
    def set_fraction(self, new_fraction):
        if new_fraction>=0 and new_fraction <=1:
            self.__fraction = new_fraction
        else:
            print('fraction is not in right format, temperory coorperate fraction is: ', self.__fraction)

    def get_fraction(self):
        return self.__fraction
    
    def set_nextAction(self,new_action):
        if new_action == 'C' or 'D':            
            self.__nextAction = new_action
        else:
            print("The action type is not apporperate")

    def get_nextAction(self):
        return self.__nextAction
    
    def set_strategyType(self, new_type):
        self.__strategyType = new_type

    def get_strategyType(self):
        return self.__strategyType

    def fermiStrategy(self):
        sigma = 0
        delta_count = self.__cooperatorCount - self.__M
        if delta_count < 0  :           # Heaviside function
            sigma = 0
        else :
            sigma = 1
        payD = ( self.cooperator_count * self.F / groupsize * self.cost) * sigma
    
        payC = payD - cost
            
    def randomStrategy(self):
        randomPick = random.random()
        if randomPick > 0.5:
            self.set_nextAction('C')
        elif randomPick < 0.5:
            self.set_nextAction( 'D')
        elif randomPick == 0.5:
            self.randomStrategy()

    def pupularFollower(self, fraction):
        rand = random.random()
        if fraction > 0.5:
            self.set_nextAction('C')
            if rand < 0.1:
                self.set_nextAction('D')
        elif fraction < 0.5:
            self.set_nextAction('D')
            if rand < 0.1:
                self.set_nextAction('C')
        elif fraction == 0.5:
            self.randomStrategy()
        #print(fraction,'lala',self.__nextAction)

    def obstinateStrategy(self, action):
        if action == 'C':
            self.set_nextAction('C')
        elif action == 'D':
            self.set_nextAction('D')
        else:
            print('No particular action selected, Default action will be C')

    def mix(self):
        strategy = random.choice(('random', 'popular', 'obstinate','qlearning'))
        print('strategy is: ',strategy)
        return strategy

    def rdExample(self):
        self.__fermiInstance.random_example()

    def fbExample(self):
        self.__fermiInstance.fb_example()

    def obExample(self):
        self.__fermiInstance.ob_example()
            
    def StrategyPick(self):
        strategyType = self.get_strategyType()
        if strategyType == 'random':
            #print('random jin qu la')
            self.randomStrategy()
        elif strategyType == 'popular':
            fraction = self.get_fraction()
            self.pupularFollower(fraction)
        elif strategyType == 'obstinate':
            currentAction = self.get_currentAction()
            self.obstinateStrategy(currentAction)
        elif strategyType == 'mix':
            newStrategy = self.mix()
            #print('here')
            self.set_strategyType(newStrategy)
            self.StrategyPick()
        elif strategyType == 'qlearning':
            self.set_nextAction(self.__qlInstance.choose_action())
            #self.__qlInstance.update_reward()
        elif strategyType == 'qlearning2':
            self.set_nextAction(self.__qlInstance.choose_action2())
        elif strategyType == 'fermi':
            print("strategy fermi is in")
        elif strategyType == "rdexample":
            self.rdExample()
            self.set_nextAction(self.__fermiInstance.get_action())
        elif strategyType == 'fbexample':
            self.fbExample()
            self.set_nextAction(self.__fermiInstance.get_action())
        elif strategyType == 'obexample':
            self.obExample()
            self.set_nextAction(self.__fermiInstance.get_action())
        else:
            #print('no Particular strategt is matched, random strategy will defaultly applied: ', strategyType)
            self.randomStrategy()
        nextAction = self.get_nextAction()
        #print('nextacttion is :', nextAction)
        return nextAction

#print(Strategy().get_nextAction())
'''
if __name__ == "__main__":
    s = Strategy()
    s.set_strategyType('mix')
    s.set_fraction(0.4)
    s.set_currentAction('C')
    i=0
    while i<=20:
        print(s.StrategyPick())
        i=i+1
'''
