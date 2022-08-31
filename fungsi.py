import json.encoder

import tweepy
import login
import time
import _json
from requests_oauthlib import OAuth1
import requests
import os



class Twitter:
    def __init__(self):
        print("initializing")
        self.inits = tweepy.OAuthHandler(login.CONSUMER_KEY, login.CONSUMER_PASS)
        self.inits.set_access_token(login.ACCESS_KEY, login.ACCESS_PASS)
        self.api = tweepy.API(self.inits)

    def read_dm(self):
        print("Retrieving DM's")
        dms = list()
        try:
            api = self.api
            dm = api.get_direct_messages()
            for x in range(len(dm)):
                sender_id = dm[x].message_create['sender_id']
                message = dm[x].message_create['message_data']['text']
                message_data = str(dm[x].message_create['message_data'])
                json_data = json.encoder.encode_basestring(message_data) ##convert jadi json
                print("Retrieving Message -> "+str(message)+" by sender id "+str(sender_id))

                if "attachment" not in json_data:
                    print("Menfess does not have any media")
                    d = dict(message = message, sender_id = sender_id, id = dm[x].id, media = None, shorted_media_url = None)
                    dms.append(d)
                    dms.reverse()

                else:
                    print("Menfess has an attachment")
                    attachment = dm[x].message_create['message_data']['attachment']
                    d = dict(message = message, sender_id = sender_id, id = dm[x].id, media = attachment['media']['media_url'], shorted_media_url = attachment['media']['url'])
                    dms.append(d)
                    dms.reverse()

            print(str(len(dms)) + " acquired")
            time.sleep(40)            ###sleep karena twitter ada limit jadi disleep biar ga kena
            return dms

        except Exception as ex:
            print(ex)
            time.sleep(60)
            pass

    def delete_dm(self, id):    ##menghapus dm
        print("Deleting DM with id = "+ str(id))
        try:
            self.api.delete_direct_message(id)
            time.sleep(40)

        except Exception as ex:
            print(ex)
            time.sleep(40)
            pass

    def post_tweet(self, tweet):    ##posting tweet menfess
        api = self.api
        dm = api.get_direct_messages()
        for u in range(len(dm)):
            sender_id = dm[u].message_create['sender_id']
        self.api.update_status(tweet)
        self.senddm(sender_id)



    def post_media(self, tweet, media_url, shorted_media_url):
        api = self.api
        dm = api.get_direct_messages()
        for m in range(len(dm)):
            sender_id = dm[m].message_create['sender_id']
        print("Dwnloading media")
        arr = str(media_url).split('/')
        auth = OAuth1(client_key= login.CONSUMER_KEY, client_secret= login.CONSUMER_PASS, resource_owner_secret =login.ACCESS_PASS, resource_owner_key= login.ACCESS_KEY)
        r = requests.get(media_url, auth = auth)
        with open(arr[9], 'wb') as f:
            f.write(r.content)
        print ("Downloaded")
        tweet = tweet.replace(shorted_media_url, "")
        self.api.update_status_with_media(filename= arr[9], status = tweet)
        self.senddm(sender_id)
        os.remove(arr[9])
        print("Post menfess with media success")

    def senddm(self, sender_id):
        notif1 = self.api.send_direct_message(sender_id, "Menfess has been posted")
        dm = self.api.get_direct_messages()
        for a in range(len(dm)):
            message = dm[a].message_create['message_data']['text']
        notifdm = self.api.send_direct_message(recipient_id=sender_id, text=message)
        self.api.delete_direct_message(notifdm.id)
        self.api.delete_direct_message(notif1.id)
        print("Message sent")
        time.sleep(10)

        return

    def dmfail(self, sender_id):
        notif2 = self.api.send_direct_message(sender_id, "Gagal posting karena lebih dari 280 huruf, twitter hanya mengizinkan 280 huruf maksimal maka menfess ditolak.")
        dm = self.api.get_direct_messages()
        for c in range(len(dm)):
            message = dm[c].message_create['message_data']['text']
        notiffail = self.api.send_direct_message(recipient_id=sender_id, text=message)
        self.api.delete_direct_message(notiffail.id)
        self.api.delete_direct_message(notif2.id)
        print("Message deleted")
        time.sleep(10)

        return








