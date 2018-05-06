# News Rank system with NLP classification
> ### Provide list of seached news based on user's preference

- **Tools**
  - Selenium, Naver API
  - Scikit-learn, KoNLPy
  - Flask, AWS
  - MySQL

  
## Data Collection + Model Training

<img src='img/news_rec.png'>

## News Rank

<img src='img/news_rank.png'>


## 뉴스검색 + 뉴스랭크
> #### 0. 유저로부터 웹에서 키워드를 입력받음	
> #### 1. 네이버 api 사용하여 뉴스검색
> #### 2. 모델 pickle로 불러온 후 전처리된 뉴스의 분야분류
> #### 3. 유저가 자주 보던 분야 순으로 검색결과제공

## AWS, flask와 연동
> #### 0. 데이터 수집부터 뉴스랭크까지 모듈화하여 flask와 연결
> #### 1. 검색어 입력 페이지 작성 후 flask와 연결
> #### 2. 위 둘을 AWS에 올림
> #### 3. 실제 유저들에 대한 데이터가 없으므로 Seed를 사용