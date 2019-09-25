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
import time
import os

d=1
id_list= []

tweets = []



with open('Elon/elon_rtweets.txt', 'r') as f:
    for line in f:
        id_list.append(line)
        



strname  = 'Elon/' + id_list[19].rstrip('\n') 
file = strname + '_tweets.json'


with open (file) as f:
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
numbers =0
for id_str in id_list[3:]:
    strname  = 'Elon/' + id_str.rstrip('\n') 
    file = strname + '_tweets.json'


    with open (file) as f:
        for line in f:
            tweets.append(json.loads(line))


    rtwt = []
    cnt =0
    file2 = strname + '_retweeters.txt'
    if (os.path.exists(file2)==False):
        for twt in tweets:
            rtid = twt['id_str']
            rts = api.GetRetweeters(rtid)
            rtwt = rtwt + rts
            cnt = cnt+1
            #print (cnt)
            if(cnt>74): 
                break
        #file2 = strname + '_retweeters.txt'        
        with open(file2, 'w') as f:
            for item in rtwt:
                f.write("%s\n" % item)
        time.sleep(960)
    numbers = numbers+1
    print(numbers)
    
    #print (rtwt)