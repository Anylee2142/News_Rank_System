# News Rank system with NLP classification
> ### Provide sorted list of seached news based on user's preference

- What i did
	> ### Data Collection + Model Training
	> ### News Rank (Training news data to classify future news, and sort them as user preferences)
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
| Politic      	| 0.92      	| 0.94   	| 0.93     	| 975     	|
| Economy      	| 0.88      	| 0.89   	| 0.88     	| 958     	|
| Society      	| 0.93      	| 0.89   	| 0.91     	| 958     	|
| World      	| 0.95      	| 0.93   	| 0.94     	| 943     	|
| Living&Culture  	| 0.93      	| 0.93   	| 0.93     	| 971     	|
| IT/Science    	| 0.93      	| 0.94   	| 0.94     	| 916     	|
| avg/total 	| 0.92      	| 0.92   	| 0.92     	| 5721    	|

