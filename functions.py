import requests
from conf.secrets import *

def reply_to_mention(mention, api) :
    
    mentionner = mention.user.screen_name
    id = mention.id
    text = api.get_status(mention.in_reply_to_status_id).text
    response = requests.get("{}predict/{}".format(URL, text))
    tendance = response.json()
    reply = make_reply(tendance, mentionner)
    valret = {
        "id_str" : mention.id_str,
        "text": text,
        "text_mentionner": mention.text,
        "reply" : reply,
        "mentionner": mention.user.screen_name,
        "gauche": tendance["gauche"],
        "droite": tendance["droite"]
    }
    try :
        api.update_status(
            status= text,
            in_reply_to_status_id = id
        )
        return valret
    except Exception as err:
        print(err)
        return False

def make_reply(tendance, mentionner) :
    if tendance["gauche"] > tendance["droite"] :
        first = "{}% de gauche".format(round(tendance["gauche"] * 100))
        second = "{}% de droite".format(round(tendance["droite"] * 100))
    else :
        first = "{}% de droite".format(round(tendance["droite"] * 100))
        second = "{}% de gauche".format(round(tendance["gauche"] * 100))

    return "@{} C'est de {}\n\n{}\n{}".format(mentionner, tendance["position"], first, second)