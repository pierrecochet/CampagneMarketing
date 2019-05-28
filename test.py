import follower
import tokenizer
import csv
try:
    import json
except ImportError:
    import simplejson as json
import tweepy
import logging
import tweet
logging.basicConfig()
from datetime import datetime, timedelta

# Variables that contains the user credentials to access Twitter API

"""
ACCESS_TOKEN = '6895181-SqAfibTTTPj426Njs5DoZPw4WOtkDeghHF9cHu8IM'
ACCESS_SECRET = 'TDSNRDwsmHVxVISOpowpADB6f3SnvAu6eOcLg7PGlwDjn'
CONSUMER_KEY = 'qFBm7PP8yvBO87EuvGCmQ'
CONSUMER_SECRET = 'UrVAZEPoFtcFNh20ilEae18yjQ2MdnH44Dz2wtpsKk'
"""

ACCESS_TOKEN = '1092775756990742528-P8nXtZHBbeHYswqC7frHyNjqq3FK4l'
ACCESS_SECRET = 'nui0bVJpTJTIz9KfmIqAgqN3G1hjVRYGGj4NBkTSyq9C8'
CONSUMER_KEY = 'SMjIKcwMnReu15Hp6XzalL45U'
CONSUMER_SECRET = 'Mb46UEuT390OVtwIZVPLzySS2S6gmPzOzrvnipvEyfE534yIwz'


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_TOKEN, ACCESS_SECRET)

# Create the api to connect to twitter with your creadentials
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, compression=True)
#---------------------------------------------------------------------------------------------------------------------
# wait_on_rate_limit= True;  will make the api to automatically wait for rate limits to replenish
# wait_on_rate_limit_notify= Ture;  will make the api  to print a notification when Tweepyis waiting for rate limits to replenish
#---------------------------------------------------------------------------------------------------------------------


#---------------------------------------------------------------------------------------------------------------------
# This is the equivalent of /timeline/home on the Web.
#---------------------------------------------------------------------------------------------------------------------


def getNbFollowers(idAccount,nbFollowersToGet):
    """
    :param idAccount: La compte dont on souhaite récupérer les followers
    :return: Une liste des followers d'un compte
    """
    list=[]
    for status in tweepy.Cursor(api.followers_ids, id = idAccount).items(nbFollowersToGet):
        list.append(status)
    return list

ids = getNbFollowers("_agricool",2)

print("============ID des followers récupérés============\n",ids )




"""
listTest=[]
for i in range (10):
    listTest.append(ids[i])

print(listTest)
"""

def setDateT(dateTweet):
    monthsDic  = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06","Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    dateToString = dateTweet[8:10]+"/"+monthsDic[dateTweet[4:7]]+"/"+dateTweet[-2:]
    d = datetime.strptime(dateToString,"%d/%m/%y")
    h = dateTweet[dateTweet.find(':')-2:dateTweet.find(':')]
    m = dateTweet[dateTweet.find(':')+1:dateTweet.find(':')+3]
    d = d.replace(hour=int(h),minute=int(m))
    d = d + timedelta(hours=1)
    return d



def indexFollower(listFollowers, id) :
    res={}
    for i in range(len(listFollowers)):
        if listFollowers[i].idF == id: # check if the follower is already in the list
            res={False:i}
            return res
    res={True:len(listFollowers)}
    return res

def getlistFollowers(ids):
    listFollowers=[]
    for i in range(len(ids)):
    # Pour chaque follower sélectionné
        for status in tweepy.Cursor(api.user_timeline, screen_name=api.get_user(ids[i]).screen_name, tweet_mode='extended').items():
            # On parcoure ces 2 derniers tweets pour récupérer les infos suivantes :
            tweetFeed = status._json
            print(tweetFeed)
            date = setDateT(tweetFeed['created_at']) # when the tweet posted
            content = tweetFeed['full_text'] # content of the tweet
            screen_name = api.get_user(ids[i]).screen_name
            res=indexFollower(listFollowers,ids[i])
            if next(iter(res)) :
                listFollowers.append(follower.Follower(ids[i],screen_name))
                listFollowers[res[True]].addTweet(tweet.Tweet(date, content, tokenizer.getWeight(content)))
            else:
                listFollowers[res[False]].addTweet(tweet.Tweet(date, content,tokenizer.getWeight(content)))

    return listFollowers

listFollowers = getlistFollowers(ids)


data=[]
with open('data.csv', 'w', newline='') as fp:
    a = csv.writer(fp, delimiter=',')

    for follower in listFollowers:


        #print(follower.screen_name)
        for tweet in follower.listTweets :
            if tweet.content.startswith("RT"):
                type = 'RT'
            else : type = 'T'
            #data.append([type,str(tweet.date)])


            #print(tweet.date)
            #print(tweet.content)
            #print(tweet.weight)
            #print('-----------------------------------------------------------------------------------------------\n')

        #print("=====================================================================================================\n")

a.writerows(data)

print(data)

