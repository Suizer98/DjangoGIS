"""


This py file made for connecting and creating database in SQL


"""

import MySQLdb
import sqlite3
import csv
import MySQLdb

# connect to sql server (file based database)
conn = sqlite3.connect('GrabEV.db')

cur = conn.cursor()

# this command use only once
cur.execute('DROP TABLE IF EXISTS heatmapweighted')
cur.execute('''
		CREATE TABLE "heatmapweighted" (
			"locations" TEXT,
			"lat" TEXT,
			"lng" TEXT,
			"weight" TEXT
			)
               ''')

fname = input('Enter the scraped location csv file name: ')
if len(fname) < 1 : fname = "heatmapweighted.csv"

with open(fname) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    # skip header if needed
    next(csv_reader, None)
    for row in csv_reader:
        print(row)
        locations = row[0]
        lat = row[1]
        lng = row[2]
        weight = row[3]
        # lat = lat.strip("\"")
        # lng = lng.strip("\"")
        cur.execute('''INSERT INTO heatmapweighted(locations,lat,lng,weight)
            VALUES (?,?,?,?)''', (locations, lat, lng, weight))
        conn.commit()


# MYSQL


# conn = MySQLdb.connect(host="localhost", port=3306, user="root", passwd="REAPINGHOOK980921", db="mymcd_scraped")
# cursor = conn.cursor()

# import mysql.connector
#
# mydb = mysql.connector.connect(
#   host="35.193.188.63",
#   user="root",
#   password="1998",
# )
#
# cursor = mydb.cursor()
#
# cursor.execute("CREATE DATABASE IF NOT EXISTS mymcd_scraped")
# cursor.execute("USE mymcd_scraped")
#
#
# sql = '''CREATE TABLE IF NOT EXISTS mcdmalaysiascraped
#     (locations TEXT,
# 	    lat TEXT,
# 		lng TEXT
# 		)
# 	'''
#
# cursor.execute(sql)
# cursor.execute("DELETE FROM mcdmalaysiascraped")
# csv_data = csv.reader(open('latlng2.csv'))
# next(csv_data)
# for row in csv_data:
#     cursor.execute('INSERT INTO mcdmalaysiascraped (locations,lat,lng)'
#                    'VALUES(%s, %s, %s)',row)
#
# mydb.commit()
#
# cursor.close()
#
# # read database
# try:
#     connection = mysql.connector.connect(host='localhost',
#                                          database='mymcd_scraped',
#                                          user='root',
#                                          password='REAPINGHOOK980921')
#
#     sql_select_Query = "select * from mcdmalaysiascraped"
#     cursor = connection.cursor()
#     cursor.execute(sql_select_Query)
#     # get all records
#     records = cursor.fetchall()
#     print("Total number of rows in table: ", cursor.rowcount)
#
#     print("\nPrinting each row")
#     for row in records:
#         print("locations = ", row[0], )
#         print("lat       = ", row[1])
#         print("lon       = ", row[2])
#
#
# except mysql.connector.Error as e:
#     print("Error reading data from MySQL table", e)
# finally:
#     if connection.is_connected():
#         connection.close()
#         cursor.close()
#         print("MySQL connection is closed")