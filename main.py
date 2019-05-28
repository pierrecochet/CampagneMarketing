from datetime import time

#from testGetAll import initiateDb
import testGetAll
from api import API
from database2 import DataBase
import threading
from frequences import Frequences

if __name__ == '__main__':
    db = DataBase()
    account_screen_name = "_agricool"
    # pour s'assurer que la bdd est remplie avant de regarder les pics d'activités
    thread = threading.Thread(target=testGetAll.initiateDb(db,account_screen_name))
    thread.start()
    thread.join()
    TwitterAPI=API("_agricool")
    TwitterAPI.traitementListe()
    f1=Frequences(TwitterAPI)
    thread1 = threading.Thread(target=f1.getActivity())
    thread1.start()
    thread1.join()

