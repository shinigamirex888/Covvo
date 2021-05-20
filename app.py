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
