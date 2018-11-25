import api
import tweepy
from tweepy import OAuthHandler
import json
import csv
import pandas as pd
import http.client



########### language analysis #############
def language(dat):
    headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '1629a954ce0b4208ac575739c888e6b6',
            }

    documents = {"documents":[
                    {"id": '1',
                     "text":dat['text']}]}

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/languages",bytes(json.dumps(documents),encoding='utf8'),headers)
        response = conn.getresponse()
        data = response.read()
        lang = eval(data)['documents'][0]['detectedLanguages'][0]['iso6391Name']
        return lang
    except Exception as e:
        print(e)



########### sentiment analysis #############
def sentiment(dat):
    headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': '1629a954ce0b4208ac575739c888e6b6',
            }

    lang = language(dat)
    print(lang)

    documents = {"documents":[
                    {"language": lang,
                     "id": '1',
                     "text":dat['text']}]}

    try:
        conn = http.client.HTTPSConnection('westeurope.api.cognitive.microsoft.com')
        conn.request("POST", "/text/analytics/v2.0/sentiment",bytes(json.dumps(documents),encoding='utf8'),headers)
        response = conn.getresponse()
        data = response.read()
        dat['score'] = eval(data)['documents'][0]['score']
        conn.close()
    except Exception as e:
        print(e)
    
    dat['date'] = str(dat['date'])
    api.save_record(dat.to_dict())



########### historical data #############
def history_tweet(API,query,geo):
    date = '2018-10-10'

    # Open/Create a file to append data
    csvFile = open('./hist_data/'+date+'_'+query+'.csv', 'w+')
    csvWriter = csv.writer(csvFile)
    csvWriter.writerow(['time','text','coordinates'])
    dat=pd.DataFrame(columns=('date','text','pos'))

    for tweet in tweepy.Cursor(API.search,q=query,geocode=geo,since_id=date).items(1000):
        if tweet.coordinates:
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),tweet.coordinates])
            dat.loc[len(dat)+1]=[tweet.created_at,tweet.text,tweet.coordinates]
        else:
            csvWriter.writerow([tweet.created_at, tweet.text.encode('utf-8'),''])
        csvFile.close()
        for i in dat.index:
            sentiment(dat.iloc[i-1])
    
    

########### stream data #############
def stream_tweet(API,query,geo):
    class MyStreamListener(tweepy.StreamListener):  
     
        def on_status(self, status):
            if status.coordinates:
                dat=pd.DataFrame(columns=('date','text','pos'))
                dat.loc[0]=[status.created_at,status.text,status.coordinates]
                print(dat)
                sentiment(dat.loc[0])
                
        def on_error(self, status_code):
            if status_code == 420:
                #returning False in on_data disconnects the stream
                return False

    if __name__ == '__main__':
        myStream = tweepy.Stream(auth = api.auth, geocode=geo, lang="en", listener=MyStreamListener())
        myStream.filter(track=[query])



query = 'earthquake'
#geo = "32.522499,-117.046623,80km"
geo = "30.417,130.333,500km"
    
consumer_key='KazehWZWJGomblUjRQ5ktDKCj'
consumer_secret='Al8y01R3YzcEyiMdsHPTSDVsDHhdklBcazf9JHYjOhBP8CQYcp'
access_token='1066250199193014272-5HRp59qikUcuGtzB9ZU5sLPDaNK1Yd'
access_secret='CIyjAh3RsjzpOOWQyYnBe5mPlkH12drIUEIgy8KU6jb3u'

auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_secret)
API = tweepy.API(auth)

history_tweet(API,query,geo)