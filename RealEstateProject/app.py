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

# - For parsing result 
import re

# - For Sending Email
import smtplib, ssl

# Create App
app = Flask(__name__)

# Variables

# Make the WSGI interface available at the top level so wfastcgi can get it.
wsgi_app = app.wsgi_app

# Routing to Main Page
@app.route('/')
def hello():
    value = str(CheckZipCodes())
    return value

# For every 1000 zipCode Searches Create a new File
def GenerateFile(timeToCreate):
    pass

# Email File every 1000 zipCodes
def EmailFile():
    port = 465  # For SSL
    password = input()

    # Create a secure SSL context
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL("smtp.gmail.com", port, context=context) as server:
        server.login("my@gmail.com", password)
        # TODO: Send email here

def CheckZipCodes():

    timeToCreate = 0
    total = 0
    zipCodes = list()
    zipCodes = cleanAndReturnZip()
    word = "listingId:"
    counter = 0
    countOfForclosures = 0

    for item in zipCodes:
        url = "https://mls.foreclosure.com/listing/search?lc=foreclosure&loc=" + item
        requestUrl = requests.get(url)
        requestText = requestUrl.text
        requestTextSplit = requestText.split('\n')

        for lines in requestTextSplit:
            if lines[0:15].lower() == 'var markersdata':
                countOfForclosures = sum(1 for _ in re.finditer(r'\b%s\b' % re.escape(word), lines))   
                total = total + countOfForclosures

                if timeToCreate/10000 == 0 or timeToCreate == 0:
                    f= open("Totals" + str(timeToCreate) + ".txt","w+")
                    timeToCreate = timeToCreate + 1
                print("Zip Code: {} Total Forclosures: {}".format(zipCodes[counter],countOfForclosures))
                f.write("Zip Code: {} Total Forclosures: {}".format(zipCodes[counter],countOfForclosurest))

        countOfForclosures = 0
        counter = counter + 1
        time.sleep(randint(0,150)/100)

    f.write("Total Overall Forclosures: {}".format(total))
    f.close() 
    return total

# Clean the csv File and return zip codes as strings
# Columns Avaliable: Zip, City, State ID, Population, County Names
def cleanAndReturnZip():
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
    zipCodes = list()
    zipCodes = list(map(str, zip['zip']))
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
