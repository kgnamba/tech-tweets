import json
import pickle
import requests
import sys

from flask import Flask, Response, render_template, request
from flask_cors import CORS
from requests_oauthlib import OAuth1, OAuth1Session

from serpapi.google_search_results import GoogleSearchResults

import tweepy

import spacy

from bert_util import sent_emb_from_text
from scipy.spatial.distance import cosine
import numpy as np


nlp = spacy.load("en_core_web_sm")


app = Flask(__name__)
CORS(app)


# pickled files should be list: [list articles, list headline embeddings]
pkl_fles = ['data/abc-headlines.pickle', 'data/newsapi-articles.pickle']
pkl_fles = [
    'data/newsapi-articles_2020-02-05_2020-02-10.pickle', 
    'data/newsapi-articles_2020-02-10_2020-02-15.pickle',
    'data/newsapi-articles_2020-02-15_2020-02-20.pickle',
    'data/newsapi-articles_2020-02-20_2020-02-21.pickle',
    'data/newsapi-articles_2020-02-21_2020-02-22.pickle',
    'data/newsapi-articles_2020-02-22_2020-02-23.pickle',
    'data/newsapi-articles_2020-02-23_2020-02-24.pickle',
    'data/newsapi-articles_2020-02-24_2020-02-25.pickle',
    'data/newsapi-articles_2020-02-25_2020-02-26.pickle'
    ]
articles = []
headlines_emb = []
for fle in pkl_fles:
    print('loading news articles from', fle)
    these_articles, these_emb = pickle.load(open(fle, 'rb'))
    articles += these_articles
    headlines_emb += these_emb
print('len(articles)', len(articles))
print('len(headlines_emb):', len(headlines_emb))

twitter_keys = {'oauth_token': '', 'oauth_token_secret': ''}
api_keys = {}
with open('API_KEYS.env', 'r') as fle:
    for line in fle:
        key = line.strip().split('=')[0]
        val = line.strip().split('=')[1]
        if key.split('_')[0] == 'twitter':
            twitter_keys[key[8:]] = val
        else:
            api_keys[key] = val
print('twitter keys', twitter_keys)
print('api_keys', api_keys)

tweepyauth = tweepy.OAuthHandler(twitter_keys['consumer_key'], twitter_keys['consumer_secret'])

tweet_emb_pth = 'data/tweet_emb.pickle'

@app.route('/')
def hello_world():
    
    statuses = []
    loggedin = False
    refresh = False
    if 'request_token' in twitter_keys:
        del twitter_keys['request_token']
        verifier = request.args.get('oauth_verifier')
        tweepyauth.get_access_token(verifier)
        twitter_keys['token'] = (tweepyauth.access_token, tweepyauth.access_token_secret)
        print(twitter_keys)
        api = tweepy.API(tweepyauth)

        loggedin = True

    elif 'token' in twitter_keys:
        tweepyauth.set_access_token(twitter_keys['token'][0], twitter_keys['token'][1])
        api = tweepy.API(tweepyauth)
        loggedin = True

    if loggedin and refresh:
        stat_emb = []
        stat_obj = []
        print('querying user home_timeline')
        cursor = tweepy.Cursor(api.home_timeline, tweet_mode='extended').items()
        count = 0
        
        while count < 250:
            count += 1
            try:
                status = cursor.next()
                stat_obj.append(status)
                stat_emb.append(sent_emb_from_text(status.full_text))
            except tweepy.error.TweepError:
                print('ERROR: failed to request tweets, rate limit hit')
                break

        print(f'pickling {len(stat_obj)} tweets')
        with open(tweet_emb_pth, 'wb') as pkl:
            pickle.dump([stat_obj, stat_emb], pkl)
        statuses = stat_obj[:5]

        remaining = int(api.last_response.headers['x-rate-limit-remaining'])
        print('remaining requests:', remaining)

    print(f'sending {len(statuses)} statuses')

    return render_template('news_collector.html', statuses=statuses)


def get_status_url(status):
    statid = status['id_str']
    username = status['user']['screen_name']
    return f'https://twitter.com/{username}/status/{statid}'

@app.route('/api/get_tweets', methods=['POST'])
def get_tweets():
    text = request.values.get('text')

    api = tweepy.API(tweepyauth)
    query = text.replace(' ', '+') + "+min_retweets:100+lang:en"
    res = api.search(q=query)

    remaining = int(api.last_response.headers['x-rate-limit-remaining'])
    print('remaining requests:', remaining)

    statuses = []
    for stat in res:
        url = get_status_url(stat._json)
        oembed = 'https://publish.twitter.com/oembed'
        r = requests.get(oembed, params={'url': url})
        html = r.json().get('html')
        statuses.append({**stat._json, **{'html': html}})

    data = {'statuses': statuses}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/api/get_news', methods=['POST'])
def get_news():
    
    text = request.values.get('text')
    in_emb = sent_emb_from_text(text, pprint=True)
    sims = []
    for head in headlines_emb:
        sim1 = 1 - cosine(in_emb, head)
        sims.append(sim1)
    indx = np.argsort(sims)[::-1]

    num_res = 10
    count = 0
    collect = 0
    headlines = []
    art_indx = []
    # TODO: THERE ARE REPEATS IN THE STORED ARTICLES, 
    # THIS IS A SHIT WAY OF DEALING WITH IT. FIX IN news_util.py
    while collect < num_res:
        i = indx[count]
        count += 1
        if articles[i]['title'] not in headlines:
            headlines.append(articles[i]['title'])
            art_indx.append(i)
            collect += 1

    top_articles = []
    for i in art_indx:
        extra_data = {'sim': sims[i]}
        top_a = {**articles[i], **extra_data}
        top_articles.append(top_a)

    data = {'headlines': headlines, 'articles': top_articles}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/api/get_goog_news', methods=['POST'])
def get_goog_news():
    print('running get_goog_news')
    text = request.values.get('text')
    tbs = request.values.get('tbs')
    params = {
        "q": text,
        "hl": "en",
        "gl": "us",
        "tbm": "nws",
        "tbs": tbs,
        "num": 10,
        "api_key": api_keys['serpapi_key']
    }

    print(params)

    client = GoogleSearchResults(params)
    data = client.get_dict()
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/api/get_noun_phrases', methods=['POST'])
def get_noun_phrases():
    text = request.values.get('text')
    doc = nlp(text)
    phrases = []
    questions = []
    for chunk in doc.noun_chunks:
        if len(chunk) == 1 and chunk[0].is_stop:
            continue
        phrases.append(chunk.text)
        questions.append(f'Do you think the reader will know what "{chunk.text}" is?')
    data = {'nounphrases': phrases, 'questions': questions}
    resp = Response(json.dumps(data), status=200, mimetype='application/json')
    return resp

@app.route('/auth', methods=['GET', 'POST'])
def auth():

    try:
        redirect_url = tweepyauth.get_authorization_url()
        twitter_keys['request_token'] = tweepyauth.request_token
        print('request_token', tweepyauth.request_token)
        print('redirect_url', redirect_url)
        return redirect_url
    except tweepy.TweepError:
        print('Error! Failed to get request token.')


if __name__ == "__main__":
    app.run(debug=True, port=8888)
