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
from utility2 import *
import operator
import enchant
l=2
d=.8

#dic1 = enchant.Dict('en_US')
#dic2 = enchant.Dict('en_UK')

client = MongoClient()
db = client['leo_tweets']
collection_tweets = db['leo_tweets']
#record2 = loads('osmar_tweets_no_rt.json')
data = []
with open ('Leo/leo_tweets.json') as f:
    for line in f:
        data.append(json.loads(line))

db.collection_tweets.insert_many(data)
#print(db.collection_tweets.index_information())


result = db.collection_tweets.find({},{"_id": 0, 'text': 1, 'entities': 1 })
tId = db.collection_tweets.find({},{"_id": 0, 'id_str': 1 })

#while(1):
   # try:
       # record = result.next()
      #  print(record['text'])
   # except StopIteration:
       # print("Empty cursor!")
    #break
topic = {}
hub = {}
stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
nltk_words.append('rt')
stop_words.extend(nltk_words)
bgrmtoken = []
for tx in result[:100]:
    text = tx['text']
    
    htag = []

    ##******************#############
    if 'entities' in tx:
        htag = tx['entities']['hashtags']

    ##******************#############
    text = re.sub(r'[^\w\s]','',text)
    tokens = word_tokenize(text)

    

    

    ##******************#############
    for ht in htag:
        htv = re.sub(r'[^\w\s]','',ht['text'])
        if((htv in tokens)==False):    
            tokens.append(htv)
    ##******************#############

    #output = []
    for words in tokens:
        words = words.lower()
        #if(((words in topic) == False) and ((words in nltk.corpus.words.words())==True)):
        if(((words in topic) == False)):# and ((dic1.check(words)==True) or  (dic2.check(words)==True))):
            pos = nltk.pos_tag([words])
            #print(pos)
            if (((words in stop_words)==False) and (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG')):
                topic[words] = d
                hub[words] = d
                bgrmtoken.append(words)
       # else:
            #print(words)


############*********************#############
bigrm = list(nltk.bigrams(bgrmtoken))

for item in bigrm:
    newtp = item[0] + item[1]
    newtp = newtp.lower()
    if ((newtp in topic)==False):
        topic[newtp] = d
    if ((newtp in hub)==False):
        hub[newtp] = d
############*********************#############
    
#print(topic)
for key in topic:
    topic[key] = topic[key]/(2* len(topic.keys()))
    hub[key] = hub[key]/(2* len(topic.keys()))



api = twitter.Api(
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key= ACCESS_TOKEN_KEY, access_token_secret=ACCESS_TOKEN_SECRET
    )

#print(hub)

rts = []
with open('Leo/leo_rtweeters.txt', 'r') as f:
    for line in f:
        line = line[:-1]
        if((line in rts)==False):
            rts.append(line)
        


#print (rts[0])
#retweets = json.dumps(rts._json)
#loaded_json = json.loads(retweets)
#for rtid in rts:
#    retweets = json.dumps(rtid._json)
#    rteets = json.loads(retweets)
#    print(rteets['user']['screen_name'])
#    screen_name = rteets['user']['screen_name']
#    break
Nt = len(topic.keys())

######################
for rtid in rts:
    topic = getUpdatedWeights3(topic, d,1, l, rtid, api,1, 1, Nt)
  
#####################
rts = []
with open('Leo/leo_rtweets.txt', 'r') as f:
    for line in f:
        line = line[:-1]
        if((line in rts)==False):
            rts.append(line)
for rtid in rts:
    hub = getUpdatedWeights4(hub, d,1, l, rtid, api,1, 1, Nt)

#print(Nt)

#tp = sorted(topic.items(), key = lambda kv:(kv[1], kv[0]))  
cnt =0
tp= {}
for key in topic:
    #print(key)
    #print(tp[key])
    if (topic[key]>=1/(2*Nt)):
        tp[key] = topic[key]*100000
    #else:
        #print((1/(2*Nt))-topic[key])
    cnt = cnt + 1

cnt =0
hb= {}
for key in hub:
    #print(key)
    #print(tp[key])
    if (hub[key]>=1/(2*Nt)):
        hb[key] = hub[key]*100000
   # else:
    #    print((1/(2*Nt))-hub[key])
    cnt = cnt + 1
    #if(cnt>20):
        #break
#print(sorted(tp.items(), key = lambda kv:(kv[1], kv[0])) )
sorted_x = sorted(tp.items(), key=operator.itemgetter(1))
print("Authoritative:")
print(sorted_x)

#print(hub)
sorted_x = sorted(hb.items(), key=operator.itemgetter(1))
print("HUB:")
print(sorted_x)


client.close()