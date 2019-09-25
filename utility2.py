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


def get_tweets(api=None, id=None):
    timeline = api.GetUserTimeline(user_id=id,count=200,exclude_replies=True)
    earliest_tweet = min(timeline, key=lambda x: x.id).id
    #print("getting tweets before:", earliest_tweet)

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











def getUpdatedWeights(topic,  d,k, l, rtid, api,Il, Ol, Nt):
    #tweets = get_tweets(api = api, id = rtid)
    #tweets = api.GetUserTimeline(user_id=rtid,count=200,exclude_replies=True)
    #print(len(tweets))
    tweets = []
    filename = 'Gates/'+ rtid + '_tweets.json'
    if os.path.exists(filename):
        with open (filename) as f:
            for line in f:
                tweets.append(json.loads(line))
    outlink =1
    inlink = 1
    stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
    nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
    nltk_words.append('rt')
    
    stop_words.extend(nltk_words)
    #old_topic = {}
    d1=d
    if (k==l):
        d1=1
    rts = []
    output = []
    for twt in tweets[:100]:
       # rtweet = json.dumps(tt._json)
       # twt = json.loads(rtweet)
        if (twt['text'].startswith("RT ")):
            outlink = outlink + 1
        inlink = inlink + twt['retweet_count']

        text = twt['text']
        text = re.sub(r'[^\w\s]','',text)
        tokens = word_tokenize(text)
        
        for words in tokens:
            words = words.lower()
           # if(((words in topic) == False) and  ((words in nltk.corpus.words.words())==True)):
            if(((words in topic) == False) and ((dic1.check(words)==True) or  (dic2.check(words)==True))):
                pos = nltk.pos_tag([words])
                if (((words in stop_words)==False) and (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG')):
                    #print(k)
                    topic[words] = 0  # don't add anymore

            elif ((words in topic) == True):
                #print(words)
                if(topic[words]!=0):  #### needs change
                    output.append(words)
        
        
  

    

    
    #Ol = Ol*outlink

    if(k%2==1):
        Ol = Ol*outlink
        Il = Il*inlink
        for wrd in output:
            topic[wrd] = topic[wrd] + (((1-d)**k)/Ol)*(d1/(2*Nt)) 
            #hub[wrd] = hub[wrd] + (((1-d)**l)/Il)*(d1/(2*Nt)) 
    else:
        Ol = Ol*inlink
        Il = Il*outlink
        for wrd in output:
            topic[wrd] = topic[wrd] + (((1-d)**k)/Ol)*(d1/(2*Nt)) 
            #hub[wrd] = hub[wrd] + (((1-d)**l)/Il)*(d1/(2*Nt)) 

    if(k==1):
        return topic

    file2 = 'Gates/' + rtid + '_retweeters.txt'
    if os.path.exists(file2):
        with open(file2, 'r') as f:
            for line in f:
                line = line[:-1]
                rts.append(line)
    for rid in rts:
        topic = getUpdatedWeights(topic, d,k+1, l, rid, api,Il, Ol, Nt)
        #break
    
    return topic




def getUpdatedWeights2(hub,  d,k, l, rtid, api,Il, Ol, Nt):
    #tweets = get_tweets(api = api, id = rtid)
    #tweets = api.GetUserTimeline(user_id=rtid,count=200,exclude_replies=True)
    #print(len(tweets))
    tweets = []
    filename = 'Elon/'+ rtid + '_tweets.json'
    if os.path.exists(filename):
        with open (filename) as f:
            for line in f:
                tweets.append(json.loads(line))
    outlink =1
    inlink = 1
    stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
    nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
    nltk_words.append("rt")
    
    stop_words.extend(nltk_words)
    #old_topic = {}
    d1=d
    if (k==l):
        d1=1
    rts = []
    output = []
    for twt in tweets[:100]:
       # rtweet = json.dumps(tt._json)
       # twt = json.loads(rtweet)
        if (twt['text'].startswith("RT ")):
            outlink = outlink + 1
        inlink = inlink + twt['retweet_count']

        text = twt['text']
        text = re.sub(r'[^\w\s]','',text)
        tokens = word_tokenize(text)
        

        for words in tokens:
            words = words.lower()
            if((words in hub) == False):
                pos = nltk.pos_tag([words])
                if (((words in stop_words)==False) and (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG')):
                    #print(k)
                    hub[words] = 0
            else:
                #print(words)
                output.append(words)
        
        
  

    

    #Ol = Ol*outlink

    if(k%2==1):
        Ol = Ol*outlink
        Il = Il*inlink
        for wrd in output:
            #topic[wrd] = topic[wrd] + (((1-d)**l)/Ol)*(d1/(2*Nt)) 
            hub[wrd] = hub[wrd] + (((1-d)**k)/Il)*(d1/(2*Nt)) 
            #print(hub[wrd])
    else:
        Ol = Ol*inlink
        Il = Il*outlink
        for wrd in output:
            #topic[wrd] = topic[wrd] + (((1-d)**l)/Ol)*(d1/(2*Nt)) 
            hub[wrd] = hub[wrd] + (((1-d)**k)/Il)*(d1/(2*Nt)) 

    if(k==1):
        return hub


    file2 = 'Elon/' + rtid + '_rtweets.txt'
    if os.path.exists(file2):
        with open(file2, 'r') as f:
            for line in f:
                line = line[:-1]
                rts.append(line)
       
    for rid in rts:
        hub = getUpdatedWeights2(hub, d,k+1 ,l, rid, api,Il, Ol, Nt)
        #break
    
    return hub


















def getUpdatedWeights3(topic,  d,k, l, rtid, api,Il, Ol, Nt):
    tweets = []
    filename = 'Leo/'+ rtid + '_tweets.json'
    if os.path.exists(filename):
        with open (filename) as f:
            for line in f:
                tweets.append(json.loads(line))
    outlink =1
    inlink = 1
    stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
    nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
    nltk_words.append('rt')
    
    stop_words.extend(nltk_words)
    #old_topic = {}
    d1=d
    if (k==l):
        d1=1
    rts = []
    output = []
    bgrmtoken = []
    for twt in tweets[:100]:
        #if (twt['text'].startswith("RT ")):
        #    outlink = outlink + 1
        #inlink = inlink + twt['retweet_count']

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
           # if(((words in topic) == False) and  ((words in nltk.corpus.words.words())==True)):
            if(((words in topic) == False)):# and ((dic1.check(words)==True) or  (dic2.check(words)==True))):
                pos = nltk.pos_tag([words])
                if (((words in stop_words)==False) and (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG')):
                    #print(k)
                    topic[words] = 0  # don't add anymore
                    bgrmtoken.append(words)

            elif ((words in topic) == True):
                #print(words)
                if(topic[words]!=0):  #### needs change
                    output.append(words)
                    bgrmtoken.append(words)
        
    ############*********************#############
    bigrm = list(nltk.bigrams(bgrmtoken))

    for item in bigrm:
        newtp = item[0] + item[1]
        newtp = newtp.lower()
        if ((newtp in topic)==False):
            topic[newtp] = 0
        else:
            output.append(newtp)
    ############*********************#############
    
    #Ol = Ol*outlink

    if(k%2==1):
        Ol = Ol*outlink
        Il = Il*inlink
        for wrd in output:
            topic[wrd] = topic[wrd] + (((1-d)**k)/Ol)*(d1/(2*Nt)) 
            #hub[wrd] = hub[wrd] + (((1-d)**l)/Il)*(d1/(2*Nt)) 
        file2 = 'Leo/' + rtid + '_retweets.txt'
        if os.path.exists(file2):
            with open(file2, 'r') as f:
                for line in f:
                    line = line[:-1]
                    rts.append(line)
    else:
        Ol = Ol*inlink
        Il = Il*outlink
        for wrd in output:
            topic[wrd] = topic[wrd] + (((1-d)**k)/Ol)*(d1/(2*Nt)) 
            #hub[wrd] = hub[wrd] + (((1-d)**l)/Il)*(d1/(2*Nt)) 
        file2 = 'Leo' + rtid + '_retweeters.txt'
        if os.path.exists(file2):
            with open(file2, 'r') as f:
                for line in f:
                    line = line[:-1]
                    rts.append(line)

    if(k==1):
        return topic

    for rid in rts:
        topic = getUpdatedWeights(topic, d,k+1, l, rid, api,Il, Ol, Nt)
        #break
    
    return topic















def getUpdatedWeights4(hub,  d,k, l, rtid, api,Il, Ol, Nt):

    tweets = []
    filename = 'Leo/'+ rtid + '_tweets.json'
    if os.path.exists(filename):
        with open (filename) as f:
            for line in f:
                tweets.append(json.loads(line))
    outlink =1
    inlink = 1
    stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
    nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
    nltk_words.append("rt")
    
    stop_words.extend(nltk_words)
    #old_topic = {}
    d1=d
    if (k==l):
        d1=1
    rts = []
    output = []
    outlist = []
    bgrmtoken = []
    for twt in tweets:

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
      
        if (twt['text'].startswith("RT ")):
            if((tokens[1] in outlist) == False):
                outlist.append(tokens[1])
            
        

        for words in tokens:
            words = words.lower()
            if((words in hub) == False):
                pos = nltk.pos_tag([words])
                if (((words in stop_words)==False) and (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG')):
                    hub[words] = 0
                    bgrmtoken.append(words)
            else:
               # if((words in output)==False):
                output.append(words)
                bgrmtoken.append(words)
        
        
    outlink = len(outlist)

    

    ############*********************#############
    bigrm = list(nltk.bigrams(bgrmtoken))

    for item in bigrm:
        newtp = item[0] + item[1]
        newtp = newtp.lower()
        if ((newtp in hub)==False):
            hub[newtp] = 0
        else:
            output.append(newtp)
    ############*********************#############




    #Ol = Ol*outlink

    if(k%2==1):
        
        file2 = 'Leo/' + rtid + '_retweeters.txt'
        if os.path.exists(file2):
            with open(file2, 'r') as f:
                for line in f:
                    line = line[:-1]
                    if((line in rts)==False):
                        rts.append(line)
    
        inlink = inlink + len(rts)
        Il = Il*inlink
        Ol = Ol*outlink
    
        for wrd in output:
            hub[wrd] = hub[wrd] + (((1-d)**k)/Il)*(d1/(2*Nt)) 
        
        print(Ol,Il)
    else:
    #   Ol = Ol*inlink
        Il = Il*outlink
    
        for wrd in output:
            hub[wrd] = hub[wrd] + (((1-d)**k)/Il)*(d1/(2*Nt)) 
    
        file2 = 'Leo/' + rtid + '_rtweets.txt'
        if os.path.exists(file2):
            with open(file2, 'r') as f:
                for line in f:
                    line = line[:-1]
                    if((line in rts)==False):
                        rts.append(line)

    if(k==l):
        return hub

       
    for rid in rts:
       # print(rid)
        hub = getUpdatedWeights4(hub, d,k+1 ,l, rid, api,Il, Ol, Nt)
        #break
    
    return hub