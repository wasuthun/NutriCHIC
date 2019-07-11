#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 22:35:01 2019

@author: johnpaul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul  8 11:13:40 2019

@author: johnpaul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jul  7 14:16:29 2019

@author: johnpaul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul  4 14:44:10 2019

@author: johnpaul
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 15:30:37 2019

@author: johnpaul
"""
import pandas as pd
import matplotlib.pyplot as plt
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

dfACC= pd.read_csv(config['Import_file']['ACC_file'], delimiter=',').iloc[1:-1,:].reset_index(drop=True).reindex()
dfBVP= pd.read_csv(config['Import_file']['BVP_file'], delimiter=',').iloc[1:-1,:].reset_index(drop=True).reindex()
dfEDA= pd.read_csv(config['Import_file']['EDA_file'], delimiter=',').iloc[1:-1,:]
dfHR= pd.read_csv(config['Import_file']['HR_file'], delimiter=',').iloc[1:-1,:].reset_index(drop=True).reindex()
#df5= pd.read_csv("/Users/johnpaul/Downloads/res1_s02_t0_j1/IBI.csv", delimiter=',')
dfTEMP= pd.read_csv(config['Import_file']['TEMP_file'], delimiter=',').iloc[1:-1,:]
dfTAGS= pd.read_csv(config['Import_file']['TAGS_file'], delimiter=',')

x=dfEDA.columns
timeStamp=x.values.tolist()[0]
numberCut=dfBVP.shape[0]
dfEDA.columns = ['EDA']
dfBVP.columns = ['BVP']
dfHR.columns = ['HR']
dfTEMP.columns = ['TEMP']
dfACC.columns = ['AC1','AC2','AC3']
print(dfACC.shape)
print(dfHR.shape)
print(dfEDA.shape)
print(dfTEMP.shape)
dfkACC=dfACC.rolling(window=2).mean().iloc[1:-1,:]
#df2=df2.rolling(window=64).mean().loc[lambda df: df.index%64==0].reset_index(drop=True)
dfkEDA=dfEDA.rolling(window=2).mean().reset_index(drop=True).reindex().iloc[1:-1,:]
dfkTEMP=dfTEMP.rolling(window=2).mean().reset_index(drop=True).reindex().iloc[1:-1,:]
#df4.index=range(10,df1.shape[0])
def null_table(data):
    print("Training Data Frame")
    print(pd.isnull(data).sum())
dfACC.index=range(0,dfACC.shape[0]*2,2)
dfHR.index=range(704,dfHR.shape[0]*64+64*11,64)
dfEDA.index=range(0,dfEDA.shape[0]*16,16)
dfTEMP.index=range(0,dfTEMP.shape[0]*16,16)
dfkACC.index=range(1,dfACC.shape[0]*2-4,2)


#df1=pd.concat([df1, dfk1]).sort_index()
dfBVP=pd.merge(dfACC, dfBVP, how='outer',left_index =True , right_index = True)
dfBVP=pd.merge(dfBVP,dfHR, how='outer',left_index =True , right_index = True)
dfBVP=pd.merge(dfBVP,dfEDA, how='outer',left_index =True , right_index = True)
dfBVP=pd.merge(dfBVP,dfTEMP, how='outer',left_index =True , right_index = True)
#df2=pd.merge(df2,df6, how='outer',left_index =True , right_index = True)
print(dfBVP)
dateList=[]
tagList=[]
for x in range(0, dfBVP.shape[0]):
    ds=x/64
    dateList.append(ds)
    tagList.append(0)
dfTIME=pd.DataFrame(dateList,columns=['Time'])
dfBVP=pd.merge(dfBVP,dfTIME, how='outer',left_index =True , right_index = True)

tagList[int((float(dfTAGS.columns[0])-float(timeStamp))/0.015625)]=dfTAGS.columns[0]
dfkTAGS=pd.DataFrame(tagList,columns=['Tags'])
print(dfTIME['Time'][int((float(dfTAGS.columns[0])-float(timeStamp))/0.015625)])
dfBVP=pd.merge(dfBVP,dfkTAGS, how='outer',left_index =True , right_index = True)

dfBVP=dfBVP.truncate(before=0, after=numberCut-1)
print(dfBVP)
print(dfBVP['Tags'][int((float(dfTAGS.columns[0])-float(timeStamp))/0.015625)])

line, = plt.plot(dfBVP['Time'],dfBVP['AC1'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['AC1'])
plt.title('ACC1')
plt.show()

line, = plt.plot(dfBVP['Time'],dfBVP['AC2'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['AC2'])
plt.title('ACC2')
plt.show()

line, = plt.plot(dfBVP['Time'],dfBVP['AC3'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['AC3'])
plt.title('ACC3')
plt.show()

line, = plt.plot(dfBVP['Time'],dfBVP['BVP'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['BVP'])
plt.title('BVP')
plt.show()

line, = plt.plot(dfBVP['Time'],dfBVP['HR'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['HR'])
plt.title('HR')
plt.show()

line, = plt.plot(dfBVP['Time'],dfBVP['EDA'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['EDA'])
plt.title('EDA')
plt.show()
line, = plt.plot(dfBVP['Time'],dfBVP['TEMP'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['TEMP'])
plt.title('TEMP')
plt.show()

line, = plt.plot(dfBVP['Time'],dfBVP['Tags'],"-")
scatter = plt.scatter(dfBVP['Time'],dfBVP['Tags'])
plt.title('Tags')
plt.show()

dfBVP.to_csv("output1.1.2.2.csv",index=False)
