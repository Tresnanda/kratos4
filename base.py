import tweepy
from fungsi import Twitter
import time


tw = Twitter()

###pancing heroku222

def start():
    print("Starting up.")
    dms = list()
    while True:
        if len(dms) is not 0:     ##jika dmnya ga kosong maka
            for i in range(len(dms)):
                message = dms[i]['message']
                sender_id = dms[i]['sender_id']
                id = dms[i]['id']

                if len(message) is not 0 and len(message) <280:    ##limit kata twitter adalah 280 words
                    if "krts!" in message:  ##cek ada keyword atau tidak
                        if len(message) is not 0:
                            if dms[i]['media'] is None:
                                print("Menfess will be posted")
                                tw.post_tweet(message)  ##menfess dipost
                                tw.delete_dm(id)  ##dm dibersihkan
                            else:
                                print("Menfess will be posted with media")
                                print(dms[i]['shorted_media_url'])
                                tw.post_media(message, dms[i]['media'], dms[i]['shorted_media_url'])
                                tw.delete_dm(id)

                        else:
                            print("Message will be deleted because it's empty")
                            tw.delete_dm(id)

                    else:       ##ga ada keyword maka menfess ditolak
                        print("Menfess rejected because it doesnt contain the keyword")
                        tw.delete_dm(id)
                elif len(message) is not 0 and len(message) >280:
                    print("Menfess lebih dari 280 huruf, twitter hanya mengizinkan 280 huruf maksimal maka menfess ditolak.")
                    tw.delete_dm(id)
                    tw.dmfail(sender_id)

            dms = list()

        else:
            print("DM is empty")
            dms = tw.read_dm()
            if len(dms) is 0 or dms is None:
                time.sleep(60)
if __name__ == "__main__":
    start()

