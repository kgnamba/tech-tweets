from flask import render_template
from flask import Flask, Response, request, jsonify, json, redirect, session 
from requests_oauthlib import OAuth1, OAuth1Session
from urllib.parse import urlparse
import os
from dotenv import load_dotenv
import requests
import json
from flask_cors import CORS
import sys
from TwitterAPI import TwitterAPI # This is used with Threader
from threader import Threader # Post threads to twitter

app = Flask(__name__)
CORS(app)
load_dotenv(dotenv_path='..\API_KEYS.env') # dotenv_path should match YOUR .env file

# This information is obtained upon registration of a new client on twitter
key = os.getenv("consumer_key")
secret = os.getenv("consumer_secret")
oauth_token = ''
oauth_token_secret = ''
a_token = ''
a_token_secret=''
user_id=''
screen_name = ''
profile_img = "https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
request_url = "https://api.twitter.com/oauth/request_token"
auth_url = "https://api.twitter.com/oauth/authorize"
access_url = "https://api.twitter.com/oauth/access_token"
update_url = "http://api.twitter.com/1/statuses/update.json"

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/twitter_interface', methods=['GET', 'POST'])
# Setting up twitter_interface page and gets user info
def twitter_interface():
    global a_token
    global a_token_secret
    global screen_name
    global user_id

    token = request.args.get('oauth_token') # Client Information
    verifier = request.args.get("oauth_verifier") # Authorization permission from client


    twitter = OAuth1(key, client_secret=secret, resource_owner_key=token,
            verifier=verifier) # Obtains access token 
    r = requests.post(access_url, auth=twitter) # Oauth access token key and secret and client profile info

    info = r.text
    # print(info)
    try: 
        # Parse through data to get access token in usable form
        info_data = str.split(info, '&')
        a_token = str.split(info_data[0], '=')[1]
        a_token_secret = str.split(info_data[1], '=')[1]
        user_id = str.split(info_data[2], '=')[1]
        screen_name = str.split(info_data[3], '=')[1]

        # print("recieved relevant informaiton")
        # print(user_id)
        # print(screen_name)

        return (render_template('twitter_interface.html', profile_img=profile_img, a_token=a_token, a_token_secret=a_token_secret,user_id=user_id, screen_name=screen_name))
    
    except: # returns home page if user doesn't authorize app
        return render_template('home.html') 


@app.route('/demo', methods=['GET', 'POST'])
def demo():
    screen_name = "Demo_User"
    user_id = None
    a_token = None
    a_token_secret = None
    return (render_template('twitter_interface.html', profile_img=profile_img, a_token=a_token, a_token_secret=a_token_secret,user_id=user_id, screen_name=screen_name))

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    # Gets access request token, which is also the client identifier
    request_token = OAuth1Session(client_key=key, client_secret=secret)

    url = 'https://api.twitter.com/oauth/request_token' # redirection url for client to authorize app

    data = request_token.get(url)
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    oauth_token= ro_key[1]
    oauth_token_secret = ro_secret[1]

    # Create a URL with client permissions
    auth = "{url}?oauth_token={token}".format(url=auth_url, token=oauth_token) # callback URL
    return auth

@app.route("/post", methods=['GET', 'POST'])
def post_tweets():

    json_data = request.get_json()  # Get tweets from twitter.js
    tweets_array = json_data["tweets"]

    thread_keys = dict(consumer_key=key,
            consumer_secret=secret,
            access_token_key=a_token,
            access_token_secret=a_token_secret)

    thread_api = TwitterAPI(**thread_keys)
    
    # tweets_array MUST be a list
    th = Threader(tweets_array, thread_api, wait=1)
    th.send_tweets()

    return {'screen_name': screen_name}

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
