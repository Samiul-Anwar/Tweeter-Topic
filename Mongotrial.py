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
from utility import *
import operator
import enchant
l=2
d=0.8


client = MongoClient()
db = client['gates_tweets']
collection_tweets = db['gates_tweets']
#record2 = loads('osmar_tweets_no_rt.json')
data = []
with open ('Gates/gates_tweets.json') as f:
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

stop_words = list(get_stop_words('en'))         #Have around 900 stopwords
nltk_words = list(stopwords.words('english'))   #Have around 150 stopwords
nltk_words.append('rt')
nltk_words = nltk_words + rmvlist
stop_words.extend(nltk_words)
bgrmtoken = []

for tx in result[:100]:
    text = tx['text']
   
    #print (pos)
    text = re.sub(r'[^\w\s]','',text)
    tokens = word_tokenize(text)
    #stm = nltk.stem.SnowballStemmer('english')
    #stm = nltk.wordnet.WordNetLemmatizer()
    #tokens = stm.stem(tkn)
    #print(tokens)
    #pos = nltk.pos_tag(tokens)
    #d = dict(itertools.zip_longest(*[iter(pos)] * 2, fillvalue=""))

    #print (pos)
    #break
    #output = []

    ##******************#############
    if 'entities' in tx:
        htag = tx['entities']['hashtags']
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
            #print(pos)
            if (((words in stop_words)==False) and (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG')):
                topic[words] = d
                bgrmtoken.append(words)
                #print(pos)
        #else:
            #print(words)



############*********************#############
bigrm = list(nltk.bigrams(bgrmtoken))

for item in bigrm:
    newtp = item[0] + item[1]
    newtp = newtp.lower()
    if ((newtp in topic)==False):
        #print (newtp)
        topic[newtp] = d
############*********************#############


    
#print(topic)
for key in topic:
    topic[key] = topic[key]/ len(topic.keys())



api = twitter.Api(
        consumer_key=CONSUMER_KEY, consumer_secret=CONSUMER_SECRET, access_token_key= ACCESS_TOKEN_KEY, access_token_secret=ACCESS_TOKEN_SECRET
    )



rts = []
with open('Gates/gates_rtweeters.txt', 'r') as f:
    for line in f:
        line = line[:-1]
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
for rtid in rts:
    topic= getUpdatedWeights(topic, d,1, l, rtid, api, 1, Nt)
    #break

#print(topic)

#tp = sorted(topic.items(), key = lambda kv:(kv[1], kv[0]))  
cnt =0
tp= {}
for key in topic:
    #print(key)
    #print(tp[key])
    if (topic[key]>=1/Nt):
        tp[key] = topic[key]*100000
    cnt = cnt + 1
    #if(cnt>20):
        #break
#print(sorted(tp.items(), key = lambda kv:(kv[1], kv[0])) )
sorted_x = sorted(tp.items(), key=operator.itemgetter(1))
#for lst in sorted_x:
#    pos = nltk.pos_tag([lst[0]])
#    if (pos[0][1]=='NN' or pos[0][1]=='NNS' or pos[0][1]=='NNP' or pos[0][1]=='NNPS' or pos[0][1]=='VBG'):
        #print(lst, pos[0][1])

print(sorted_x)
client.close()