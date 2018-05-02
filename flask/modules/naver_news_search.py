import os
import sys
import urllib.request
import json

def api_search(keyword, how_many):
    with open('/home/ej/github/naver_api_info.txt', 'r') as f:
        client_id = str(f.readline().replace('\n',''))
        client_secret = str(f.readline().replace('\n',''))

    encText = urllib.parse.quote(keyword)
    encDisp = urllib.parse.quote(str(how_many))
    url = "https://openapi.naver.com/v1/search/news?query={}&display={}".format(encText, encDisp)
    # url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id", client_id)
    request.add_header("X-Naver-Client-Secret", client_secret)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode == 200):
        response_body = response.read()
        return json.loads(response_body.decode('utf-8'))
    else:
        print('Response without code 200')
        return None
