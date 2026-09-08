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

# dowbload chrome driver for selenium and here's put the path of the downloaded exe file.
# selenium will use this path to launch the driver
# CHROME = "D:/Downloads/chromedriver_win32/chromedriver.exe"
from selenium.webdriver.support.wait import WebDriverWait

chromedriver_autoinstaller.install()
# CHROME = Service('./chromedriver')
options = Options()
options.headless = True
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)
# driver = webdriver.Chrome(service=CHROME, options=options)
# driver = webdriver.Chrome(executable_path=CHROME, options=options)

# ask the driver to navigate to this url
driver.get('https://www.mcdonalds.com.my/locate-us')
# driver.get('https://www.google.com')


try:
    myElem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.ID, 'IdOfMyElement')))
    print ("Page is ready!")
except TimeoutException:
    print ("Loading may not be completed!")


driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
# time.sleep(5)
# elements =driver.find_elements_by_class_name("addressText")

# extract the elements with < class = "addressText"
elements = driver.find_elements(By.CLASS_NAME, "addressText")

# # write scraped text in file
# with open('mcd.txt', 'w') as f:
#         for line in elements:
#                 print(line.text)
#                 f.write(line.text)
#                 f.write('\n')

# # filter unwanted texts
# open('mcdfiltered.txt','w').writelines(line for line in open('mcd.txt') if not 'Fax:' in line)
# open('mcdfinal.txt','w').writelines(line for line in open('mcdfiltered.txt') if not 'Tel:' in line)
#
#
# with open('mcdfinal.txt') as rawfile:
#     addresses = [line.rstrip('\n') for line in rawfile]
#     print(addresses)

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
elements2 = driver.find_elements(By.CLASS_NAME, "addressTitle")

addressesTitle = []

for line2 in elements2:
    if not ':' in line2.text:
        addressesTitle.append(line2.text)
        print(line2.text)

print(addressesTitle)
len(addressesTitle)

print ("Number of items in the list = ", len(addressesTitle))

# full address
addresses = []

for line in elements:
    if not ':' in line.text:
        addresses.append(line.text)
        print(line.text)

print(addresses)

len(addresses)

print ("Number of items in the list = ", len(addresses))

# get lat long using long address
# loop until success because sometimes geocoder return blank attributes



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

#  headers
fields = ['locations', 'lat', 'lng']

with open('latlng.csv', 'w') as f:
    # using csv.writer method from CSV package
    write = csv.writer(f)
    write.writerow(fields)
    write.writerows(codes)


df = pd.read_csv("latlng.csv")
# checking the number of empty rows in th csv file
print(df.isnull().sum())
# Droping the empty rows
modifiedDF = df.dropna()
# Saving it to the csv file
modifiedDF.to_csv('latlng.csv', index=False)


with open('latlng.csv', 'r') as in_file, open('latlng2.csv', 'w') as out_file:
    seen = set() # set for fast O(1) amortized lookup
    for line in in_file:
        if line in seen: continue # skip duplicate

        seen.add(line)
        out_file.write(line)

if(os.path.exists('latlng.csv') and os.path.isfile('latlng2.csv')):
  os.remove('latlng.csv')
  print("file deleted")
else:
  print("file not found")

# import back the csv
data = pd.read_csv ("latlng2.csv")
df = pd.DataFrame(data)

print(df)
len(df)

print ("Number of items in the list = ", len(df))


# get lat long using address title
# codesT = []
# for i in addressesTitle:
#     addressT = gmaps.geocode(i)
#     print (addressT)
#     lat = addressT[0]["geometry"]["location"]["lat"]
#     lng = addressT[0]["geometry"]["location"]["lng"]
#     locations = addressesTitle[0]
#     codesT.append([locations, lat, lng])
#
#
# print(codesT)
#
# fields = ['locations', 'lat', 'lng']
#
# with open('latlngT.csv', 'w') as f:
#     # using csv.writer method from CSV package
#     write = csv.writer(f)
#     write.writerow(fields)
#     write.writerows(codes)
#     lines = (line.rstrip() for line in f)
#     lines = (line for line in lines if line)
#
# df = pd.read_csv("latlngT.csv")
# # checking the number of empty rows in th csv file
# print(df.isnull().sum())
# # Droping the empty rows
# modifiedDF = df.dropna()
# # Saving it to the csv file
# modifiedDF.to_csv('latlngT.csv', index=False)



