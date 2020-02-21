from data import profile_img, status, tweets
from flask import Flask
from flask import render_template
from flask import Flask, Response, request, jsonify, json, redirect, session 
from requests_oauthlib import OAuth1, OAuth1Session
from urllib.parse import urlparse
import requests
import post
import twitter
import os
from dotenv import load_dotenv
import requests
import tweepy
import json
from flask_cors import CORS
import sys
from TwitterAPI import TwitterAPI
from threader import Threader

app = Flask(__name__)
CORS(app)

# This information is obtained upon registration of a new client on twitter
key = os.getenv("consumer_key")
secret = os.getenv("consumer_secret")
oauth_token = ''
oauth_token_secret = ''
a_token = ''
a_token_secret=''
user_id=''
screen_name = ''
request_url = "https://api.twitter.com/oauth/request_token"
auth_url = "http://api.twitter.com/oauth/authorize"
access_url = "https://api.twitter.com/oauth/access_token"
update_url = "http://api.twitter.com/1/statuses/update.json"
callback_url = 'http://127.0.0.1:5000/callback'

@app.route('/')
def home(name=None):
    #print(key)
    return render_template('home.html')

@app.route('/twitter_interface', methods=['GET', 'POST'])
# Setting up twitter_interface, gets user info
def twitter_interface(name=None):
    global a_token
    global a_token_secret
    global screen_name
    global user_id

    token = request.args.get('oauth_token')
    verifier = request.args.get("oauth_verifier")

    # In this step we also use the verifier
    twitter = OAuth1(key, client_secret=secret, resource_owner_key=token,
            verifier=verifier)
    r = requests.post(access_url, auth=twitter)

    # This is the end of Step 3, we can now extract resource owner key & secret
    # as well as some extra information such as screen name.

    info = r.text
    print(info)
    try:
        info_data = str.split(info, '&')
        a_token = str.split(info_data[0], '=')[1]
        a_token_secret = str.split(info_data[1], '=')[1]
        user_id = str.split(info_data[2], '=')[1]
        screen_name = str.split(info_data[3], '=')[1]

        print("recieved relevant informaiton")
        print(user_id)
        print(screen_name)

        return (render_template('twitter_interface.html', profile_img=profile_img, a_token=a_token,
         a_token_secret=a_token_secret,user_id=user_id, screen_name=screen_name))
    
    except:
        return render_template('home.html')
    
    

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    # This uses consumer_key and secret to get request from API
    request_token = OAuth1Session(client_key=key, client_secret=secret)
    url = 'https://api.twitter.com/oauth/request_token'
    data = request_token.get(url)
    data_token = str.split(data.text, '&')
    ro_key = str.split(data_token[0], '=')
    ro_secret = str.split(data_token[1], '=')
    oauth_token= ro_key[1]
    oauth_token_secret = ro_secret[1]
    #print(oauth_token_secret)
    # Create the redirection url and send the user to twitter to give app permissions
    auth = "{url}?oauth_token={token}".format(url=auth_url, token=oauth_token)
    return auth

@app.route("/callback", methods=["GET", "POST"])
def callback():
    global a_token
    global a_token_secret
    global screen_name
    global user_id

    token = request.args.get('oauth_token')
    verifier = request.args.get("oauth_verifier")

    # In this step we also use the verifier
    twitter = OAuth1(key, client_secret=secret, resource_owner_key=token,
            verifier=verifier)
    r = requests.post(access_url, auth=twitter)

    # This is the end of Step 3, we can now extract resource owner key & secret
    # as well as some extra information such as screen name.

    info = r.text

    info_data = str.split(info, '&')
    a_token = str.split(info_data[0], '=')[1]
    a_token_secret = str.split(info_data[1], '=')[1]
    user_id = str.split(info_data[2], '=')[1]
    screen_name = str.split(info_data[3], '=')[1]

    # Show a very basic status update form
    print("a_token: ", a_token)
    print("screenid: ", screen_name)
    
    return ""

@app.route("/save_tweet", methods=["GET", "POST"])
def save_tweet():
    global tweets

    json_data = request.get_json()
    new_tweet = json_data["message"]

    tweets.append(new_tweet)

    print(tweets)
    
    return {'tweets': tweets}

@app.route("/post", methods=["POST"])
def post_func():

    global tweets
    
    thread_keys = dict(consumer_key=key,
            consumer_secret=secret,
            access_token_key=a_token,
            access_token_secret=a_token_secret)
    
    thread_api = TwitterAPI(**thread_keys)

    print(tweets)
    th = Threader(tweets, thread_api, wait=1)
    th.send_tweets()
    tweets = []

    # print("Got message to post")
    # json_data = request.get_json()
    # status = json_data["message"]

    # # authentication of consumer key and secret 
    # auth = tweepy.OAuthHandler(key, secret) 

    # # authentication of access token and secret 
    # auth.set_access_token(a_token, a_token_secret) 
    # api = tweepy.API(auth) 

    # try:
    #     api.verify_credentials()
    #     print("Authentication OK")
    # except:
    #     print("Error during authentication")
    
    # # update the status 
    # api.update_status(status) 
    # print("Posted status to Twitter!")

    return {'screen_name': screen_name}

if __name__ == "__main__":
    app.secret_key = os.urandom(24)
    app.run(debug=True)
