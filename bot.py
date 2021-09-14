import json
from logging import error
from time import sleep
import requests
from requests.api import post
import tweepy
from conf.secrets import *
from conf.mongo_url import *
from functions import *
from pymongo import MongoClient

def __main__(reply) :
    while 1 :
        for mentions in tweepy.Cursor(api.mentions_timeline).items() :
            if reply.find_one({"id_str": mentions.id_str}) == None :
                try :
                    api.get_status(mentions.in_reply_to_status_id).text # On vérifie qu'il y ai un tweet parent
                    valret = reply_to_mention(mentions, api)
                    if valret :
                        reply_id = reply.insert_one(valret)
                except :
                    print("Aucun tweet parent trouvé")
                    reply_id = reply.insert_one({
                        "id_str" : mentions.id_str,
                        "mentionner": mentions.user.screen_name,
                        "parents": False 
                    })
                print(reply_id)
        sleep(60)

auth = tweepy.OAuthHandler(API_KEY, API_SECRET_KEY)
auth.set_access_token(ACCESS_TOKEN, ACCESS_TOKEN_SECRET)
auth.secure = True
api = tweepy.API(auth)

try :
    api.verify_credentials()
    print("Authentification Ok")
    try :
        client = MongoClient(MONGO_URL)
        db = client.politweet
        reply = db.reply
        print("connected")
        __main__(reply)
    except Exception as err:
        print(err)    
except :
    print("Error during authentification")