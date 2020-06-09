# Libaries 
from flask import Flask

# - To make HTTP Requests
import requests 




def CheckZipCodes():
    total =0
    url = "https://mls.foreclosure.com/listing/search?lc=foreclosure&loc=" + '08816'
    requestUrl = requests.get(url)
    requestText = requestUrl.text
    requestTextSplit = requestText.split('\n')
    for lines in requestTextSplit:
        if lines[0:15].lower() == 'var markersdata':
            print(lines)

CheckZipCodes()
