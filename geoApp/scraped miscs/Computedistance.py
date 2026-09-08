import numpy as np
import pandas as pd
import sqlite3
import geopy.distance
import csv
from itertools import chain
import scipy
from scipy import stats
import matplotlib.pyplot as plt


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

# compute shortest distance
finallist = []
for i,row in x.iterrows(): # A
    a = row['lat'], row['lng']
    distances = []

    # change here
    for j,row2 in w.iterrows(): # B
        b = row2['lat'], row2['lng']
        distances.append(geopy.distance.geodesic(a, b).km)

    min_distance = min(distances)
    min_index = distances.index(min_distance)
    i = i+1
    min_index = min_index + 1
    print("Station", i, "is closest to target", min_index, min_distance, "km")
    finallist.append([i, row['lat'], row['lng'], min_index, row2['lat'], row2['lng'], min_distance])

print(finallist)

# input_filename = 'EVCS-cities.csv'
#
# with open(input_filename, 'w') as f:
#     # using csv.writer method from CSV package
#     write = csv.writer(f)
#     write.writerows(finallist)
#
# df = pd.read_csv(input_filename)
# # checking the number of empty rows in th csv file
# print(df.isnull().sum())
# # Droping the empty rows
# modifiedDF = df.dropna()
# # Saving it to the csv file
# modifiedDF.to_csv(input_filename, index=False)
#
# cursor2.execute('DROP TABLE IF EXISTS EVCScities')
# cursor2.execute('''
# 		CREATE TABLE "EVCScities" (
# 			"From1" TEXT,
# 			"lat1" TEXT,
# 			"lng1" TEXT,
# 			"To2" TEXT,
# 			"lat2" TEXT,
# 			"lng2" TEXT,
# 			"Distances" TEXT
# 			)
#                ''')
#
# fname = input('Enter the scraped location csv file name: ')
# if len(fname) < 1 : fname = input_filename
#
# with open(fname) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader:
#         print(row)
#         From = row[0]
#         lat1 = row[1]
#         lng1 = row[2]
#         To = row[3]
#         lat2 = row[4]
#         lng2 = row[5]
#         Distances = row[6]
#         # lat = lat.strip("\"")
#         # lng = lng.strip("\"")
#         cursor2.execute('''INSERT INTO EVCScities (From1, lat1, lng1, To2, lat2, lng2, Distances)
#             VALUES (?,?,?,?,?,?,?)''', (From, lat1, lng1, To, lat2, lng2, Distances))
#         conn.commit()



df1 = pd.DataFrame(EVCSmcd, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
df1 = df1.iloc[:, 6:]
df1['Distances'] = df1['Distances'].astype(float)
df1 = np.array(df1)


df2 = pd.DataFrame(EVCSgovern, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
df2 = df2.iloc[:, 6:]
df2['Distances'] = df2['Distances'].astype(float)
df2 = np.array(df2)


df3 = pd.DataFrame(EVCSshopping, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
df3 = df3.iloc[:, 6:]
df3['Distances'] = df3['Distances'].astype(float)
df3 = np.array(df3)

df4 = pd.DataFrame(EVCScities, columns=['From1', 'lat1', 'lng1', 'To1', 'lat2', 'lng2','Distances'])
df4 = df4.iloc[:, 6:]
df4['Distances'] = df4['Distances'].astype(float)
df4 = np.array(df4)


# pearson = np.corrcoef(df1, df2)
# print(pearson)





cursor2.close()
conn.close()


