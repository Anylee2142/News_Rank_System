from selenium import webdriver
import pandas as pd
from datetime import datetime
from multiprocessing import Process
from os import makedirs as mk
from os import path as pt
from os import listdir
from os.path import isfile, join
import time
import MySQLdb as db
import sys

def crawling(area,driver, count, cur_time):
    articles = driver.find_element_by_css_selector('#section_body')
    article_list = articles.find_elements_by_css_selector(
        'dl > dt:nth-child(2) > a')
    href_list = [each.get_attribute('href') for each in article_list]

    title_list = [each.text for each in article_list]

    for idx, article in enumerate(href_list):
        driver.get(article)
        article_body = driver.find_element_by_id('articleBodyContents')
        time.sleep(0.5)

        posted_time = driver.find_element_by_class_name('t11')
        content = article_body.text
        file_name = '{}/{}-{}.txt'.format(area, count,
                                          posted_time.text.replace(':', '-'))

        dest_path = '{}/{}/{}'.format('crawling',cur_time, file_name)
        with open(dest_path, 'w', encoding='UTF-8') as f:
            title = '\t'+title_list[idx] + '\n\n'
            f.write(title + content)

        count += 1

    return count

def get_page_buttons(driver):
    page_buttons = driver.find_elements_by_class_name('_paging')
    return [each.get_attribute('href') for each in page_buttons]

def how_many_pages_to_crawl(area, driver,cur_time, count, page_counts):
    if page_counts == 0:
        print('Insert more than 0')
        return

    buttons = get_page_buttons(driver)
    count += crawling(area,driver,count, cur_time)
    page_counts -= 1
    print('\t','remaining page = ' + str(page_counts))

    idx = 0
    while page_counts:
        # idx 페이지로 이동
        driver.get(buttons[idx])

        # 다음 버튼이면
        if idx == 9:
            buttons = get_page_buttons(driver,)
            idx = 0
            count += crawling(area,driver,count,cur_time)

        # 다음 버튼이 아니면
        else:
            count += crawling(area,driver,count,cur_time)
            idx += 1

        page_counts -= 1
        print('\t','remaining page = ' + str(page_counts))

    return count

def do_job(area, cur_time, how_many_pages = 20):
    options = webdriver.ChromeOptions()
    options.add_argument('headless')
    options.add_argument("--disable-gpu")
    options.add_argument('log-level=3')

    driver = webdriver.Chrome('chromedriver.exe', chrome_options=options)

    count = 0

    for each in area:
        area_link = each[0]
        area_str = each[1]

        driver.get(area_link)
        print(area_str,' Crawling Started')

        count = how_many_pages_to_crawl(area_str, driver, cur_time, count ,how_many_pages)
        print('\t','counts of crawling = ',count)

        count = 0

def mk_dir(new_path):
    path = ['정치','경제','사회','세계','생활문화','IT과학']

    if not pt.exists(new_path):
        mk(new_path)
        for area in path:
            mk('{}/{}'.format(new_path,area))

def trimming(file_name):
    # 1. 역순으로 제일 먼저 찾은 이메일 밑으로 다 없앰
    # 2. 나머지 특수문자들 다 없앰 (. 빼고)
    # 3. 공백문자열 다 없앰
    import re
    with open(file_name,'r',encoding='utf8') as f:
        articles = f.readlines()

    # 1.
    is_email = []
    for each in articles:
        tmp = re.findall('[^@]+@[^@]+\.[^@]+', each)
        is_email.append(tmp)

    is_email = [True if len(each)!=0 else False for each in is_email]
    upper_bound = len(is_email) - 2 - is_email[::-1].index(True) if True in is_email else len(is_email)-1

    articles = [articles[idx] if not is_email[idx] else '' for idx in range(0,upper_bound)]

    # 2.
    for idx, val in enumerate(articles):
        converted = re.sub('[^가-힣0-9a-zA-Z.\\s]', ' ', val)
        articles[idx] = converted

    # 3.
    articles = [each for each in articles if each != '']

    return articles

