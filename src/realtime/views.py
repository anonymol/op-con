#coding=UTF-8

import util
from realtime import control
import processing

def home(request):
    if request.method == 'GET':
        return util.request.render('index.html', {}, request)

def realtime(request):
    if request.method == 'GET':
        query = request.GET.get('q', None)
        
        if query:
            tweets = control.get_realtime_tweets(query + " -filter:links -RT -@", 100, True)            
            tweets_analysed = processing.control.analysis_sentimental(tweets, query, number=10, d1=True, d2=True, d3=True)
            
            stats = processing.control.stats_analysis(tweets_analysed)
            
            top_words = processing.control.top_words(tweets)
            top_hashtags = processing.control.top_hashtags(tweets)
            top_users = processing.control.top_users(tweets)
            
            tweets_analysed = sorted(tweets_analysed, key=lambda tupla:tupla[2]==tupla[3], reverse=True)
            
            d = {
                 'query'        : query,
                 'size'         : len(tweets),
                 'tweets'       : tweets_analysed,
                 'stats'        : stats,
                 'top_words'    : top_words,
                 'top_hashtags' : top_hashtags,
                 'top_users'    : top_users
                 }
            
            return util.request.render('realtime.html', d, request)
        
        else:
            return util.request.print_html('No query sent!')
