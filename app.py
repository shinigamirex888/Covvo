#New idea
import pymongo
from bs4 import BeautifulSoup as bs
import requests
from urllib.request import urlopen as ureq
from flask import Flask,render_template,request
from pandas import to_datetime
from flask_cors import cross_origin
from numpy import timedelta64
import datetime
import logging
import plotly
import pymongo as mg
import plotly.graph_objects as go
import json

# checking the database logs(logger)

DBlogger=logging.getLogger('Database')

DBlogger.setLevel(logging.DEBUG)

formatter=logging.Formatter('%(asctime)s:%(name)s: %(message)s')

file_handeler=logging.FileHandler('Database.log')

file_handeler.setLevel(logging.ERROR)

file_handeler.setFormatter(formatter)

DBlogger.addHandler(file_handeler)

#Stream Handler To Get Logs on Consol

stream_handler=logging.StreamHandler()
stream_handler.setFormatter(formatter)
DBlogger.addHandler(stream_handler)

app=Flask(__name__)


#Function to get product Hightlights!

def get_product_highlights(box):
    lst=[]
    highlights=box.find_all('li',{'class':'_21Ahn-'})
    for i in range(len(highlights)):
        lst.append(highlights[i].text)
    return lst









