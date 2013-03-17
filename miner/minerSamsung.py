import tweepy
from datetime import datetime
import json

tweets=[]
f=open("samsungs4miner.json","a")

tweetids=[]
tweetidsfile=None

try:
  tweetidsfile=open(".addedTweets")
  tweetids=json.load(tweetidsfile)
except IOError as e:
  pass

for status in tweepy.Cursor(tweepy.API().search,q='#samsungs4' , rpp=100, lang="en").items(100):
    if(status.id_str not in tweetids):
      d={ 'text'      : status.text.replace('\r', '').replace('\n', ''),
        'tweet_id'  : status.id_str,
        'date'      : status.created_at
        }
      tweets.append(d)
      tweetids.append(status.id_str)

for item in tweets:
    f.write("%s\n"%item)

f.close()