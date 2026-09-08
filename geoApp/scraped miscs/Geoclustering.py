from sklearn.cluster import DBSCAN
import numpy as np
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import csv
from csv import writer
import statsmodels.api as sm
from sklearn.cluster import KMeans
import seaborn as sns
sns.set()

conn = sqlite3.connect('GrabEV.db')
cursor2 = conn.cursor()

# get all records
sql_select_Query = "Select * from Electro"
cursor2.execute(sql_select_Query)
recordsElectro = cursor2.fetchall()

sql_select_Query = "Select * from Shopping"
cursor2.execute(sql_select_Query)
recordsShopping = cursor2.fetchall()

sql_select_Query = "Select * from Shell"
cursor2.execute(sql_select_Query)
recordsShell = cursor2.fetchall()

sql_select_Query = "Select * from Petronas"
cursor2.execute(sql_select_Query)
recordsPetronas = cursor2.fetchall()

sql_select_Query = "Select * from Paul"
cursor2.execute(sql_select_Query)
recordsPaul = cursor2.fetchall()

sql_select_Query = "Select * from mcdmalaysiascraped"
cursor2.execute(sql_select_Query)
records = cursor2.fetchall()

sql_select_Query = "Select * from Government"
cursor2.execute(sql_select_Query)
recordsGo = cursor2.fetchall()

sql_select_Query = "Select * from EVCS"
cursor2.execute(sql_select_Query)
recordsEVCS = cursor2.fetchall()

sql_select_Query = "Select * from EVCSmcd"
cursor2.execute(sql_select_Query)
EVCSmcd = cursor2.fetchall()

sql_select_Query = "Select * from EVCSgovern"
cursor2.execute(sql_select_Query)
EVCSgovern = cursor2.fetchall()

sql_select_Query = "Select * from EVCSshopping"
cursor2.execute(sql_select_Query)
EVCSshopping = cursor2.fetchall()

sql_select_Query = "Select * from EVCScities"
cursor2.execute(sql_select_Query)
EVCScities = cursor2.fetchall()

sql_select_Query = "Select * from Prominentcities"
cursor2.execute(sql_select_Query)
recordscities = cursor2.fetchall()

cursor2.close()
conn.close()



x = pd.DataFrame(recordsEVCS, columns=['locations','lat', 'lng'])
x = x.iloc[:, 1:]
x['lat'] = x['lat'].astype(float)
x['lng'] = x['lng'].astype(float)
xno = (len(x))

y = pd.DataFrame(recordsShopping, columns=['locations','lat', 'lng'])
y = y.iloc[:, 1:]
y['lat'] = y['lat'].astype(float)
y['lng'] = y['lng'].astype(float)
yno = (len(y))

z = pd.DataFrame(records, columns=['locations','lat', 'lng'])
z = z.iloc[:, 1:]
z['lat'] = z['lat'].astype(float)
z['lng'] = z['lng'].astype(float)
zno = (len(z))


v = pd.DataFrame(recordsGo, columns=['locations','lat', 'lng'])
v = v.iloc[:, 1:]
v['lat'] = v['lat'].astype(float)
v['lng'] = v['lng'].astype(float)
vno = (len(v))

w = pd.DataFrame(recordscities, columns=['locations','lat', 'lng'])
w = w.iloc[:, 1:]
w['lat'] = w['lat'].astype(float)
w['lng'] = w['lng'].astype(float)
wno = (len(w))

df1 = pd.DataFrame(EVCSmcd, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
dfEVCS = df1.iloc[:, 1:3]
dfmcd = df1.iloc[:, 4:6]
df1 = df1.iloc[:, 6:]
df1['Distances'] = df1['Distances'].astype(float)
df1 = np.array(df1)
print("The average shortest distance EVCS to mcd is", np.mean(df1), "m")

df2 = pd.DataFrame(EVCSgovern, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
dfgovern = df2.iloc[:, 4:6]
df2 = df2.iloc[:, 6:]
df2['Distances'] = df2['Distances'].astype(float)
df2 = np.array(df2)
print("The average shortest distance EVCS to government agencies is",np.mean(df2), "m")

df3 = pd.DataFrame(EVCSshopping, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
dfshop = df3.iloc[:, 4:6]
df3 = df3.iloc[:, 6:]
df3['Distances'] = df3['Distances'].astype(float)
df3 = np.array(df3)
print("The average shortest distance EVCS to shopping malls is", np.mean(df3), "m")

df4 = pd.DataFrame(EVCScities, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
dfcities = df4.iloc[:, 4:6]
df4 = df4.iloc[:, 6:]
df4['Distances'] = df4['Distances'].astype(float)
df4 = np.array(df4)
print("The average shortest distance EVCS to prominent cities is", np.mean(df4), "m")

total = (np.mean(df1) + np.mean(df2) + np.mean(df3))
print(total)


weight_factormcd = 1/(np.mean(df1)/total)
weight_factorgovern = 1/(np.mean(df2)/total)
weight_factorshop = 1/(np.mean(df3)/total)
# weight_factorcities = 1/(np.mean(df4)/total)

totalweight = (weight_factorshop + weight_factorgovern + weight_factormcd)
print(totalweight)

# weight_fcities = (weight_factorcities/totalweight)
weight_fgovern = (weight_factorgovern/totalweight)
weight_fshop = (weight_factorshop/totalweight) + weight_fgovern
weight_fmcd = (weight_factormcd/totalweight) + weight_fshop

print("weight factors summary:", weight_fgovern, weight_fshop, weight_fmcd)