README.txt
This file explains what is happening in the code. 

post.py
Authorizes the app to post on behalf of the user. Sending the "authorization signature" 
so that the app can make requests to the TwitterAPI. 
    NOTE:
        Make sure that you have the .env file! This is included in the .gitignore file
        so that the API credentials aren't comprimises! 

server.py
-It's doing a lot of things.
Backend of the app. 
Functions:
    home - renders homepage and sets up app authorization to use API. On #login button click, sends user to post.py,
        which sends user to Twitter authorization page. 
    twitter_interface - Makes request to API for user data such as username and profile picture.
    Sets up twitter interface.
    auth - User gives app permission to post on their Twitter account
    callback - self-explanatory
    save_tweet - POST request to add tweet to thread. Saves tweet into thread.
    post - posts thread to twitter account

twitter.py
Bunch of twitter authentication functions that seem to be unconnected to server.py

twitter.js
Javascript functions for twitter_interface, posting twitter methods