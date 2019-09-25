import json
import string
import re
from pymongo import MongoClient
from bson.json_util import loads, dumps
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
import importlib
#import t
import twitter
from t import *
from utility import *

d=1
tweets = []
file1 = 'Elon/elon_tweets.json'
with open (file1) as f:
    for line in f:
        tweets.append(json.loads(line))
   # try:
       # record = result.next()
      #  print(record['text'])
   # except StopIteration:
       # print("Empty cursor!")
    #break


api = twitter.Api(
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key= ACCESS_TOKEN_KEY, access_token_secret=ACCESS_TOKEN_SECRET
    )

rts = []
cnt =0;
for twt in tweets[:100]:
    if(twt['text'].startswith('RT ')):
        #print(twt)
       
        if 'entities' in twt:
            if 'user_mentions' in twt['entities']:
                if twt['entities']['user_mentions']:
                    rts.append(twt['entities']['user_mentions'][0]['id_str'])
                    #print (rts)
    

with open('Elon/elon_rtweets.txt', 'w') as f:
    for item in rts:
        f.write("%s\n" % item)
        #print ('N')
   # rts = api.GetRetweeters(rtid)
    
#print (rtwt)