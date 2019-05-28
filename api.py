import threading

import follower
import tokenizer
import tweet

import tweepy
import logging
import csv
import time
from model import *
from database import DataBase

try:
    import json
except ImportError:
    import simplejson as json

logging.basicConfig()
from datetime import datetime, timedelta

######################################API SETTINGS########################################

#ACCESS_TOKEN = '1092775756990742528-f3jdO4dHk6mz74xelnaIR5DanAWPm6'
#ACCESS_SECRET = 'ajiXNmSln042ivtOOTh9GYkh0vcJNZwiQAmZMuf6sRCtB'
#CONSUMER_KEY = 'nazYTA9BgmjpZSB54whfr4gkF'
#CONSUMER_SECRET = 'zOm049TtpKJ4zc36gqD3XV8xl4SYSvQJCz1AygEbDK0BVt5v37'

#ACCESS_TOKEN = '818456674507902977-CweXH1SJkOeyKLAc1EUnZ2JKSHpC83Z'
#ACCESS_SECRET = "kLla8weNLy1tfEdwEIlUmz9g1tV91sO7VHE5dOhyrYLsL"
#CONSUMER_KEY = "cZQqU0bI8Du4OAr3vqZFGH17C"
#CONSUMER_SECRET = "JuFRZeTaWVG48GYALBRDuaJHJr5LQVqBsFyDyyDxaUVYhu0rMz"

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

#api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)

##########################################################################################

class API :
    def __init__(self,idAccount):
        self.idAccount = idAccount
        self.listFollowers = self.getlistFollowers()


    def getlistFollowers(self):
        db = DataBase()
        followers = db.getFollowersdb()
        listFollowers = []
        for fol in followers :
            tweets = db.getTweetsdb(fol[0])#follower[0]=id du follower
            for tweetSolo in tweets:
                res = self.indexFollower(listFollowers, fol[0])

                if next(iter(res)):
                    # Si on ne connait pas le follower :
                    listFollowers.append(follower.Follower(fol[0], fol[1]))
                    # On crée et on ajoute le follower
                    listFollowers[res[True]].addTweet(tweet.Tweet(tweetSolo[2], tweetSolo[3], tokenizer.getWeight(tweetSolo[3])))
                    # On crée et on ajoute le tweet
                else:
                    # Si on connait pas follower :
                    listFollowers[res[False]].addTweet(tweet.Tweet(tweetSolo[2], tweetSolo[3], tokenizer.getWeight(tweetSolo[3])))
                    # On crée et on ajoute le tweet
        return listFollowers

    def indexFollower(self,listFollowers, id):
        for i in range(len(listFollowers)):
            if listFollowers[i].idF == id:  # check if the follower is already in the list
                res = {False: i}
                return res
        res = {True: len(listFollowers)}
        return res

    def setDateT(self,dateTweet):
        monthsDic = {"Jan": "01", "Feb": "02", "Mar": "03", "Apr": "04", "May": "05", "Jun": "06", "Jul": "07", "Aug": "08",
                     "Sep": "09", "Oct": "10", "Nov": "11", "Dec": "12"}
        dateToString = dateTweet[8:10] + "/" + monthsDic[dateTweet[4:7]] + "/" + dateTweet[-2:]
        d = datetime.strptime(dateToString, "%d/%m/%y")
        h = dateTweet[dateTweet.find(':') - 2:dateTweet.find(':')]
        m = dateTweet[dateTweet.find(':') + 1:dateTweet.find(':') + 3]
        d = d.replace(hour=int(h), minute=int(m))
        d = d + timedelta(hours=1)
        return d

    def traitementListe(self):
        db = DataBase()
        for follower in self.listFollowers:
            thread = threading.Thread(target=follower.updateWeightFollower())
            thread.start()
            thread.join()
            db.updateWeightF(follower.idF, follower.weight)
        self.listFollowers.sort(key=lambda follower: follower.weight, reverse=True)

#for follower in TwitterAPI.listFollowers:
    #follower.updateWeightFollower()
    #db.updateWeightF(follower.idF, follower.weight)
#TwitterAPI.listFollowers.sort(key=lambda follower: follower.weight, reverse=True)




##########################################################################################

#class CSVFile:
#
#
#    def writeBasicCSV(self):
#        data = []
#        with open('BasicData.csv', 'w', newline='') as fp:
#            a = csv.writer(fp, delimiter=',')
#            for follower in TwitterAPI.listFollowers:
#                for tweet in follower.listTweets:
#                    if tweet.content.startswith("RT"):
#                        type = 'RT'
#                    else:
#                        type = 'T'
#                    data.append([type, str(tweet.date)])
#                    time.sleep(10)
#            a.writerows(data)
#            print(data)
#            fp.close
#
#    def writeFollowerCSV(self):
#        data = []
#        with open('ListFollowers.csv', 'w', newline='') as fp:
#            a = csv.writer(fp, delimiter=',')
#            for follower in TwitterAPI.listFollowers:
#                data.append([follower.screen_name])
#                time.sleep(120)
#            a.writerows(data)
#            print(data)
#            fp.close
#
#    def writeTweetCSV(self):
#        data = []
#        with open('ListTweets.csv', 'w', newline='') as fp:
#            a = csv.writer(fp, delimiter=',')
#            for follower in TwitterAPI.listFollowers:
#                for tweet in follower.listTweets:
#                    if tweet.content.startswith("RT"):
#                        type = 'RT'
#                    else:
#                        type = 'T'
#                    data.append([follower.screen_name,type, str(tweet.date)])
#                    time.sleep(10)
#            a.writerows(data)
#            print(data)
#            fp.close

#BasicCSV = CSVFile()
#BasicCSV.writeBasicCSV()

#FollowerdataCSV = CSVFile()
#FollowerdataCSV.writeFollowerCSV()

#TweetdataCSV = CSVFile()
#TweetdataCSV.writeTweetCSV()

##########################################################################################
