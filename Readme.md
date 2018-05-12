# News Rank system with NLP classification
> ### Provide sorted list of seached news based on user's preference

- What i did
	> ### Data Collection + Model Training
	> ### News Rank
	> ### Associate with Flask + AWS

- **Tools**
  - Selenium, Naver API
  - Scikit-learn, KoNLPy
  - Flask, AWS
  - MySQL

  
## Data Collection + Model Training 

<img src='img/news_rec.png'>

## News Rank
> ### Provide sorted list of news based on user's preference

<img src='img/news_rank.PNG'>

## Associate with Flask + AWS

<img src='img/news_aws.PNG'>

## Performance (3-Fold CV)

|           	| precision 	| recall 	| F1-Score 	| support 	|
|:---------:	|-----------	|--------	|----------	|---------	|
| 정치      	| 0.92      	| 0.94   	| 0.93     	| 975     	|
| 경제      	| 0.88      	| 0.89   	| 0.88     	| 958     	|
| 사회      	| 0.93      	| 0.89   	| 0.91     	| 958     	|
| 세계      	| 0.95      	| 0.93   	| 0.94     	| 943     	|
| 생활문화  	| 0.93      	| 0.93   	| 0.93     	| 971     	|
| IT과학    	| 0.93      	| 0.94   	| 0.94     	| 916     	|
| avg/total 	| 0.92      	| 0.92   	| 0.92     	| 5721    	|

