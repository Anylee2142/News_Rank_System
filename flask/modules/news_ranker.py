import MySQLdb as db
import pandas as pd
import numpy as np
import pickle
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from konlpy.tag import Twitter as t
from .naver_news_search import api_search

# def init_model():
#     return pickle.load(open('dataset/twitter_tfidf_mulnb_2018-04-22 20-17-55.pkl','rb'))

# def init_genre_matrix():
#     conn = db.connect(
#     "127.0.0.1",
#     "root",
#     '5555',
#     "news_rec",
#     charset='utf8',
#     )
#
#     view = pd.read_sql('SELECT * FROM VIEW', conn)
#     view['count'] = 1
#     article = pd.read_sql('SELECT * FROM article', conn)
#
#     merged = pd.merge(view, article,left_on='article_id', right_on='article_id')
#     merged = merged.loc[:,['user_id','article_id','area','count']]
#
#     return merged.pivot_table(values='count',index='user_id',columns='area',aggfunc=np.sum)

# Classification Engine, gerne matrix are loaded once at first when this module imorted
# model1 = init_model()
# genre_matrix = init_genre_matrix()

def go_get_article(crawling_list):
    import pandas as pd
    import time
    from bs4 import BeautifulSoup
    import requests

    article_list = []

    print('Naver api search started !')

    for idx, val in enumerate(crawling_list):
        html = val
        response = requests.get(html)
        web_elem = BeautifulSoup(response.content, 'html.parser')
        p_tags = web_elem.find_all('p')

        article = ''

        for each in p_tags:
            article += each.text

        article_list.append(article)

        if idx % 10 == 0:
            print('{} completed, {} total'.format(idx + 1, len(crawling_list)))

    print('completed !')

    return article_list

def trimming(articles):
    import re

    is_email = []
    for each in articles:
        tmp = re.findall('[^@]+@[^@]+\.[^@]+', each)
        is_email.append(tmp)

    is_email = [True if len(each) != 0 else False for each in is_email]
    upper_bound = len(
        is_email) - 2 - is_email[::-1].index(True) if True in is_email else len(is_email) - 1

    articles = [articles[idx] if not is_email[idx]
                else '' for idx in range(0, upper_bound)]

    # 2.
    for idx, val in enumerate(articles):
        converted = re.sub('[^가-힣0-9a-zA-Z.\\s]', ' ', val)
        articles[idx] = converted

    # 3.
    articles = [each for each in articles if each != '']

    return articles

def news_rank(user_id, genre_matrix, y_pred, y_prob):
    user_pref = genre_matrix.loc[user_id].sort_values(ascending=False).index

    print(user_id,"'s preference list = ",list(user_pref), '\n')

    article = []

    for area in range(0, 6):
        each_area = np.argwhere(y_pred == area)
        each_area = each_area.reshape(1, len(each_area))
        article.append(each_area)

    prob_df = pd.DataFrame(y_prob)
    sorted_article = []

    print('sorted by probability')

    for area, each in enumerate(article):
        sorter = prob_df.loc[each[0], :]
        sorter.sort_values(by=area, axis=0, inplace=True, ascending=False)
        sorted_article.append(list(sorter.index))

    for area in user_pref:
        print(area, sorted_article[area])

    news_rank = []
    area = ['정치','경제','사회','세계','생활문화','IT과학']
    for pref_area in user_pref:
        for each_article in sorted_article[pref_area]:

            news_rank.append((area[pref_area], each_article))

    return list(user_pref), news_rank

def news_rank_recommend(model1, genre_matrix, user_id, keyword, how_many):
#     model1 = init_model()

    searched_news = api_search(keyword, how_many)['items']

    title_list = [each_news['title'] for each_news in searched_news]
    crawling_list = [each_news['link'] for each_news in searched_news]

    crawled_searched_news = go_get_article(crawling_list)
    crawled_searched_news = [each.split('.') for each in crawled_searched_news]
    crawled_searched_news = [''.join(trimming(each)) for each in crawled_searched_news]

    news_content = pd.DataFrame(columns=['content'])
    X_test = pd.Series(crawled_searched_news)

    y_pred = model1.predict(X_test)
    y_prob = model1.predict_proba(X_test)

    user_pref, ranked_news = news_rank(user_id, genre_matrix, y_pred, y_prob)


    return user_pref, [('[{}] {}'.format(str(each[0]), title_list[each[1]]) ,crawling_list[each[1]]+'\n') for each in ranked_news]
