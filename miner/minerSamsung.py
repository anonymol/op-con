import tweepy
from datetime import datetime
import json
import re
import math

def analyse_affin(text):
  # AFINN-111 is as of June 2011 the most recent version of AFINN
  filenameAFINN = 'AFINN111.txt'
  afinn = dict(map(lambda (w, s): (w, int(s)), [ ws.strip().split('\t') for ws in open(filenameAFINN) ]))

  # Word splitter pattern
  pattern_split = re.compile(r"\W+")

  words = pattern_split.split(text.lower())
  sentiments = map(lambda word: afinn.get(word, 0), words)
  if sentiments:
    # How should you weight the individual word sentiments? 
    # You could do N, sqrt(N) or 1 for example. Here I use sqrt(N)
    sentiment = float(sum(sentiments))/math.sqrt(len(sentiments))
  else:
    sentiment = 0
  if(sentiment>0):
    return {'label' : 'pos'}
  elif(sentiment==0):
    return {'label' : 'neutral'}
  return {'label' : 'neg'}

tweets=[]
f=open("samsungs4miner.json","a")

tweetids=[]
tweetidsfile=None

try:
  tweetidsfile=open(".addedTweets")
  tweetids=json.load(tweetidsfile)
except IOError as e:
  pass

for status in tweepy.Cursor(tweepy.API().search,q='#samsungs4' , rpp=100, lang="en").items(1000):
    if(status.id_str not in tweetids):
      d={ 'text'      : status.text.replace('\r', '').replace('\n', ''),
        'tweet_id'  : status.id_str,
        'date'      : status.created_at,
        }
      tweets.append(d)
      tweetids.append(status.id_str)

for item in tweets:
  text_without_accents = item['text']#util.remover_acentos(item['text'])
  if text_without_accents:        
    analyse = analyse_affin(text_without_accents)
  f.write("%s%s\n"%(item,analyse))

f.close()