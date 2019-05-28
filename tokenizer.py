#on va faire le principe inverse d'un tokenizer dans le sens que l'on ne va pas supprimer des mots pour ne garder que les
#mots clefs intéressants, mais l'on va relever que les mots clefs intéressant à partir du banque de mots prédéfinis
#afin de donner un poid d'intérêt au tweets
#Dans notre cas nous travaillons avec agricool nous allons donc chercher des mots clefs en lien avec l'agriculture

def getWeight(content):

    keyWords = {"#agrifood":10,"@_agricool":10,"agriculture":9,"écologie":9,"écosystème":10,"press":4,"manger":6,"pesticide":8,"eat":6,
                "fruit":6,"légume":6,"strawberrie":5,"fraise":5,"framboise":5,"tasty":1,"goûtue":1,"délicieux":1,"healthy":5,"sain":5,"ecofriendly:6,"
                "l'agriculture":9,"culture":4,"climate":6,"futur":5,"pollution":5,"world":7,"geste":6,"tri":7}
    weight = 0
    for w in content.lower().split():  # s'assurer que tout est en minuscule
        for value in keyWords:
            tempvalue=value[:4]
            if w.startswith(tempvalue):
                weight += keyWords[value]
    return weight
