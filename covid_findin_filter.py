import json
import os
import sys
import time
import twitter

e = {}
with open('API_KEYS.env', 'r') as fle:
    for line in fle:
        key, val = line.strip().split('=')
        if key.split('_')[0] == 'twitter':
            e[key[8:].upper()] = val

t = twitter.Api(
    consumer_key=e["CONSUMER_KEY"],
    consumer_secret=e["CONSUMER_SECRET"],
    access_token_key=e["ACCESS_TOKEN"],
    access_token_secret=e["ACCESS_TOKEN_SECRET"],
    sleep_on_rate_limit=True
)


def tweet_url(t):
    return "https://twitter.com/%s/status/%s" % (t['user']['screen_name'], t['id'])

def find_threads(r2, reverse_replies, thread=[]):
    if not thread:
        thread = [r2]
    for i, r1 in enumerate(reverse_replies):
        if r2['in_reply_to_status_id'] == r1['id'] and r2['user']['id'] == r1['user']['id']:
            thread = find_threads(r1, reverse_replies[i+1:], thread=[r1]+thread)
            break
    return thread

def unroll_thread_up(thread, depth=0):
    if len(thread) > 30:
        # print('thread too long in unroll_thread_up')
        return []

    try:
        t1 = t.GetStatus(thread[0]['in_reply_to_status_id']).AsDict()
    except twitter.error.TwitterError as e:
        # print('got twitter error:', e)
        # print('looking at twitter status:', thread[0]['id'])
        return thread
    thread = [t1] + thread
    if 'in_reply_to_status_id' in t1:
        if t1['in_reply_to_user_id'] == t1['user']['id']:
            thread = unroll_thread_up(thread, depth=depth+1)
    return thread

def look_thru_replies(reverse_replies):
    found = set()
    errors = 0
    for i, tweet in enumerate(reverse_replies):

        if tweet['id'] in found:
            continue

        thread = find_threads(tweet, reverse_replies[i+1:])

        if len(thread) <= 4:
            continue

        try:
            t1 = t.GetStatus(thread[0]['in_reply_to_status_id']).AsDict()
        except twitter.error.TwitterError as e:
            # print('got twitter error:', e)
            # print('looking at twitter status:', thread[0]['id'])
            errors += 1
            continue

        thread = [t1] + thread
        if 'in_reply_to_status_id' in t1:
            if t1['in_reply_to_user_id'] == t1['user']['id']:
                thread = unroll_thread_up(thread)
                if not thread:
                    continue
            else:
                continue

        for ttweet in thread:
            found.add(ttweet['id'])

        try:
            t1 = t.GetStatus(thread[0]['id']).AsDict()
        except twitter.error.TwitterError as e:
            errors += 1
            continue

        likes = t1.get('favorite_count', 0)
        news = '#breaking' in t1['text'].lower()
        print(f'{tweet_url(thread[0])}\t{len(thread)}\t{likes}\t{news}')

    print(f'num tweets: {i}\nnum errors: {errors}')

if __name__ == "__main__":
    collected_replies = []
    src_dir = 'data/covidcollection'
    for filename in os.listdir(src_dir):
        if '2020-04-08' in filename:
            collected_replies.append(src_dir + '/' + filename)

    replies = []
    for filename in sorted(collected_replies):
        with open(filename, 'r') as fle:
            for line in fle:
                tweet = json.loads(line.strip('\n'))
                replies.append(tweet)

    print("num replies:", len(replies))

    look_thru_replies(replies[::-1])
