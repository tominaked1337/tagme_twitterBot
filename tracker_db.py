
#set up MongoDB conn
from pymongo import MongoClient
import re

client = MongoClient('mongodb://localhost:27017/')

db = client["WhaleAlert_Tracker"]

col = db["tracking"]



def track_tweet(tweet):
    full_tweet = tweet.text
    transfer_values = full_tweet[full_tweet.find('(') + 1:full_tweet.find(')')].replace(",", "").split(" ")
    amount_usd = int(transfer_values[0])
    currency = transfer_values[1]
    tweet_url = 'https://twitter.com/twitter/statuses/' + tweet.id_str
    # extract only the url containing the transaction details from the tweet
    details = re.search("(?P<url>https?://[^\s]+)", tweet.text).group("url")

    cursor = col.find({})
    ids = []
    for i in cursor:
        ids.append(i['tweet_id'])

    #apply only for transfers higher than 1MM USD

    while tweet.id_str not in ids:
        tweet_data = {'tweet_id':tweet.id_str,
                      'date':tweet.created_at.strftime('%Y-%m-%d'),
                      'amount':amount_usd,
                      'currency': currency,
                      'tweet_url':tweet_url,
                      'details':details}

        col.insert_one(tweet_data)

        ids.clear()

        return True


def search_by_date(date):
    cursor = col.find({'date':date}).sort("amount", -1)
    c = 0
    top5tw = []
    for i in cursor:
        if c != 5:
            c+=1
            top5tw.append(i)

    return top5tw
