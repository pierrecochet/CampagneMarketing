import datetime



class Frequences :
    def __init__(self,TwitterAPI):
        self.ActiviteParHeure = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        self.sommeActivite = 0
        self.TwitterAPI=TwitterAPI
        #self.ActivitesParHeure = self.calculActiviteHoraire()
        # Un tableau contenant 24 cases qui renseigne sur l'activité des followers sur chaque heure pendant 1 jour
        #self.ActivitesParHeure = [336]
        # Un tableau contenant 336 cases qui renseigne sur l'activité des followers sur chaque heure pendant 1 mois

    def getWeekday(self,YearTweet,MonthTweet,DayTweet):
        """
        :param YearTweet: L'année de publication du tweet
        :param MonthTweet: Le mois de publication du tweet
        :param DayTweet: Le jour de publication du tweet
        :return: Le jour de la semaine duquel le Tweet a été envoyé
        """
        return datetime.date(YearTweet, MonthTweet, DayTweet).strftime("%A")


    def calculActiviteHoraire(self):
        """
        On crée un tableau de taille 24 où chaque case représente une heure.
        On passe tous les tweets et on incrémente la case du tableau qui correspond à l'heure de publication du tweet
        :return: rien
        """
        ActivitesParHeure = []
        for follower in self.TwitterAPI.listFollowers:
            for tweet in follower.listTweets:
                print(tweet)
                heure = int(tweet.date[11:13])
                ActivitesParHeure [heure]+=1

    def setPeaksActivite(self,ExempleListeHeures):
        """
        On passe d'une liste d'heures de publications à une liste de nombre d'activité par heure
        :param ExempleListeHeures:
        :return:
        """
        ActiviteParHeure = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for h in ExempleListeHeures:
            ActiviteParHeure[h] += 1

    def nToWeekDay(self,numHour):
        numWeekday = numHour//24
        WeekdayDic = {0 :"lundi   ", 1 : "mardi   ",2: "mercredi",3: "jeudi   ",4: "vendredi",5: "samedi  ",6: "dimanche"}
        return WeekdayDic[numWeekday]

    def hBefore(self,numHour):
        return numHour%24

    def hAfter(self,numHour):
        return numHour%24+1

    def pourcentageActivite(self,hmax):
        if self.sommeActivite != 0:
            return (self.ActiviteParHeure[hmax] / self.sommeActivite)*100
        else:
            return 0

    def setWeekActivity(self,ListeDActivites1):
        for activite in ListeDActivites1:
            a = activite[0]*24+activite[1]
            self.ActiviteParHeure[a]+=1

    def getListActivite(self) :
        ListeDActivites1 = []
        for follower in self.TwitterAPI.listFollowers:
            for tweet in follower.listTweets :
                ListeDActivites1.append([int(tweet.date.weekday()),int(tweet.date.hour)])
        return ListeDActivites1

    def getActivity(self):

        """
        On a une liste de date on cherche les pics:
        
        On regarde les heures qui reviennent le plus 
        """




        ListeDActivites1 = self.getListActivite()



        self.setWeekActivity(ListeDActivites1)

        self.sommeActivite = float(sum(self.ActiviteParHeure))



        for i in range(6):
            hmax = self.ActiviteParHeure.index(max(self.ActiviteParHeure))
            print(self.pourcentageActivite(hmax), "% :",self.nToWeekDay(hmax), "(", self.hBefore(hmax), "-", self.hAfter(hmax), "))")
            del self.ActiviteParHeure[hmax]


        hmax1 = self.ActiviteParHeure.index(max(self.ActiviteParHeure))
        print("\nLa période d'activité maximale est le", self.nToWeekDay(hmax1), "entre", self.hBefore(hmax1), "h et", self.hAfter(hmax1), "h.")
        print("La semaine dernière, cette période représentait", self.pourcentageActivite(hmax1),"% de l'activité de vos Followers.")



        del self.ActiviteParHeure[hmax1]
        hmax2 = self.ActiviteParHeure.index(max(self.ActiviteParHeure))
        print("\nLa période d'activité maximale est le", self.nToWeekDay(hmax2), "entre", self.hBefore(hmax2), "h et", self.hAfter(hmax2), "h.")
        print("La semaine dernière, cette période représentait", self.pourcentageActivite(hmax2),"% de l'activité de vos Followers.")

        del self.ActiviteParHeure[hmax2]
        hmax3 = self.ActiviteParHeure.index(max(self.ActiviteParHeure))
        print("\nLa période d'activité maximale est le", self.nToWeekDay(hmax3), "entre", self.hBefore(hmax3), "h et", self.hAfter(hmax3), "h.")
        print("La semaine dernière, cette période représentait", self.pourcentageActivite(hmax3),"% de l'activité de vos Followers.")

        del self.ActiviteParHeure[hmax3]
        hmax4 = self.ActiviteParHeure.index(max(self.ActiviteParHeure))
        print("\nLa période d'activité maximale est le", self.nToWeekDay(hmax4), "entre", self.hBefore(hmax4), "h et", self.hAfter(hmax4), "h.")
        print("La semaine dernière, cette période représentait", self.pourcentageActivite(hmax4),"% de l'activité de vos Followers.")

        del self.ActiviteParHeure[hmax4]
        hmax5 = self.ActiviteParHeure.index(max(self.ActiviteParHeure))
        print("\nLa période d'activité maximale est le", self.nToWeekDay(hmax5), "entre", self.hBefore(hmax5), "h et", self.hAfter(hmax5), "h.")
        print("La semaine dernière, cette période représentait", self.pourcentageActivite(hmax5),"% de l'activité de vos Followers.")

