#coding=UTF-8

from string import punctuation
from libs import alchemy
import socket
import util
import threading
import time
import math
import re
from libs.textprocessing.TextProcessing import TextProcessing 
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

# AFINN-111 is as of June 2011 the most recent version of AFINN
filenameAFINN = '/media/110GBPart/SOURCE/twittermining/op-con/src/processing/AFINN111.txt'
afinn = dict(map(lambda (w, s): (w, int(s)), [ 
            ws.strip().split('\t') for ws in open(filenameAFINN) ]))

# Word splitter pattern
pattern_split = re.compile(r"\W+")

ignore_words = ['the', 'this', 'that', 'for', 'and',"'ve","'re","'m","'s"]

def top_words(tweets_list, number=10):
    words = {}    
    words_gen = (word.strip(punctuation).lower() for tweet in tweets_list
                                                 for word in tweet['text'].split()
                                                    if len(word) > 3 and word not in ignore_words)
    
    for word in words_gen:
        words[word] = words.get(word, 0) + 1
    
    top_words = sorted(words.iteritems(),
                       cmp=lambda x, y: cmp(x[1], y[1]) or cmp(y[0], x[0]),
                       reverse=True)[:number]
    
    return top_words

def top_hashtags(tweets_list, number=10):
    words = {}    
    words_gen = (word.strip().lower() for tweet in tweets_list
                                                 for word in tweet['text'].split()
                                                    if word.startswith('#') and
                                                    len(word) > 4)
    
    for word in words_gen:
        words[word] = words.get(word, 0) + 1
    
    top_hashtags = sorted(words.iteritems(),
                       cmp=lambda x, y: cmp(x[1], y[1]) or cmp(y[0], x[0]),
                       reverse=True)[:number]
    
    return top_hashtags

def top_users(tweets_list, number=10):
    words = {}    
    words_gen = (tweet['user'] for tweet in tweets_list)
    
    for word in words_gen:
   
     words[word] = words.get(word, 0) + 1
    
    top_users = sorted(words.iteritems(),
                       cmp=lambda x, y: cmp(x[1], y[1]) or cmp(y[0], x[0]),
                       reverse=True)[:number]
    
    return top_users

def stats_analysis(tweet_analysed_list):
    stats1 = {'neg' : 0, 'pos' : 0, 'neutral' : 0}
    stats2 = {'neg' : 0, 'pos' : 0, 'neutral' : 0}
    stats3 = {'neg' : 0, 'pos' : 0, 'neutral' : 0}
    
    for tupla in tweet_analysed_list: #(tweet, analise1, analise2, analise3)
        stats1[tupla[1]['label']] = stats1.get(tupla[1]['label'], 0) + 1
        stats2[tupla[2]['label']] = stats2.get(tupla[2]['label'], 0) + 1
        stats3[tupla[3]['label']] = stats3.get(tupla[3]['label'], 0) + 1
        
    return (stats1, stats2, stats3)

def analise(tweets_list, query, my_queue, d1, d2, d3):
    for tweet in tweets_list:
        text_without_accents = util.remover_acentos(tweet['text'])
        
        if text_without_accents:        
            analise1 = analyse_affin(text_without_accents) if d3 else {'label' : 'off'}#alchemy.classifyAlchemyAPI(text_without_accents) if d1 else {'label' : 'off'}
            analise2 = analyse_textprocessing(text_without_accents) if d2 else {'label' : 'off'}
            analise3 = analyse_affin(text_without_accents) if d3 else {'label' : 'off'}
            
            my_queue.put((tweet, analise1, analise2, analise3))
        
        else:
            my_queue.put((tweet, {'label' : 'erro'}, {'label' : 'erro'}, {'label' : 'erro'}))

def analysis_sentimental(tweets_list, query, number=2, d1=True, d2=True, d3=True):    
    from Queue import Queue 
    my_queue = Queue()

    divisor = len(tweets_list)/number
    for i in range(number):        
        th = threading.Thread(name='t'+str(i+1), target=analise, args=(tweets_list[divisor*i:divisor*(i+1)], query, my_queue, d1, d2, d3)) 
        th.start()    
    
    while th.isAlive():
        time.sleep(5)
    
    lista = [my_queue.get() for i in range(my_queue.qsize())]
    
    return lista

def analyse_affin(text):
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

def analyse_textprocessing(text):
  if not text:
    return None
   
  obj = TextProcessing("PUBqD=D4=4KKr4WvOfxh#VMkayw$W-iO", "PRI-@KOUBovv#gV-cPGC3wd$%P2fYU3k")
   
  try:
    return obj.sentiment(util.remover_acentos(text))
  except Exception:
    return {'label' : 'erro'}