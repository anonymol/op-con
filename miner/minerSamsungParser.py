import datetime
import re
import math

#import json
#python_data = [u'steve@gmail.com']
#json_string = json.dumps(data)

def parseMined(timeDelta, unit):
  f=open("samsungs4miner.json","r")

  now = datetime.datetime.utcnow()
  pos={}
  neg={}
  neu={}
  compiled=re.compile(r'\'date\': datetime.datetime\(([0-9]*), ([0-9]*), ([0-9]*), ([0-9]*), ([0-9]*), ([0-9]*).*\'label\': \'([a-z]*)' , re.IGNORECASE)

  for line in f.readlines():
      match=compiled.findall( line )
      for m in match:
	d = datetime.date( int(m[0]), int(m[1]), int(m[2]) )
	t = datetime.time( int(m[3]), int(m[4]), int(m[5]) )
	tweetTime = datetime.datetime.combine(d, t)
	delta = (now - tweetTime)
	dt=(delta.seconds + delta.days*86400)/timeDelta
	key='<'+str(int(math.ceil(dt)))+' '+unit+ ' ago'
	retdt=None
	if(m[6]=='pos'):
	  retdt=pos
	elif(m[6]=='neg'):
	  retdt=neg
	else:
	  retdt=neu
	if key in retdt.keys():
	  retdt[key]=retdt[key]+1
	else:
	  retdt[key]=1
  f.close()
  return pos,neg,neu

print parseMined(3600,'hours');