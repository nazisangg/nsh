import numpy as np
import pandas as pd
import time
import json
import os
import csv
import math
class qlearningStrategy(object):
    
    def __init__(self, playerNumber):
        self.__lastState = None
        self.__nextAction = None
        self.__currentAction = 'C'
        self.__lastAction = 'C'
        self.__playerNumber = playerNumber
        self.__fraction = 0.5
        self.__lastReward = 0
        self.__newReward = 0
        self.__currentC = 0
        self.__state = self.__currentAction + '_' +str(self.__currentC) + 'C_'+str(self.__playerNumber-1-self.__currentC) + 'D' 
        self.__N_STATES =2**playerNumber
        self.__ACTIONS = ['C', 'D']
        self.__EPSILON = 0.9
        self.__GAMMA = 0.9
        self.__ALPHA = 0.1
        self.__LAMBDA =0.9
        self.__table = self.build_q_table()
        self.__filename= 'nsh'+ str(playerNumber) + 'csv'
        self.__dataFrame = None
        #MAX_EPISODES =13
        #FRESH_TIME = 0.3

        
    def set_newReward(self, newReward):
        self.__newReward = newReward

    def set_lastReward(self, newReward):
        self.__lastReward = newReward

    def set_lastAction(self,newAction):
        self.__lastAction = newAction

    def set_currentC(self, newC):
        self.__currentC = newC
        
    def set_state(self,state):
        self.__state = state
    
    def set_currentAction(self, new_action):
        self.__currentAction = new_action
        
    def get_currentAction(self):
        return self.__currentAction
    
    def set_nextAction(self, new_action):
        self.__nextAction = new_action
        
    def get_nextAction(self):
        return self.__nextAction

    def set_fraction(self, new_fraction):
        self.__fraction = new_fraction

    def get_fraction(self):
        return self.__fraction
    
        
    def json_builder(self):
        try:
            for line in open(self.__filename, encoding="UTF-8"):
                print("zhi zhang")
        except FileNotFoundError:
            with open(self.__filename, 'w') as f:
                json.dump(self.table, f)
            


    def build_q_table(self):
        playerNumber = self.__playerNumber
        actions = self.__ACTIONS
        lst = []
        actions= actions
        table = pd.DataFrame()
        array= np.zeros((2*playerNumber, len(actions))) 
        for i in range(0,playerNumber):
            name1 = 'C_' + str(i) + 'C_'+ str(playerNumber-1-i)+'D'
            lst.append(name1)
            name2 = 'D_' + str(i) + 'C_'+ str(playerNumber-1-i)+'D'
            lst.append(name2)
        table = pd.DataFrame(array, index = lst, columns = actions )
            
#        table = pd.DataFrame.from_records(lst, columns=actions)
#        i=0
        '''
        for x in table.index:
            print(table.loc[x]['C'])
        '''
        #print(table.stateName)
        return table

    def choose_action(self):
        q_table = self.__table
        state= self.__state
        #print(q_table)
        #print(state)
        state_action = q_table.loc[state]
        #print(state_action)
        if (np.random.uniform()> self.__EPSILON) or (state_action.all() == 0):
            action_name= np.random.choice(self.__ACTIONS)
        else:
            #print("lalaal lalala wo shi kuai le de xiao hang jia")
            action_name = state_action.argmax()
        #print(action_name)
        self.set_nextAction(action_name)
        self.set_lastAction(self.__currentAction)
        self.set_currentAction(self.__nextAction)
        return self.__nextAction

    def soft_max(self, x,lst):
        #map(math.exp(),lst)
        a= [math.exp(i) for i in lst]
        b = sum(a)
        try:
            c = math.exp(x)/b
        except:
            print(a," ",b)
            c = 0
        #print(c)
        return c

#qlearningStrategy(10).soft_max([1,2,3,4,5])
    def choose_action2(self):
        q_table = self.__table
        state= self.__state
        state_action = q_table.loc[state]
        #print(state_action)
        if (np.random.uniform()> self.__EPSILON) or (state_action.all() == 0):
            action_name= np.random.choice(self.__ACTIONS)
        else:
            lst = []
            m = [self.soft_max(i, state_action) for i in state_action]
            #print('m: ', m)
            try:
                if m[0]>m[1]:
                    action_name = 'C'
                else:
                    action_name = 'D'
            except:
                print('m: ', m)
                action_name = 'C'
        #print(action_name)
        self.set_nextAction(action_name)
        self.set_lastAction(self.__currentAction)
        self.set_currentAction(self.__nextAction)
        return self.__nextAction
    def findMaxQvlue(self):
        if self.__lastState != None:
            qC = self.__table.loc[self.__lastState]['C']
            qD = self.__table.loc[self.__lastState]['D']
            if qC >= qD:
                return qC
            else:
                return qD
        else:
            return 0

    def update_reward(self):
        #print(self.__newReward)
        #print(self.__lastReward)
        #print("lastAction: ", self.__lastAction)
        if self.__newReward > self.__lastReward:
            self.__table.loc[self.__state][self.__lastAction] = self.__table.loc[self.__state][self.__lastAction]+self.__ALPHA*(3+self.__GAMMA*self.findMaxQvlue()-self.__table.loc[self.__state][self.__lastAction])
        elif self.__newReward <= self.__lastReward:
            self.__table.loc[self.__state][self.__lastAction] = self.__table.loc[self.__state][self.__lastAction]+self.__ALPHA*(-100+self.__GAMMA*self.findMaxQvlue()-self.__table.loc[self.__state][self.__lastAction])
        self.set_lastReward(self.__newReward)
        self.__lastState = self.__state
        #print(self.__table)
'''            
class table(object):
    def __init__(self):
'''                      
class CSVBuilder(object):
    def __init__(self,txt,table):
        if os.path.isfile(txt)==False:
            with open(txt, 'w') as f:
                f_csv=csv.writer(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
                f_csv.writerow(table)
            
            
    
    def fileSaving(self, data):
        filename = self.__filename
        i = 0
        with open(filename, 'a') as f:
            f_csv=csv.writer(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
            for line in data:
                #print('here')
                f_csv.writerow(line)
#qlearningStrategy(10)
#table = qlearningStrategy(10).build_q_table()
#print(table)
#for x in table.index:
#    print(x)
#CSVBuilder('test1.txt', table)
#qlearningStrategy(10).choose_action()
         
