import datetime
import json
import os
import subprocess
import time

def get_replies(tweetsfile):
    '''
    Return list of json tweet objects from filename that are replies.

    tweetsfile should be file with one json tweet object per line.
    '''
    replies = []
    with open(tweetsfile, 'r') as fle:
        for line in fle:
            tweet = json.loads(line.strip('\n'))
            if tweet['in_reply_to_status_id'] is not None:
                if tweet['in_reply_to_user_id'] == tweet['user']['id']:
                    replies.append(tweet)
    return replies

src_dir = '/Users/katy/Documents/Grad/tech-tweets/data/covidcollection'
now = datetime.datetime.now()
timestr = now.strftime("%Y-%m-%d_%H%M")
filename = f'{src_dir}/cc_{timestr}.jsonl'
filename_replies = f'{src_dir}/cc_{timestr}_replies.jsonl'

# cmd = f'twarc filter coronavirus,covid19 --lang en > cc_{timestr}.jsonl'
cmd = ['/usr/local/bin/twarc', 'filter', 'coronavirus,covid19', '--lang', 'en']

output = open(filename, 'w')

try:
    subprocess.call(cmd, stdout=output, timeout=60*60)
except subprocess.TimeoutExpired as e:
    pass

output.close()

replies = get_replies(filename)


with open(filename_replies, 'w') as fle:
    for r in replies:
        fle.write(json.dumps(r) + '\n')

os.remove(filename)