def raw_to_preprocessed(folder_name):
    path = ['정치','경제','사회','세계','생활문화','IT과학']

    print('Preprocess Started')
    for each in path:
        crawling_path = '{}/{}/{}'.format('crawling',folder_name,each)
        file_names = [f for f in listdir(crawling_path) if isfile(
            join(crawling_path, f)) and f.endswith(".txt")]
        # 파일이름

        full_names = ['{}/{}'.format(each, tmp) for tmp in file_names]
        # 영역/파일이름

        crawling_path = ['{}/{}/{}'.format('crawling',folder_name, tmp) for tmp in full_names]
        # crawling/영역/파일이름
        for idx, file_name in enumerate(crawling_path):
            trimmed = trimming(file_name)
            trimmed = ''.join(trimmed)

            dest_path = '{}/{}/{}'.format('preprocess',folder_name,full_names[idx])

            with open(dest_path, 'w', encoding='utf-8') as f:
                f.write(trimmed)

        print('\t',each, ' completed !')

    print('Preprocess Completed\n')

def load_whole_preprocessed(folder_name):
    path = [('정치',0), ('경제',1), ('사회',2), ('세계',3), ('생활문화',4), ('IT과학',5)]
    total_df = pd.DataFrame(columns=['content','area'])

    def date_trimmer(raw_date):
        tmp = raw_date.split('/')[-1].replace('.txt',':00')
        tmp = tmp.split()
        return '-'.join(tmp[0].split('-')[1:]) + ' ' + tmp[1].replace('-',':')

    print('loading preprocessed started')

    for each in path:
        preprocess_path = '{}/{}/{}'.format('preprocess',folder_name,each[0])
        file_names = [f for f in listdir(preprocess_path) if isfile(
            join(preprocess_path, f)) and f.endswith(".txt")]
        full_names = ['{}/{}'.format(preprocess_path, tmp) for tmp in file_names]

        contents = []
        written_date = []

        df = pd.DataFrame(columns=['content','area'])

        for file_name in full_names:

            with open(file_name, 'r', encoding='utf-8') as f:
                contents.append(f.read())
                written_date.append(file_name)

        df['content'] = pd.Series(contents)
        df['area'] = each[1]
        df['written_date'] = pd.Series(written_date)
        df['written_date'] = df['written_date'].apply(date_trimmer)
        df['title'] = df['content'].apply(lambda x: x.split('\n')[0].replace('\t',''))

        df = df[['title','content','written_date','area']]

        total_df = total_df.append(df)
        print('\t',each,' completed !')

    print('loading preprocessed completed\n')

    return total_df

def preprocessed_to_db(data):
    conn = db.connect(
        '127.0.0.1',
        'root',
        '5555',
        'news_rec',
        charset='utf8')

    print('Preprocessed to db started')


    # article to DB
    curs = conn.cursor()
    for idx, val in data.iterrows():
        area = val['area']
        title = "'{}'".format(val['title'])
        content = "'{}'".format(val['content'].replace('\n', ''))
        date = "'{}'".format(val['written_date'])

        sql = 'INSERT INTO Article(area, title, content, written_date) VALUES({},{},{},{});'.format(
            area, title, content, date)

        curs.execute(sql)
        conn.commit()
    print('Preprocessed to db completed')

def do_crawl(how_many_pages):
    politic = 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=100'
    economy = 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=101'
    society = 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=102'
    culture = 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=103'
    world = 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=104'
    science = 'http://news.naver.com/main/main.nhn?mode=LSD&mid=shm&sid1=105'

    area = [(politic, '정치'), (economy, '경제'), (society, '사회'),
            (culture, '생활문화'), (world, '세계'), (science, 'IT과학')]


    p1 = Process(target=do_job, args=(area[:3],cur_time, how_many_pages))
    p1.start()
    p2 = Process(target=do_job, args=(area[3:],cur_time, how_many_pages))
    p2.start()

    while True:
        time.sleep(5)
        if p1.exitcode != None and p2.exitcode != None:
            print('crawling completed !\n')
            break

if __name__ == '__main__':
    # python crawling_to_db.py YOUR_PAGE_COUNTS
    cur_time = datetime.now().strftime('%Y-%m-%d %H-%M-%S')

    mk_dir('{}/{}'.format('crawling',cur_time))

    how_many_pages = 20 if len(sys.argv)<=1 else int(sys.argv[1])
    do_crawl(how_many_pages)

    mk_dir('{}/{}'.format('preprocess',cur_time))

    raw_to_preprocessed(cur_time)

    preprocessed_to_db(load_whole_preprocessed(cur_time))
