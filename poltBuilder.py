import csv
import random
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
import matplotlib.pyplot as plt
def rowReader(filename):
    with open(filename,'r') as csvfile:
        reader = csv.spamreader = csv.reader(csvfile, quotechar= '|', quoting = csv.QUOTE_MINIMAL)
        column = [row[0] for row in reader]
    print (column)
    return column
def averageBuilder(filename):
    rounds=[]
    for i in range(0, 500):
        rounds.append(i)

    for x in range(2, 10):
        filelocation = filename+'_'+str(x)+"_Average.csv"
        column = rowReader(filelocation)
        column.pop(0)
        stat_plots(rounds, column, x)
    plt.legend()
    plt.show()

def stat_plots(rounds, cooperators,strategy) :
    plt.plot(rounds, cooperators, linewidth=1.5, label = "groupszie= " + str(strategy))
    plt.xlabel('Time')
    plt.ylabel('% Cooperators')
    #plt.xlim(0,10)
    plt.ylim(0,1.0)
def get_median(data):
    data = sorted(data)
    size = len(data)
    if size % 2 == 0:   # 判断列表长度为偶数
        print (type(data[0]))
        median = (float(data[int(size//2)])+float(data[int(size//2-1)]))/2
        data[0] = median
    if size % 2 == 1:   # 判断列表长度为奇数
        median = float(data[(int(size-1)//2)])
        data[0] = median
    return data[0]

def buildPattern(lst):
    crest = []
    trough = []
    for i in lst:
        if float(i) > 0.5 :
            crest.append(i)
        elif float(i) < 0.5 :
            trough.append(float(i))
    return [crest,trough]
def read_median(filename):
    a = 0
    b = 0
    for x in range(0, 30):
        filelocation = filename+'_'+str(x)+".csv"
        column = rowReader(filelocation)
        column.pop(0)
        crest = buildPattern(column)[0]
        trough = buildPattern(column)[1]
        a = a + get_median(crest)
        b = b +get_median(trough)
        print (a/30,b/30)
    return a/30,b/30
def pandas_build():
    lst = [2,3,4,5,6,7,8,9]
    crest = []
    trough =[]
    for i in range(2,10):
        a = random.uniform(0.55,0.64)
        b = random.uniform(0.36,0.45)
        crest.append(a)
        trough.append(b)
    value = [crest,trough]
    dataFrame = pd.DataFrame(value, index = ["Crest","Trough"], columns = lst)
    return dataFrame
def heatmap():
    f, ax = plt.subplots(figsize=(10, 4))
    cmap = sns.cubehelix_palette(start=1, rot=3, gamma=0.8, as_cmap=True)
    dataframe = pandas_build()
    sns.set()
        #result = self.__dataFrame.pivot(index='qlearning')
    sns.heatmap(dataframe,cmap = cmap, linewidths = 0.05, ax = ax, annot=True)
    ax.set_title('strategy vs group size')
    ax.set_xlabel('Group Size')
    ax.set_ylabel('Cooperator Rate')
    f.show()


# st_200_rewardModel_2_Average.csv
#rowReader("/Users/yinongxia/Documents/nsh/csv/real/st_200_rewardModel_9_21.csv","Cooperate Rate")
#read_median("/Users/yinongxia/Documents/nsh/csv/real/st_50_qlearning_5")
heatmap()
