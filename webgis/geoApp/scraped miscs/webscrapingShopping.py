"""


This py file is for webscraping addresess from website HTML


"""

import os
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import pandas as pd
import googlemaps
import csv
from selenium import webdriver
from selenium.webdriver.support import expected_conditions as EC, expected_conditions
import chromedriver_autoinstaller
from time import sleep
import sqlite3

# dowbload chrome driver for selenium and here's put the path of the downloaded exe file.
# selenium will use this path to launch the driver
# CHROME = "D:/Downloads/chromedriver_win32/chromedriver.exe"
from selenium.webdriver.support.wait import WebDriverWait

# chromedriver_autoinstaller.install()
# # CHROME = Service('./chromedriver')
# options = Options()
# options.headless = True
# # options.add_argument("--headless")
#
# driver = webdriver.Chrome(options=options)
# # driver = webdriver.Chrome(service=CHROME, options=options)
# # driver = webdriver.Chrome(executable_path=CHROME, options=options)
#
# # ask the driver to navigate to this url
# driver.get('https://en.wikipedia.org/wiki/List_of_shopping_malls_in_Malaysia')
# # driver.get('https://www.google.com')
#
#
# try:
#     myElem = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
#     print ("Page is ready!")
# except TimeoutException:
#     print ("Loading may not be completed!")
#
#
# driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# # time.sleep(5)
# # elements =driver.find_elements_by_class_name("addressText")
#
# # extract the elements with < class = "addressText"
# elements = driver.find_elements(By.CLASS_NAME, "mw-parser-output")


# Geocoder
# Create and activate api key on google cloud platform to use its api
gmaps = googlemaps.Client(key='AIzaSyB9-TQpzo1bAJuSBXnYMpCCyXgJbE86h50')

# geocoder = Nominatim(user_agent= 'SZ')
# country = []
# geocodes = []
# names = []
codes = []
codes2 = []

# AddressTitle
# elements2 = driver.find_elements(By.CLASS_NAME, "addressTitle")
#
# addressesTitle = []
#
# for line2 in elements2:
#     if not ':' in line2.text:
#         addressesTitle.append(line2.text)
#         print(line2.text)
#
# print(addressesTitle)
# len(addressesTitle)

# print ("Number of items in the list = ", len(addressesTitle))

# full address
addresses = []

# for line in elements:
#     # if not '//' in line.text:
#         addresses.append(line.text)
#         print(line.text)
#
# print(addresses)
#
# len(addresses)
#
# print ("Number of items in the list = ", len(addresses))

# with open('shopping.csv', 'w', encoding='utf-8') as f:
#     for line in addresses:
#         print(line.encode("utf-8"))
#         f.write(line)
#         f.write('\n')
#
# # filter unwanted texts
# open('shopping2.csv', 'w').writelines(line for line in open('shopping.csv', encoding='utf-8')
#                                                         if not '^' in line
#                                                         if not '[edit]' in line
#                                                         if not '.' in line
#                                                         if not ':' in line)
#
# if (os.path.isfile('shopping2.csv') and os.path.isfile('shopping.csv')):
#     os.remove('shopping.csv')
#     print("file deleted")
# else:
#     print("file not found")



# get lat long using long address
# loop until success because sometimes geocoder return blank attributes


data = pd.read_csv("shopping2.csv", error_bad_lines=False)
for line in data.locations:
    # row variable is a list that represents a row in csv

    addresses.append(line)

print(addresses)


sleep_time = 2
num_retries = 10
for x in range(0, num_retries):
    try:
        for i in addresses:
            address = gmaps.geocode(i)
            print(address)
            lat = address[0]["geometry"]["location"]["lat"]
            lng = address[0]["geometry"]["location"]["lng"]
            locations = address[0]["formatted_address"]
            codes.append([locations, lat, lng])
        str_error = None
    except Exception as e:
        str_error = str(e)
        print(str_error)
    if str_error:

        sleep(sleep_time)  # wait before trying to fetch the data again
        sleep_time *= 2  # Implement your backoff algorithm here i.e. exponential backoff
    else:
        break

print(codes)
#
#
# #  headers
# fields = ['locations', 'lat', 'lng']
#
# with open('Paultanfinal2.csv', 'w') as f:
#     # using csv.writer method from CSV package
#     write = csv.writer(f)
#     write.writerow(fields)
#     write.writerows(codes)
#
#
# df = pd.read_csv("Paultanfinal2.csv")
# # checking the number of empty rows in th csv file
# print(df.isnull().sum())
# # Droping the empty rows
# modifiedDF = df.dropna()
# # Saving it to the csv file
# modifiedDF.to_csv('Paultanfinal2.csv', index=False)
#
#
# # driver.close()
#
# # connect to sql server (file based database)
# conn = sqlite3.connect('GrabEV.db')
#
# cur = conn.cursor()
#
# # this command use only once
# cur.execute('DROP TABLE IF EXISTS Paul')
# cur.execute('''
# 		CREATE TABLE "Paul" (
# 			"locations" TEXT,
# 			"lat" TEXT,
# 			"lng" TEXT
# 			)
#                ''')
#
# fname = input('Enter the scraped location csv file name: ')
# if len(fname) < 1 : fname = "Paultanfinal2.csv"
#
# with open(fname) as csv_file:
#     csv_reader = csv.reader(csv_file, delimiter=',')
#     for row in csv_reader:
#         print(row)
#         locations = row[0]
#         lat = row[1]
#         lng = row[2]
#         # lat = lat.strip("\"")
#         # lng = lng.strip("\"")
#         cur.execute('''INSERT INTO Paul (locations,lat,lng)
#             VALUES (?,?,?)''', (locations, lat, lng))
#         conn.commit()