import tweepy
from datetime import datetime
tweets=[]
for status in tweepy.Cursor(tweepy.API().search,q='Conclave13' , rpp=100, lang="en").items(100):
    d={ 'user' : status.from_user,
        'user_id'   : status.from_user_id_str,
        'image'     : status.profile_image_url_https,
        'text'      : status.text.replace('\r', '').replace('\n', ''),
        'tweet_id'  : status.id_str,
        'geo'       : status.geo,
        'date'      : status.created_at
        }
    tweets.append(d)
f=open("Conclave13.json","a")
f.write("%s"%datetime.now())
f.write("\n")
for item in tweets:
    f.write("%s\n"%item)
f.write("\n")
f.close()
