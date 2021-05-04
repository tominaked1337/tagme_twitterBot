import tweepy
import time

from tweepy import Status

from keys import *
from currency import *
from search_gif import get_gif, remove_gif
from tracker_db import track_tweet, search_by_date

#Auth With Tweepy
auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth, wait_on_rate_limit=True)

# File used to store last used or retrieved id
FILE_NAME = 'last_seen_id.txt'

# Retrieve last seen id from txt file mentioned above
def retrieve_last_seen_id(file_name):
    f_read = open(file_name, 'r')
    last_seen_id = int(f_read.read().strip())
    f_read.close()
    return last_seen_id


# store the last seen id for next time so that the same tweets are not accessed everytime
def store_last_seen_id(last_seen_id, file_name):
    f_write = open(file_name, 'w')
    f_write.write(str(last_seen_id))
    f_write.close()
    return


def find_keywords():
    print('retrieving and replying to tweets...', flush=True)
    
    #add last seen id for running script from last endpoint
    last_seen_id = retrieve_last_seen_id(FILE_NAME)

    #track tweets from @whale_alert. Limited 3000 tweets download.
    for timeline_tweet in tweepy.Cursor(api.user_timeline, screen_name='whale_alert').items(3000):
        last_seen_id = timeline_tweet.id
        store_last_seen_id(last_seen_id, FILE_NAME)
        # keyword to find
        if 'transferred' in timeline_tweet.text.lower():
            if track_tweet(timeline_tweet):
                print("tweet stored")




def reply_mentions():
    try:
        print('retrieving and replying to tweets...', flush=True)
        # add last seen id for running script from last endpoint
        last_seen_id = retrieve_last_seen_id(FILE_NAME)

        mentions = api.mentions_timeline()

        for mention_to_reply in reversed(mentions):
            #print(str(mention_to_reply.id) + ' - ' + mention_to_reply.full_text, flush=True)
            #Check if the mention is new, guided by the id
            if mention_to_reply.id > last_seen_id:
                last_seen_id = mention_to_reply.id
                store_last_seen_id(last_seen_id, FILE_NAME)
                print("new mention -> ", mention_to_reply.text)

                if '-top5' in mention_to_reply.text:
                    fulltw = mention_to_reply.text
                    date = fulltw[fulltw.find('-top5')+6:]
                    top5 = search_by_date(date)

                    r = "Top 5 higher transactions from {}" \
                    "\n1. {} ({})" \
                    "\n2. {} ({})" \
                    "\n3. {} ({})" \
                    "\n4. {} ({})" \
                    "\n5. {} ({})".format(date,top5[0]['amount'],top5[0]['details'],top5[1]['amount'],top5[1]['details'],top5[2]['amount'],top5[2]['details'],top5[3]['amount'],top5[3]['details'],top5[4]['amount'],top5[4]['details'])

                    api.update_status('@' + mention_to_reply.user.screen_name + " " + r, mention_to_reply.id)
                    print("replied successfully")

                elif '-usd' in mention_to_reply.text:
                    usd_currency = getUSDcurrency()
                    api.update_status('@' + mention_to_reply.user.screen_name + " " + usd_currency, mention_to_reply.id)
                    print("replied successfully")
                elif '-btc' in mention_to_reply.text:
                    btc_currency = getBTCcurrency()
                    api.update_status('@' + mention_to_reply.user.screen_name + " " + btc_currency, mention_to_reply.id)
                    print("replied successfully")

                elif '-gif' in mention_to_reply.text:
                    fullTweet = mention_to_reply.text
                    word = fullTweet[fullTweet.find('-gif')+5:]
                    print(word)
                    gif = get_gif(word)
                    api.update_with_media(gif, status= '@' + mention_to_reply.user.screen_name, in_reply_to_status_id= mention_to_reply.id)
                    print("replied successfully")
                    # once the mention with the gif attached is replied, the file is removed waiting for another request
                    remove_gif()

                else:
                    api.update_status('@' + mention_to_reply.user.screen_name + " Sorry, I could'nt find any existing command in your Tweet. Please, try again." , mention_to_reply.id)

    except tweepy.TweepError as e:
        print(e.reason, "Error")


while True:
    # Run Script
    reply_mentions()
    #find_keywords()
    time.sleep(15)
