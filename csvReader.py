#from testNPlayers import game
#import testNPlayers
import csv
import sys
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import plotly.graph_objs as go
import plotly.plotly as py
import numpy as np
import seaborn as sns
import pandas as pd

#print("Please type in the name of files")
print ('Please type in the running type:')
_model=sys.stdin.readline().strip('\n')
if _model == 'main1' or _model == 'main2':
    print("Please type in the name of files")
    _file = sys.stdin.readline().strip('\n')
    _fileLocation = '/Users/yinongxia/Documents/nsh/csv/real/' + _file
elif _model == 'main3':
    print ("Please type in the strategy type:")
    _list = sys.stdin.readline().strip('\n').split()
    _fileLocation = None
    print (_list)
_dataFrame = None
#_fileLocation = '/Users/yinongxia/Documents/nsh/csv/real/'+_file+'/'+_file
_runningTime = 30
class csvReader(object):
    def __init__(self, rounds=500,initName= _fileLocation, runningTime = _runningTime):
        self.__rounds = rounds
        self.__cooperator = []
        self.__initName = initName
        self.__fileLst = []
        self.__lst = []
        self.__runningTime = runningTime
        self.__dataFrame = None
        self.initCooperator()
        self.initfileList()
        self.initLst()

    def get_dataFrame(self):
        return self.__dataFrame

    def get_cooperator(self):
        return self.__cooperator
    
    def get_fileLst(self):
        return self.__fileLst
    
    def initCooperator(self):
        i= 0
        while i < self.__rounds:
            self.__cooperator.append(0)
            i=i+1
#st_200_random_[5, 1, 1, 5]
    def initfileList(self):
        i = 0
        while i < self.__runningTime:
            filename = self.__initName + '_'+ str(i) +'.csv'
            self.__fileLst.append(filename)
            i=i+1
    def initLst(self):
        i=0
        while i<self.__rounds:
            self.__lst.append([0.0,0.0])
            i=i+1
        #print(self.__lst,"haha",len(self.__lst))
    def get_lst(self):
        return self.__lst

#/Users/yinongxia/Documents/nsh/csv/st_10_fpopular
#2017-09-13_12-34-47

def main():
    reader = csvReader()
    cooperator = reader.get_lst()
    lalala = []
    rounds = []
    lst = reader.get_fileLst()
    filename = _fileLocation + '_Average.csv'
    with open(filename, 'w') as f:
            f_csv=csv.writer(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
            f_csv.writerow(['Cooperate Rate', 'Average Reward'])
    for filenames in lst:
        with open(filenames, 'r') as f:
            spamreader = csv.reader(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
            for i,row in enumerate(spamreader):
                try:
                    #print(i)
                    cooperator[i-1][0] = float(cooperator[i-1][0]) +float(row[0])
                    cooperator[i-1][1] = float(cooperator[i-1][1]) +float(row[1])
                except:
                    print(filenames)
    with open(filename, 'a') as f:
        f_csv=csv.writer(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
        i=0
        for line in cooperator:
            line[0] = line[0]/len(lst)
            line[1] = line[1]/len(lst)
            lalala.append(line[0])
            rounds.append(i)
            i=i+1
            f_csv.writerow(line)
        plot(lalala,rounds)

def plot(lalala,rounds):
    plt.plot(rounds, lalala, linewidth=1.0)
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1)
#    txt = _models+'_'+_strategy +'_'+ str(_playerNumber) +'_'+ str([_F,_cost,_M,_N])+'_'+str(_gameround)
    filename = _fileLocation +'.png'
    plt.savefig(filename)

def findFinalLine(fileLocation):
    with open (fileLocation, 'r') as f:
        spamreader = csv.reader(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
        print (len(spamreader))
        for row in spamreader:
                #print(type(row[0]))
                try:
                    cooperater.append(float(row[0]))
                except:
                    print(row[0])
                r=r+1

def build_q_table(strategy,i):
    for stategies in strategy:
        fileLocation = '/Users/yinongxia/Documents/nsh/csv/real/' + _file + str(i) + ']/' + _file + str(i) + ']_Average.csv'

        #if _dataFrame == None:
    for i in range(1,11):
        fileLocation = '/Users/yinongxia/Documents/nsh/csv/real/'+_file+str(i)+']/'+_file +str(i)+']_Average.csv'
    with open (fileLocation, 'r') as f:
        spamreader = csv.reader(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
        for row in spamreader:
                #print(type(row[0]))
                try:
                    cooperater.append(float(row[0]))
                except:
                    print(row[0])
                r=r+1
    playerNumber = 10
    actions =   ['A','B']
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
    return table


def heatMap():
    z = [50,200,500,2000]
    yData = [1,2,3,4,5,6,7,8,9,10]
    zData = [0.5,0.6,0.5,0.6,0.7,0.65,0.71,0.62,0.47,0.51]
    sns.set()
#    uniform_data = np.random.rand(10, 12)
    uniform_data = build_q_table()
    print(uniform_data)
    ax = sns.heatmap(uniform_data)
    plt.show()
'''
    mean = [0,0]
    cov = [[0,1],[1,0]]
    x, y = np.random.multivariate_normal(mean, cov, 10000).T
    print('x: ',len(x))
    print('y: ',len(y))
    
    hist, xedges, yedges = np.histogram2d(x,y)
    print('hist: ', hist)
    print('xedges: ', xedges)
    print('yedges: ', yedges)
    plt.hist2d(x, y, bins=40)
    plt.colorbar()
    plt.grid()
    plt.show()
#    X,Y = np.meshgrid(xedges,yedges)
    #print(X,Y)

    plt.imshow(hist)
    plt.grid(True)
    plt.colorbar()
    plt.show()
'''

def threeD_plot(rounds,cooperators, para):
    fig = plt.figure()
    ax = Axes3D(fig)
    ax.set_ylabel('Time')
    ax.set_zlabel('% Cooperators')
    ax.set_xlabel('para')
    plt.plot(para, rounds, cooperators, marker="o", linewidth=1.0)

def main2():
    for i in range(1,11):
        print(i)
        name = 'Para:'+str(i)
        cooperater= []
        rounds = []
        r = 0
        para = []
        fig = plt.figure()
        ax = Axes3D(fig)
        ax.set_ylabel('Time')
        ax.set_zlabel('% Cooperators')
        ax.set_xlabel('para')
        fileLocation = '/Users/yinongxia/Documents/nsh/csv/real/'+_file+str(i)+']/'+_file +str(i)+']_Average.csv'
        with open(fileLocation, 'r') as f:
            spamreader = csv.reader(f, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
            for row in spamreader:
                #print(type(row[0]))
                try:
                    cooperater.append(float(row[0]))
                    rounds.append(r)
                    para.append(i)
                except:
                    print(row[0])
                r=r+1
        plt.plot(para, rounds, cooperater, linewidth=1.0, label = name)
    plt.legend()
    plt.show()
                    
main()
#csvReader().initLst()
#main2()
#heatMap()
