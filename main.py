import pandas as pd
import datetime 
import yfinance as yf
import matplotlib.pyplot as plt

from pandas.plotting import scatter_matrix
# %matplotlib inline
from newspaper import Article
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
import nltk
nltk.download('punkt')

def load_urls(urls):
    f = open('urls.txt','r')
    lines = f.readlines()
    key = lines[0]
    i = 0
    temp = []

    for line in lines:
        if len(line) < 15 :
            i = 0
            key = line.strip('\n')
            temp = []
        else:
            temp.append(line.strip('\n'))
            urls[key] = temp        
        i+=1 
def load_article(company,urls):
    
    items = urls[company]
    text =''
    article_contents = []
    
    for item in items:
        text = ''
        toi_article = Article(item, language='en')
        #To download the article
        toi_article.download()
        
        #To parse the article
        toi_article.parse()
        
        #To perform natural language processing ie..nlp
        toi_article.nlp()
        
        #To extract title
        text += toi_article.title
        text += ' '
        text += toi_article.text
        article_contents.append(text)
    
    return article_contents
            
def calculate_sentiment_analysis(company_articles):
    
    sid_obj = SentimentIntensityAnalyzer()
    scores = []
    for item in company_articles:
        sentiment_dict = sid_obj.polarity_scores(item)
        scores.append(sentiment_dict)
    
    return scores

def calculate_sentiment_analysis_avg(company):
    avg_pos = 0.0
    avg_neg = 0.0
    avg_neu = 0.0

    for item in company:
        avg_neg+=item['neg']
        avg_pos+=item['pos']
        avg_neu+=item['neu']
            
    avg_neg = avg_neg/len(company)
    avg_neu = avg_neu/len(company)
    avg_pos = avg_pos/len(company)
    return avg_pos, avg_neg,avg_neu

    
def show_stock_prices():
    start = "2021-04-01"
    end = '2021-5-01'
    goog = yf.download('GOOG',start,end)
    amzn = yf.download('AMZN',start,end)
    msft = yf.download('MSFT',start,end)
    aapl = yf.download('AAPL',start,end)
    wmt = yf.download('WMT',start,end)
    goog['Open'].plot(label = 'Google',figsize = (15,7))
    # for i in goog['Open']:
    #     plt.text(i)
    amzn['Open'].plot(label = 'Amazon')
    msft['Open'].plot(label = 'Microsoft')
    # aapl['Open'].plot(label = 'Apple')
    # wmt['Open'].plot(label = 'Walmart')
    plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
    plt.title('Stock Prices of GOOG, AMZN, MSFT, AAPL and WMT')
    plt.show()   

        
       
if __name__ == '__main__':
    urls = {}
    google = [] 
    amazon = []
    microsoft = []
    apple = []
    walmart = []
    
    load_urls(urls)
    
    google = load_article('Google', urls)
    # amazon = load_article('Amazon', urls)
    # microsoft = load_article('Microsoft', urls)
    # apple = load_article('Apple', urls)
    # walmart = load_article('Walmart', urls)
    
    google = calculate_sentiment_analysis(google)
    avg_pos,avg_neg,avg_neu = calculate_sentiment_analysis_avg(google)

    print("Google was rated as ", avg_neg*100, "% Negative")
    print("Google was rated as ", avg_neu*100, "% Neutral")
    print("Google was rated as ", avg_pos*100, "% Positive")
    
    show_stock_prices()
