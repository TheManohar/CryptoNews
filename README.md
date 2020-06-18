# CryptoNews
CryptoNews is a project based on `Flask` and `Dash`. The main parts of the project are: <br>
**ETL**: collecting the latest news about crypto from various news sources to a `MySQL` database. <br>
**Data Analysis**: performing a sentiment analysis on headlines and description of articles, by using `vaderSentiment`. <br>
**Dashboard**: display the average sentiment score for the collected articles and how many were evaluated.

# Dashboard Elements
The live dashboard is available on: [http://msitapati.pythonanywhere.com](http://msitapati.pythonanywhere.com)
## Sentiment Analysis
![avg_scores.png](avg_scores.png)
With the use of `vaderSentiment` I have analysed headline, description and content extract of all the articles and averaged these scores into one main sentiment score. This score goes from -100% for the most negative possible news sentiment up to +100% for a perfectly positive sentiment score on the news

## Daily Articles Count
![articles_count.png](articles_count.png)
This is a simple barchart displaying the count for how many times a crypto-related keyword has been mentioned in news headlines for a given day

# Project Scripts
![crypto_news.png](crypto_news.png)
This is how the data moves within this project So tahat you can see the final resulting dashboard.

## ETL Scripts:
1) `main.py`: main scrip that runs the ETL and Data Analysis scripts every 3600 seconds (1 hour)
2) `extract.py`: fetching the latest news from newsapi.org for the keywords: crypto, bitcoin and ethereum <br>
3) `transform.py`: data parsing <br>
4) `load.py`: load parsed data into MySQL server <br>

## Data Analysis Scripts:
1) `db_dump.py`: convert a complete copy of the artcles table into a DataFrame and dumps it into .pkl format <br>
2) `data_analysis.py`: performs: data cleaning, Sentiment Analysis and prepares a daily resampling of the data <br>

## Dashboard Scripts:
1) `dash_app.py`: script to setup the layout and plotly graphs necessary to generate the dashboard <br>
2) `flask_app.py`: an API based on Flask. It collects and displays the latest news in json format <br>
