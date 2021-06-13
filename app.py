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

#Function to get the donut graph
# Todo- Make donut UI

def get_pie_chart(rating_list):
    labels = ['5 Stars', '4 Stars', '3 Stars', '2 Stars','1 Stars']
    values=rating_list
    data = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4,hoverinfo='label+value',title='User Rating')])
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


#Function to get the reviews

def get_review(commentsbox ,search,flag=True):
    reviews = []
    for comment in commentsbox[:-1]:
        try:
            name = comment.find_all('p', {"class": "_2sc7ZR _2V5EHH"})[0].text
            # print("Name: ",name)
        except:
            name = "No user name found !"

        try:
            if(flag==True):
                rating = comment.div.div.div.div.text[0]

            else:
                rating = comment.div.div.div.div.text

        except:
            rating = 'There is no rating given by this user !'
        try:
            heading = comment.div.div.div.p.text

        except:
            heading = 'No Heading found for this review !'

        try:
            comment_body = comment.find_all('div', {"class": 't-ZTKy'})[0].text
            if(comment_body.endswith('READ MORE')):
                comment_body=comment_body[:comment_body.find('READ MORE')]
            else:
                comment_body=comment_body

        except:
            comment_body = "No comments given by user !"

        """To get the date since user using this device !"""
        try:
            dt=comment.find_all('p', {'class': "_2sc7ZR"})[1].text
            # print(dt)
            if("months" in dt):
                using_since = int(dt[:dt.find('months')])
                # print(using_since)
            else:
                dt=to_datetime(dt)
                today = to_datetime(datetime.datetime.today().strftime('%Y-%m-%d'))
                using_since=int((today-dt)/timedelta64(1,'M'))

                # print(using_since)

            # print(using_since)
            # buyed_on = comment.find_all('p', {'class': "_2sc7ZR"})[1].text
            # print(buyed_on)

        except:
            using_since = "No information present !"

        my_dict = {"Product": search, "Name": name, "Rating": rating, "CommentHead": heading, "Comment": comment_body,'Using Since':str(using_since)+" months"}

        reviews.append(my_dict)
    return(reviews)

""""Function to get the product info """

def get_product_info(temp_product_page,search,product_link):
    product_info=[]
    try:
        product_name=temp_product_page.find_all('span',{'class':"B_NuCI"})[0].text
        product_name=product_name[:product_name.find('(')]
        # print(product_name)
    except:
        product_name=search

    try:
        product_overall_rating=temp_product_page.find('span',{'class':'_1lRcqv'}).div.text
        # print(product_overall_rating)
    except:
        product_overall_rating="No Rating Available !"

    try:
        product_seller=temp_product_page.find_all('div',{'class':'_1RLviY'})[0].text
        product_seller_rating=product_seller[-3:]
        product_seller=product_seller[:-3]
        # print(product_seller_rating)
        # print(product_seller)
    except:
        product_seller='No Information Available About Product Seller'
        product_seller_rating='No Information Available About Product Seller Rating'










