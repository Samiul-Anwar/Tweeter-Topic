import json
import string
import re
from pymongo import MongoClient
from bson.json_util import loads, dumps
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
from stop_words import get_stop_words
from nltk.tokenize import RegexpTokenizer
import nltk
import importlib
#import t
import twitter
from t import *
import os
import enchant

dic1 = enchant.Dict('en_US')
dic2 = enchant.Dict('en_UK')


rmvlist = ['amp', 'de', 'en', 'un', 'el']

dir = 'Gates/'

def get_tweets(api=None, id=None):
    timeline = api.GetUserTimeline(user_id=id,count=200,exclude_replies=True)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    #print("getting tweets before:", earliest_tweet)
    return timeline
    while True:
        tweets = api.GetUserTimeline(
           user_id=id, max_id=earliest_tweet, count=200, exclude_replies=True
        )
        new_earliest = min(tweets, key=lambda x: x.id).id

        if not tweets or new_earliest == earliest_tweet:
            break
        else:
            earliest_tweet = new_earliest
            #print("getting tweets before:", earliest_tweet)
            timeline += tweets

    return timeline











def getUpdatedWeights(topic, d,k, l, rtid, api, Ol, Nt):
    #tweets = get_tweets(api = api, id = rtid)
    #tweets = api.GetUserTimeline(user_id=rtid,count=200,exclude_replies=True)
    #print(len(tweets))
    tweets = []
    filename = dir+ rtid + '_tweets.json'
    if os.path.exists(filename):
        with open (filename) as f:
            for line in f:
                tweets.append(json.loads(line))
    outlink =0
    stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
    nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
    nltk_words.append('rt')
    nltk_words = nltk_words + rmvlist
    stop_words.extend(nltk_words)
    #old_topic = {}
    d1=d
    if (k==l):
        d1=1
    rts = []
    output = []
    bgrmtoken = []
    for twt in tweets[:100]:
       # rtweet = json.dumps(tt._json)
       # twt = json.loads(rtweet)
        if (twt['text'].startswith("RT ")):
            outlink = outlink + 1


       # rts.append(api.GetRetweeters(twt['id_str']))  
       # print(twt['id_str'])
        #print(twt['retweet_count'])
        text = twt['text']
        text = re.sub(r'[^\w\s]','',text)
        tokens = word_tokenize(text)

        ##******************#############
        if 'entities' in twt:
            htag = twt['entities']['hashtags']
        #print(htag)
        ##******************#############

        ##******************#############
        for ht in htag:
            #print(ht['text'])
            htv = re.sub(r'[^\w\s]','',ht['text'])
            if((htv in tokens)==False):
                tokens.append(htv)
        ##******************#############


        for words in tokens:
            words = words.lower()
            if(((words in topic) == False) and (len(words)>1)):
            #if(((words in topic) == False) and ((dic1.check(words)==True) or  (dic2.check(words)==True))):
                pos = nltk.pos_tag([words])
                if (((words in stop_words)==False) and (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG')):
                    #print(k)
                    topic[words] = 0
                    bgrmtoken.append(words)
                    
        
            elif(((words in topic) == True)):# and ((words in output)==False)):       #print (words )
                output.append(words)
                bgrmtoken.append(words)
        #break
        
   # print (rts)

    ############*********************#############
    bigrm = list(nltk.bigrams(bgrmtoken))

    for item in bigrm:
        newtp = item[0] + item[1]
        newtp = newtp.lower()
        if ((newtp in topic)==False):
            topic[newtp] = 0
        else:
            #print(newtp)
            output.append(newtp)
    ############*********************#############
    

    file2 = dir + rtid + '_retweeters.txt'
    if os.path.exists(file2):
        with open(file2, 'r') as f:
            for line in f:
                line = line[:-1]
                rts.append(line)
    Ol = Ol*outlink
    for wrd in output:
        topic[wrd] = topic[wrd] + (((1-d)**k)/Ol)*(d1/Nt) 
    if(k==l):
        return topic
    for rid in rts:
        topic= getUpdatedWeights(topic, d,k+1, l, rid, api, Ol, Nt)
        #break
    
    return topic