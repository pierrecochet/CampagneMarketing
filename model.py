import time
from datetime import datetime, timedelta

import tweepy
import csv
from database import *
import mysql.connector

mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root',
    database='twitterdb')
mycursor = mydb.cursor()

#ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
#ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
#CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
#CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

ACCESS_TOKEN = '818456674507902977-CweXH1SJkOeyKLAc1EUnZ2JKSHpC83Z'
ACCESS_SECRET = 'kLla8weNLy1tfEdwEIlUmz9g1tV91sO7VHE5dOhyrYLsL'
CONSUMER_KEY = 'cZQqU0bI8Du4OAr3vqZFGH17C'
CONSUMER_SECRET = 'JuFRZeTaWVG48GYALBRDuaJHJr5LQVqBsFyDyyDxaUVYhu0rMz'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)


def get_followers(user_name):
    """
    get a list of all followers of a twitter account
    :param user_name: twitter username without '@' symbol
    :return: list of usernames without '@' symbol
    """
    api = tweepy.API(auth)
    followers = []
    for page in tweepy.Cursor(api.followers, screen_name=user_name, wait_on_rate_limit=True,count=20).pages(1):
    #for page in tweepy.Cursor(api.followers, screen_name=user_name).pages(2):
        try:
            followers.extend(page)
        except tweepy.TweepError as e:
            print("Going to sleep:", e)
            time.sleep(60)
    return followers






def save_followers_to_db(user_name, data,db):
    """
    saves json data in the database by creating followers identified by their screen_name
    :param data: data recieved from twitter
    :return: None
    """
    db.createDB() #!!!!ATTENTION !!!! CA DROP LES TABLES ATTENTION
    for profile_data in data:
        id = profile_data._json["id"]
        screen_name = profile_data._json["screen_name"]
        name = profile_data._json["name"]
        db.fillFollowerInDB(id,screen_name,name)


def insertTweet(db):
    records = db.getFollowersdb()
    followers = []
    for row in records:
        tweets = getTweetsFollower(row[0])
        for tweet in tweets:
            soloTweet = tweet._json
            date = setDateT(soloTweet['created_at'])  # On calcule et on stocke la date du tweet
            content = soloTweet['full_text']
            db.insertTweetdb(row[0],date,content)




def getTweetsFollower(followerId):
    tweets = []
    api = tweepy.API(auth)
    try:#certains comptes sont protected du coup ça plante quand on veut prendre les tweets du coup il faut faire un try catch
        for status in tweepy.Cursor(api.user_timeline, screen_name=api.get_user(followerId).screen_name,tweet_mode="extended").items(2):
            try:
                tweets.append(status)
            except tweepy.TweepError as e:
                print("Going to sleep:", e)
                time.sleep(60)
    except tweepy.TweepError:
        print("protected account")
    return tweets
#!!!!!!!!!!!!!!!!!!!!!!!!!!! TO DELETE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!





def setDateT(dateTweet):
    monthsDic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                 "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
    dateToString = dateTweet[8:10] + "/" + monthsDic[dateTweet[4:7]] + "/" + dateTweet[-2:]
    d = datetime.strptime(dateToString, "%d/%m/%y")
    h = dateTweet[dateTweet.find(':') - 2:dateTweet.find(':')]
    m = dateTweet[dateTweet.find(':') + 1:dateTweet.find(':') + 3]
    d = d.replace(hour=int(h), minute=int(m))
    d = d + timedelta(hours=1)
    return d


def initiateDb(db,account):
    followers = get_followers(account)
    save_followers_to_db(account, followers,db)
    insertTweet(db)


#!!!!!!!!!!!!!!!!!!!!!!!!!!! TO DELETE !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

if __name__ == '__main__':

    db= DataBase()

    initiateDb(db,"_agricool")
