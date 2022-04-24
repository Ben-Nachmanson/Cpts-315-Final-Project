import yfinance as yf
import matplotlib.pyplot as plt
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

def calculate_percent_change(company):
    
    pChange = (company['Open'][-1] - company['Open'][0])/company['Open'][0]  
    
    return round(pChange*100,2)
    
def plot_stock_prices():
    start = "2021-04-01"
    end = '2021-5-01'
    
    goog = yf.download('GOOG',start,end)
    pChangeGoogle = calculate_percent_change(goog) 
         
    amzn = yf.download('AMZN',start,end)
    pChangeAmazon = calculate_percent_change(amzn)      

    msft = yf.download('MSFT',start,end)
    pChangeMicrosoft = calculate_percent_change(msft)      

    aapl = yf.download('AAPL',start,end)
    pChangeApple = calculate_percent_change(aapl)      

    wmt = yf.download('WMT',start,end)
    pChangeWalmart = calculate_percent_change(wmt)      

    
    plot1 = plt.figure("Google")
    goog['Open'].plot(label = 'Google')
    plt.title("Google Stock Price "+ "("+ str(pChangeGoogle) +"%"+')' )
    plt.ylabel("Price")
      
    plt.legend(loc = "lower right")
  
    plt.text('2021-04-1',2370, str(round(avg_pos_google*100,2)) +"% Positive, "+ str(round(avg_neu_google*100,2)) +"% Neutral, " + str(round(avg_neg_google*100,2))+"% Negative")
    plt.text('2021-04-1',2390, "Sentiment Analysis of Google CNN articles")
    
    plot2 = plt.figure("Amazon")
    amzn['Open'].plot(label = 'Amazon')
    plt.title("Amazon Stock Price "+ "("+ str(pChangeAmazon) +"%"+')')
    plt.ylabel("Price")
    
    plt.legend(loc = "lower right")
    
    plt.text('2021-04-1',3460, str(round(avg_pos_amazon*100,2)) +"% Positive, "+ str(round(avg_neu_amazon*100,2)) +"% Neutral, " + str(round(avg_neg_amazon*100,2))+"% Negative")
    plt.text('2021-04-1',3490, "Sentiment Analysis of Amazon CNN articles")
    
    plot3 = plt.figure("Microsoft")
    msft['Open'].plot(label = 'Microsoft')
    plt.title("Microsoft Stock Price "+ "("+ str(pChangeMicrosoft) +"%"+')')
    plt.ylabel("Price")
    
    plt.legend(loc = "lower right")
  
    plt.text('2021-04-1',258, str(round(avg_pos_microsoft*100,2)) +"% Positive, "+ str(round(avg_neu_microsoft*100,2)) +"% Neutral, " + str(round(avg_neg_microsoft*100,2))+"% Negative")
    plt.text('2021-04-1',260, "Sentiment Analysis of Microsoft CNN articles")
    
    plot4 = plt.figure("Apple")
    aapl['Open'].plot(label = 'Apple')
    plt.title("Apple Stock Price "+ "("+ str(pChangeApple) +"%"+')')
    plt.ylabel("Price")

    plt.legend(loc = "lower right")
    
    plt.text('2021-04-1',135, str(round(avg_pos_apple*100,2)) +"% Positive, "+ str(round(avg_neu_apple*100,2)) +"% Neutral, " + str(round(avg_neg_apple*100,2))+"% Negative")
    plt.text('2021-04-1',136, "Sentiment Analysis of Apple CNN articles")
    
    plot5 = plt.figure("Walmart")
    wmt['Open'].plot(label = 'Walmart')
    plt.title("Walmart Stock Price "+ "("+ str(pChangeWalmart) +"%"+')')
    plt.ylabel("Price")
    
    plt.legend(loc = "lower right")

    plt.text('2021-04-1',140, str(round(avg_pos_walmart*100,2)) +"% Positive, "+ str(round(avg_neu_walmart*100,2)) +"% Neutral, " + str(round(avg_neg_walmart*100,2))+"% Negative")
    plt.text('2021-04-1',140.5, "Sentiment Analysis of Walmart CNN articles")

    plt.show()        
       
if __name__ == '__main__':
    urls = {}
    google = [] 
    amazon = []
    microsoft = []
    apple = []
    walmart = []
    
    load_urls(urls)
    
    print()
    print("Urls loaded")
    google = load_article('Google', urls)
    amazon = load_article('Amazon', urls)
    microsoft = load_article('Microsoft', urls)
    apple = load_article('Apple', urls)
    walmart = load_article('Walmart', urls)
    
    print()
    print("Articles loaded")
    print()
    
    print("Calculating Sentiment Analysis...")
    google = calculate_sentiment_analysis(google)
    avg_pos_google,avg_neg_google,avg_neu_google = calculate_sentiment_analysis_avg(google)
    
    amazon = calculate_sentiment_analysis(amazon)
    avg_pos_amazon,avg_neg_amazon,avg_neu_amazon = calculate_sentiment_analysis_avg(amazon)

    microsoft = calculate_sentiment_analysis(microsoft)
    avg_pos_microsoft,avg_neg_microsoft,avg_neu_microsoft = calculate_sentiment_analysis_avg(microsoft)

    apple = calculate_sentiment_analysis(apple)
    avg_pos_apple,avg_neg_apple,avg_neu_apple = calculate_sentiment_analysis_avg(apple)

    walmart = calculate_sentiment_analysis(walmart)
    avg_pos_walmart,avg_neg_walmart,avg_neu_walmart = calculate_sentiment_analysis_avg(walmart)
   
    plot_stock_prices()
