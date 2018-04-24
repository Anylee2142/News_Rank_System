from flask import Flask, render_template, request, jsonify
from modules.news_ranker import *

# from konlpy.tag import Twitter as t
import pandas as pd
import numpy as np
import MySQLdb as db
import pickle

app = Flask(__name__)

# def tagger(doc):
#     pos_tagger = t()
#     return ["/".join(t) for t in pos_tagger.pos(doc)]

def init_server(conn):
    model = pickle.load(open('models/twitter_tfidf_mulnb_2018-04-24 18-40-35.pkl','rb'))

    view = pd.read_sql('SELECT * FROM VIEW', conn)
    view['count'] = 1
    article = pd.read_sql('SELECT * FROM article', conn)
    merged = pd.merge(view, article,left_on='article_id', right_on='article_id')
    merged = merged.loc[:,['user_id','article_id','area','count']]
    genre_matrix = merged.pivot_table(values='count',index='user_id',columns='area',aggfunc=np.sum)

    return model, genre_matrix

model, genre_matrix = init_server(db.connect(
"127.0.0.1",
"root",
'5555',
"news_rec",
charset='utf8'))

@app.route('/test')
def test():
    return 'Server works just fine'

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/news_rank',methods=['POST'])
def news_rank():
    conn = db.connect(
    "127.0.0.1",
    "root",
    '5555',
    "news_rec",
    charset='utf8')

    id = request.values.get('id')
    pw = request.values.get('pw')
    keyword = request.values.get('keyword')
    how_many_pages = request.values.get('number_page')

    # Find user_id from ID, PW
    curs = conn.cursor()
    curs.execute("SELECT user_id FROM user WHERE id='{}' AND pw='{}'".format(id,pw))
    user_id = curs.fetchone()[0]

    print(genre_matrix.loc[user_id])

    # Ranking news from user_id
    user_pref, ranked_news = news_rank_recommend(model, genre_matrix, user_id, keyword, how_many_pages )

    # Handling for Disallowed key characters
    ranked_news = [(each[0],each[1].replace('amp;','')) for each in ranked_news]

    # Return ranked news
    return render_template('news_rank.html',RANKED_NEWS=ranked_news, ID=id)

if __name__=='__main__':
    def tagger(doc):
        pos_tagger = t()
        return ["/".join(t) for t in pos_tagger.pos(doc)]

    app.run(host='0.0.0.0')
