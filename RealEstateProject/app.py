# Libaries 
from flask import Flask

# - To make HTTP Requests
import requests 

# - To prevent IP address blacklist from too many Requests
import time
from random import randint

# - Data Science Libaries to parse ZipCode Files
import numpy as np
import pandas as pd

# Create App
app = Flask(__name__)

# Variables
zipCodes = []

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Routing to Main Page
@app.route('/')
def hello():
    cleanAndReturnZip(zipCodes)
    value = CheckZipCodes(zipCodes)
    print (value)
    return "hi"

def CheckZipCodes(zipCodes):
    total = 0
    for item in zipCodes:
        url = "https://mls.foreclosure.com/listing/search.html?g=" + item + "&lc=foreclosure"
        requestUrl = requests.get(url)
        requestText = requestUrl.text
        for lines in requestText.split('/n'):
            if lines[0:11] == 'let markersData=':
                newList = lines.split("delimeter")
        total = total + len(newList)
        time.sleep(randint(0,10))
    return total

# Clean the csv File and return zip codes as strings
# Columns Avaliable: Zip, City, State ID, Population, County Names
def cleanAndReturnZip(zipCodes):
    zip = pd.read_csv('templates/uszips.csv')
    zip.drop('timezone',axis=1,inplace=True)
    zip.drop('military',axis=1,inplace=True)
    zip.drop('imprecise',axis=1,inplace=True)
    zip.drop('county_fips_all',axis=1,inplace=True)
    zip.drop('county_name',axis=1,inplace=True)
    zip.drop('density',axis=1,inplace=True)
    zip.drop('parent_zcta',axis=1,inplace=True)
    zip.drop('lng',axis=1,inplace=True)
    zip.drop('lat',axis=1,inplace=True)
    zip.drop('zcta',axis=1,inplace=True)
    zip.drop('county_fips',axis=1,inplace=True)
    zip.drop('county_weights',axis=1,inplace=True)
    zip.head()
    zipCodes = list(map(str, zipCodes))
    return zipCodes

# Run
if __name__ == '__main__':
    import os
    HOST = os.environ.get('SERVER_HOST', 'localhost')
    try:
        PORT = int(os.environ.get('SERVER_PORT', '5555'))
    except ValueError:
        PORT = 5555
    app.run(HOST, PORT)
