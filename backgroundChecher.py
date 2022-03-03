import threading
import utils.dbManager as db
from time import sleep
import os
from telegramBot import TGBot

CHATID = os.environ['CHATID']
API_KEY = os.environ['APIKEY']

#Questa sezione verificherà in contunuazione se ci sono nuovi link
class BackgroundChecker (threading.Thread):
    def __init__(self, magazziniere: db.FileManager, tg: TGBot):
        threading.Thread.__init__(self)
        self.magazziniere = magazziniere
        self.tg = tg

    def run(self):
        print("<backgroundChecker> thread started")
        while 1:
            lista_ricerche = self.magazziniere.getListaRicerche()
            for linkRicerca in lista_ricerche:
                new_link_annunci = self.magazziniere.trovaNuoviLink(linkRicerca)

                for annuncio in new_link_annunci:
                    self.tg.bot.send_message(CHATID, annuncio)

                # print ("<Scraper>: Waiting 2 seconds..")
                sleep(2) # Aspetto 2 secondi per evitare rate-limit

            print("<Scraper>: Check finished, waiting 5 minutes..")
            sleep(300) #aspetto 5 minuti




