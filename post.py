
# importing the module 
import tweepy 

consumer_key = 'G3WTD5N5Hvb75c3b810q04U08'
consumer_secret = 'IMaBHKM3EDtqsfqKBtUdgpX1lUknm9biKR6rd4524E9tS2pSHP'
access_token = '777720434691305472-OzsQtSMVsxu3DaEBmCj3VbIIGoxDaNB'
access_token_secret = 'jB16isLczcdsOgZrkqDSWqbVIj2ERUez4DkhQeXHIGiM7'
url = 'https://www.columbia.edu/'

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


