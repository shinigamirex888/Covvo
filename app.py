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

"""Logger to check the database logs"""

DBlogger = logging.getLogger('Database')

DBlogger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s:%(name)s: %(message)s')

file_handeler = logging.FileHandler('Database.log')

file_handeler.setLevel(logging.ERROR)

file_handeler.setFormatter(formatter)

DBlogger.addHandler(file_handeler)

"""Stream Handler To Get Logs on Consol"""

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)
DBlogger.addHandler(stream_handler)

app = Flask(__name__)

"""Function to get product Hightlights!"""


def get_product_highlights(box):
    lst = []
    highlights = box.find_all('li', {'class': '_21Ahn-'})
    for i in range(len(highlights)):
        lst.append(highlights[i].text)
    return lst


"""Function to get the donut graph"""


def get_pie_chart(rating_list):
    labels = ['5 Stars', '4 Stars', '3 Stars', '2 Stars', '1 Stars']
    values = rating_list
    data = go.Figure(data=[go.Pie(labels=labels, values=values, hole=.4, hoverinfo='label+value', title='User Rating')])
    graphJSON = json.dumps(data, cls=plotly.utils.PlotlyJSONEncoder)

    return graphJSON


"""Function to get the reviews !"""


def get_review(commentsbox, search, flag=True):
    reviews = []
    for comment in commentsbox[:-1]:
        try:
            name = comment.find_all('p', {"class": "_2sc7ZR _2V5EHH"})[0].text
            # print("Name: ",name)
        except:
            name = "No user name found !"

        try:
            if (flag == True):
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
            if (comment_body.endswith('READ MORE')):
                comment_body = comment_body[:comment_body.find('READ MORE')]
            else:
                comment_body = comment_body

        except:
            comment_body = "No comments given by user !"

        """To get the date since user using this device !"""
        try:
            dt = comment.find_all('p', {'class': "_2sc7ZR"})[1].text
            # print(dt)
            if ("months" in dt):
                using_since = int(dt[:dt.find('months')])
                # print(using_since)
            else:
                dt = to_datetime(dt)
                today = to_datetime(datetime.datetime.today().strftime('%Y-%m-%d'))
                using_since = int((today - dt) / timedelta64(1, 'M'))

                # print(using_since)

            # print(using_since)
            # buyed_on = comment.find_all('p', {'class': "_2sc7ZR"})[1].text
            # print(buyed_on)

        except:
            using_since = "No information present !"

        my_dict = {"Product": search, "Name": name, "Rating": rating, "CommentHead": heading, "Comment": comment_body,
                   'Using Since': str(using_since) + " months"}

        reviews.append(my_dict)
    return (reviews)


""""Function to get the product info """


def get_product_info(temp_product_page, search, product_link):
    product_info = []
    try:
        product_name = temp_product_page.find_all('span', {'class': "B_NuCI"})[0].text
        product_name = product_name[:product_name.find('(')]
        # print(product_name)
    except:
        product_name = search

    try:
        product_overall_rating = temp_product_page.find('span', {'class': '_1lRcqv'}).div.text
        # print(product_overall_rating)
    except:
        product_overall_rating = "No Rating Available !"

    try:
        product_seller = temp_product_page.find_all('div', {'class': '_1RLviY'})[0].text
        product_seller_rating = product_seller[-3:]
        product_seller = product_seller[:-3]
        # print(product_seller_rating)
        # print(product_seller)
    except:
        product_seller = 'No Information Available About Product Seller'
        product_seller_rating = 'No Information Available About Product Seller Rating'

    # scrapping the image url from flipkart
    try:
        product_image_url = temp_product_page.find_all('div', {'class': 'q6DClP'})[0].attrs['style']
        product_image_url = product_image_url[product_image_url.find('(') + 1:-1].replace('128', '352')
        # print(product_image_url)

    except:
        product_image_url = 'No image availbel for ' + search

    try:
        product_price = temp_product_page.find_all('div', {"class": '_30jeq3 _16Jk6d'})[0].text
        # print(product_price)
    except:
        product_price = 'Not available'

    try:
        actual_product_price = temp_product_page.find_all('div', {'class': '_3I9_wc _2p6lqe'})[0].text
        # print(actual_product_price)
    except:
        actual_product_price = 'Not available'

    try:
        discount_on_product = temp_product_page.find_all('div', {'class': '_3Ay6Sb _31Dcoz'})[0].text
        # print(discount_on_product)
    except:
        discount_on_product = 'Not available'
    try:
        available_offer = temp_product_page.find_all('div', {'class': 'WT_FyS'})[0].text
        available_offer = available_offer.replace('T&C', '\n').replace('View Plans', '')
        # print(available_offer)

    except:
        available_offer = 'No Offer available for this product'
        # print(available_offer)

    try:
        currently_available = temp_product_page.find_all('button', {'class': '_2KpZ6l _2U9uOA ihZ75k _3AWRsL'})[0].text
        # print(currently_available)
        if (currently_available == ' BUY NOW'):
            currently_available = 'Yes'
        else:
            currently_available = 'Out Of Stock'
        # print(currently_available)
    except:
        currently_available = 'Out Of Stock'
        # print(currently_available)
    try:
        product_warranty = temp_product_page.find_all('div', {'class': '_352bdz'})[0].text.replace('Know More', '')
        # print(product_warranty)
    except:
        product_warranty = 'No Information Available'

    try:
        easy_payment_options = temp_product_page.find_all('div', {'class': '_250Jnj'})[0].text
        # print(easy_payment_options)
    except:
        easy_payment_options = "No Information Available"

    mydict = {"Product Name": product_name, "Product link": product_link, "Product Price": product_price,
              "Actual Product Price": actual_product_price, "Discount": discount_on_product,
              'currently_available': currently_available, "Product Image Url": product_image_url,
              "Produtct Seller": product_seller, "Seller Rating": product_seller_rating,
              "Product Rating": product_overall_rating, "Available_Offer": available_offer,
              "Easy Payment Options": easy_payment_options, 'product_warranty': product_warranty}

    product_info.append(mydict)

    return product_info