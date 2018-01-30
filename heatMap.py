import seaborn as sns
import pandas as pd
import os
import csv
import matplotlib.pyplot as plt

_dataFrame = None
class heatMap(object):
    def __init__(self):
        self.__dataFrame = None
        self._parameter = []
        self.__runningTimes = 500
    def pandas_build(self, strategy, value, parameter):
        lst = []
        #print (value)
        for i in parameter:
            para = str([5, 1, 1, int(i)])
            lst.append(para)

        if self.__dataFrame == None:
            print (len(value),len(lst),len(strategy))
            self.__dataFrame = pd.DataFrame(value, index = strategy, columns = lst)
            #self.__dataFrame
        else:
            self.__dataFrame[lst] = value
    def get_dataFrame(self):
        return self.__dataFrame
    def valueColection(self,strategy, population, parameters):
        value = []
        location = os.getcwd()
        for para in parameters:
            name = 'st_' + str(population) + '_' + strategy + '_' + para
            #name2 = 'st_' + str(population) + '_' + strategy + '_' + str([5, 1, 1, int(para)])
            filename = location + '/csv/real/' + name + '/' + name + '_0.csv'
            #print (filename)
            with open(filename, 'r') as f:
                spamreader = csv.reader(f, quotechar='|', quoting=csv.QUOTE_MINIMAL)
                for index, row in enumerate(spamreader):
                    if index == self.__runningTimes:
                        a = round(float(row[0]),8)
                        value.append(a)
        #print (value)
        return value


    def heatmap(self,strategylst, population,parameters):
        f, ax = plt.subplots(figsize=(10, 4))
        cmap = sns.cubehelix_palette(start=1, rot=3, gamma=0.8, as_cmap=True)
        lst = []
        for stategies in strategylst:
            #print (stategies)
            valuelst =self.valueColection(stategies, population,parameters)
            #print (valuelst)
            lst.append(valuelst)
        self. pandas_build(strategylst,lst,parameters)
        print ('hereheheheheheh')
        print (self.__dataFrame)
        sns.set()
        #result = self.__dataFrame.pivot(index='qlearning')
        sns.heatmap(self.__dataFrame,cmap = cmap, linewidths = 0.05, ax = ax, annot=True)
        ax.set_title('strategy vs group size')
        ax.set_xlabel('region')
        ax.set_ylabel('kind')
        f.show()

    def test(self):
        import numpy as np
        from pandas import DataFrame
        import seaborn as sns
        Index = ['aaa', 'bbb', 'ccc', 'ddd', 'eee']
        Cols = ['A', 'B', 'C', 'D']
        df = DataFrame(abs(np.random.randn(5, 4)), index=Index, columns=Cols)
        print (df)
        sns.heatmap(df, cmap = cmap, linewidths = 0.05, ax = ax ,annot=True)
        #sns.show()



h=heatMap()
#h.test()
#h.valueColection('qlearning',50,['[5,1,1,1]','[5,1,1,2]','[5,1,1,3]','[5,1,1,4]','[5,1,1,5]','[5,1,1,6]','[5,1,1,7]','[5,1,1,8]','[5,1,1,9]','[5,1,1,10]'])
h.heatmap(['qlearning','rewardModel'],200,['2','3','4','5','6','7','8','9','10'])
#h.heatmap(['qlearning'],200,['1','2','3','4','5','6','7','8','9','10'])
#h.pandas_build(['random'], [10,20,30], ['[0,1,2]','[1,2,3]','[3,2,1]'])
#print (h.get_dataFrame())
