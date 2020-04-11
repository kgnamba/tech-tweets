# Tech Tweets
Tech Tweets is an AI driven web application designed to help researches explain their work on Twitter.

## Table of Contents

* [TO DO](#to-do)
* [Requirements] (#requirements)
* [Code Explanation](#code-explanation)
* [Notes](#notes)

## To Do
1. Figure out why a_token and a_token_secret are passed into twitter_interface.html
2. Should there be error if only trying to post one tweet?
3. Remodel twitter_interface to look more like twitter.
4. Have automatic scroll down when adding tweets.
5. Get the upload files/images button in twitter interface to work.
6. Maybe organize code explanation by like, folders or something :/

## Requirements
These can be installed using pip.
* Python 3.5+ (I actually don't know if version matters)
* Threader (Can be installed using pip)
* Flask, flask_cors
* dotenv (This is for .env file)
* TwitterAPI
* requests_oauthlib

## Code Explanation
Jump To:
* [server.py](#serverpy)
* [home.html](#homehtml)
* [home.js](#homejs)
* [twitter_interface.html](#twitter_interfacehtml)
* [twitter.js](#twitterjs)
* [fragments.py](#fragementspy)

### server.py
Backend of the project. 
* Renders home, twitter interface, and demo pages
* Gets user data (profile_img, username, etc.)
* Runs twitter authorization (run_auth())

### home.html
Home page. Landing page when running server.py. Goes to twitter authentication or demo mode.

### home.js
Javascript for home.html. 
* Runs authentication when log-in button is clicked.

### twitter_interface.html
The Tech Tweets app interface. Create and review twitter threads and post them to twitter account.

### twitter.js
Javascript functions for the twitter interface page. 
* Creates tweets, delete tweets, and hold tweets
    * NOTE: deleteTweets works by passing tweet index in array. Deletes tweets WITHOUT removing null el from array
* Functions to post thread to twitter
* Creates textboxes for tweets

## Notes
***BEWARE*** - There is a .gitignore file that has the API_KEYS. Make sure you have access.
***BEWARE*** - The callback URL for authentication is defined via the developer account. Have callback 127.0.0.1:5000
***BEWARE*** - Make sure that in server.py that your load_dotenv(dotenv_path= YOUR .ENV FILE)
Created using Python 3.7.3