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



api = twitter.Api(
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key= ACCESS_TOKEN_KEY, access_token_secret=ACCESS_TOKEN_SECRET
    )

with open('Leo/leo_rtweets.txt', 'r') as f:
    for line in f:
        line = line[:-1]
        sts = get_tweets(api = api, id = line)
        filename = 'Leo/' + line +'_tweets.json'
        print(filename)
        with open(filename, 'w+') as f:
            for tweet in sts:
                f.write(json.dumps(tweet._json))
                f.write('\n')
        
