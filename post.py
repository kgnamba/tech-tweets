
# importing the module 
import os
from dotenv import load_dotenv
import tweepy 

load_dotenv()

consumer_key =  os.getenv("consumer_key")
consumer_secret = os.getenv("consumer_secret")
access_token = os.getenv("access_token")
access_token_secret = os.getenv("access_token_secret")
url = 'https://www.columbia.edu/'
#url = 'http://127.0.0.1:5000' 

def run_auth(status):
    # authentication of consumer key and secret 
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret) 
  
    # authentication of access token and secret 
    auth.set_access_token(access_token, access_token_secret) 
    api = tweepy.API(auth) 

    try:
        api.verify_credentials()
        print("Authentication OK")
    except:
        print("Error during authentication")
    
    # update the status 
    api.update_status(status) 
    print("Posted status to Twitter!")

    return None
    

if __name__ == "__main__":
    status = 'it is working within python'

    run_auth(status)


