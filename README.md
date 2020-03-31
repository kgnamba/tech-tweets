# Tech Tweets
Tech Tweets is an AI driven web application designed to help researches explain their work on Twitter.

## Table of Contents

* [TO DO](#to-to)
* [Code Explanation](#code-explanation)
* [Notes](#notes)

## To Do
1. Figure out why a_token and a_token_secret are passed into twitter_interface.html
2. DISABLE POST BUTTON IN DEMO MODE!!!
3. Delete Tweets functionality.
4. Remodel twitter_interface to look more like twitter.
5. Maybe organize code explanation by like, folders or something :/

## Code Explanation
Jump To:
* [server.py](#server.py)
* [home.html](#home.html)
* [home.js](#home.js)
* [twitter_interface.html](#twitter_interface.html)
* [twitter.js](#twitter.js)
* [fragments.py](#fragements.py)

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
* Creates tweets and hold tweets
* Functions to post thread to twitter
* Creates textboxes for tweets

## Notes
***BEWARE*** - There is a .gitignore file that has important information inside. Make sure you have access.