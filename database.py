#from api import API
import mysql.connector


mydb = mysql.connector.connect(
    host='localhost',
    user='root',
    passwd='root',
    database='twitterdb')



class DataBase :
    def __init__(self):
        self.listFollowers = []
        self.listTweets = []
        #self.api = API("_agricool")
        self.mycursor = mydb.cursor()


    def buildDB(self,screen_name,name):
        self.createDB()
        self.fillFollowerInDB(screen_name,name)

    def createDB(self):
        """
        Delete the entire database and create a new empty one
        """
        self.mycursor.execute(" DROP Table IF EXISTS tweet")
        self.mycursor.execute(" DROP Table IF EXISTS follower")
        createFollowerTable = "CREATE TABLE follower (" \
                                "idF VARCHAR(255) NOT NULL,"\
                                "screen_name VARCHAR(255)," \
                                "name varchar(255)," \
                                "weight int," \
                                "PRIMARY KEY(idF)" \
                              ")"
        createTweetTable = "CREATE TABLE `tweet` (" \
                           "`idT` INT(10) NOT NULL AUTO_INCREMENT," \
                            "idF VARCHAR(255),"\
                           "date DATETIME," \
                           "content VARCHAR(1000)," \
                            "weight int(10),"\
                            "FOREIGN KEY(idF) REFERENCES follower(idF),"\
                           "PRIMARY KEY (`idT`)" \
                           ");"
        self.mycursor.execute(createFollowerTable)
        self.mycursor.execute(createTweetTable)
        mydb.commit()


    def fillFollowerInDB(self,id,screen_name,name):
        """
        Insert a Follower into the database
        """
        sqlInsertFollowers = "INSERT INTO follower (idF,screen_name, name) VALUES (%s,%s,%s)"
        args = (id,screen_name, name)
        self.mycursor.execute(sqlInsertFollowers,args)
        mydb.commit()


    def getFollowersdb(self):
        sqlgetFollowers = "SELECT * from twitterdb.follower;"
        self.mycursor.execute(sqlgetFollowers)
        records = self.mycursor.fetchall()
        #print("Total number of followers : ", self.mycursor.rowcount+"\n")
        #for row in records:
        #    print("Id = ", row[0], )
        #    print("Screen_name", row[1])
        #    print("Name = ", row[2], "\n")
        return records

    def insertTweetdb(self,idF,date,content):
        sqlInsertFollowers = "INSERT INTO tweet (idF,date, content) VALUES (%s,%s,%s)"
        args = (idF, date, content)
        self.mycursor.execute(sqlInsertFollowers, args)
        mydb.commit()

    def getTweetsdb(self,id):
        args=(id,)
        sqlGetTweets = "SELECT * from twitterdb.tweet where idF = %s"
        self.mycursor.execute(sqlGetTweets,args)
        records = self.mycursor.fetchall()
        return records

    def updateWeightF(self, idF, weight):
        updateTableFollower = "UPDATE follower SET weight = %s WHERE idF = %s"
        args = (weight, idF)
        self.mycursor.execute(updateTableFollower, args)
        mydb.commit()


# Constuit la DataBase