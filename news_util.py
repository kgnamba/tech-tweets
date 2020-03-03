import json
import pickle

from newsapi import NewsApiClient

from bert_util import sent_emb_from_text


def get_newsapi_articles(pkl_fle_nme, from_date, to_date):

    print('getting news articles from NEWSAPI...')
    # Get all news articles for the session:
    with open('NEWSAPI_KEY.env', 'r') as f:
        key = f.read()

    calls = 0
    api = NewsApiClient(api_key=key)
    source_str = "abc-news,associated-press,the-verge,the-wall-street-journal,\
        the-washington-post,wired,politico,newsweek,fox-news,cbs-news,cnn,\
        mashable,national-geographic,the-hill,next-big-future,reuters,\
        vice-news"

    articles = []
    for src in source_str.split(','):
        calls += 1
        res = api.get_everything(
            language="en",
            sort_by="popularity",
            page_size=100,
            sources=src)

        curr_articles = {}
        for item in res['articles']:
            if item['title'] is not None:
                curr_articles[item['title']] = item

        for keyword in ['politics', 'national', 'world', 'business', 'tech', 'science']:
            calls += 1
            res = api.get_everything(
                language="en",
                sort_by="popularity",
                page_size=100,
                from_param=from_date,
                to=to_date,
                sources=src,
                q=keyword)
            for item in res['articles']:
                if item['title'] is not None and item['title'] not in curr_articles:
                    curr_articles[item['title']] = item

        list_articles = [curr_articles[key] for key in curr_articles]
        print(src, len(list_articles))
        articles += list_articles

    print('api calls', calls)
    print('len(articles)', len(articles))

    print('embedding headlines...')
    headlines_emb = []
    for article in articles:
        e1 = sent_emb_from_text(article['title'])
        headlines_emb.append(e1)
    print('len(articles)', len(articles))
    print('len(headlines_emb):', len(headlines_emb))

    print('saving data as', pkl_fle_nme)
    with open(pkl_fle_nme, 'wb') as pkl:
        pickle.dump([articles, headlines_emb], pkl)


def get_abc_headlines(pkl_fle_nme):
    print('getting news headlines...', end='', flush=True)
    articles = []
    src = {'id': 'abc', 'name': 'ABC News'}
    with open('data/abcnews-date-text.csv', 'r') as fle:
        fle.readline()  # skip header
        for line in fle:
            date, headline = line.strip("\n").split(',')
            year = int(date[:4])
            if year > 2018:
                articles.append({'publishedAt': date, 'title': headline, 'source': src})
    print(len(articles), 'articles')

    print('embedding news articles...', end='', flush=True)
    headlines_emb = []
    firstsent_emb = []
    count = 0
    for article in articles:
        count += 1
        if count % 1000 == 0:
            print('.', end='', flush=True)
        e1 = sent_emb_from_text(article['title'])
        headlines_emb.append(e1)
        firstsent_emb.append(None)
    print('len(headlines_emb):', len(headlines_emb))
    print('len(firstsent_emb):', len(firstsent_emb))


    print('saving data as', pkl_fle_nme)
    with open(pkl_fle_nme, 'wb') as pkl:
        pickle.dump([articles, headlines_emb], pkl)


date1 = '2020-02-26'
date2 = '2020-02-27'
fle_nme = f'data/newsapi-articles_{date1}_{date2}.pickle'
get_newsapi_articles(fle_nme, date1, date2)