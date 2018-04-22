from flask import Flask, render_template, request, jsonify

from modules.crawling_to_db import *
from modules.model_training import *
from modules.news_ranker import *

import pandas as pd

app = Flask(__name__)

model = pickle.load(open('models/twitter_tfidf_mulnb_2018-04-22 20-17-55.pkl','rb'))

@app.route('/test')
def wow():
    return 'Server works just fine'

@app.route('/post_test')
def post_test():
    return render_template('test.html')

@app.route('/test1',methods=['POST'])
def test1():
    print(request.values.get('name'))
    print(request.values.get('email'))
    print(request.values.get('password'))

    return render_template('test.html')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/test2',methods=['GET'])
def test2():
    id = request.values.get('id')
    pw = request.values.get('pw')

    keyword = request.values.get('keyword')
    how_many_pages = request.values.get('number_page')

    # Searching news with Naver API
    raw = api_search(keyword, how_many_pages)['items']
    searched = [(each['title'], each['link']) for each in raw]

    # Find user_id from ID, PW

    # Ranking news from user_id

    # Return ranked news

    return jsonify(searched)

@app.route('/news_rank',methods=['GET'])
def news_rank():

    keyword = request.values.get('sentence')

    print(request.values.get('sentence'))

    return render_template('index_tmp.html')


if __name__=='__main__':
    app.run(host='0.0.0.0')
