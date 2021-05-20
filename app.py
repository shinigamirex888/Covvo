#installing the required libraries


from flask import Flask, render_template, request,jsonify
import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as uReq
import pymongo

app = Flask(__name__)


@app.route('/',methods=['POST','GET'])
def index():
    if request.method=='POST':
        searchString=request.form['content'].replace(" ","")
        #this will shorten the input content
        try:
            #will access data from the existing database if present.
            dbConn = pymongo.MongoClient("mongodb://localhost:27017/")
            db = dbConn['crawlerDB']
            reviews = db[searchString].find({})
            if reviews.count() > 0:
                return render_template('results.html', reviews=reviews)

