import threading
import utils.dbManager as db
import telebot
import os

CHATID = int(os.environ['CHATID'])
API_KEY = str(os.environ['APIKEY'])

class TGBot (threading.Thread):
    def __init__(self, magazziniere: db.FileManager):
        threading.Thread.__init__(self)
        self.magazziniere = magazziniere
        self.bot = telebot.TeleBot(API_KEY)
        self.context = 0

    def send(self, str):
        self.bot.send_message(CHATID, str)

    def run(self):
        print("<TGBot>: Thread started, type=" + str(type(CHATID)))

        @self.bot.message_handler(commands=['chatid'])
        def send_chatid(message):
            self.bot.send_message(message.chat.id, "user id: " + str(message.chat.id))
            print(str(type(message.chat.id)))

        @self.bot.message_handler(commands=['list'])
        def send_list(message):
            if str(message.chat.id) == str(CHATID):
                lista_ricerche = self.magazziniere.getListaRicerche()
                index = 1
                for ricerca in lista_ricerche:
                    nome = self.magazziniere.getFileName(ricerca)
                    self.bot.send_message(CHATID, str(index) + ") " + nome)  # TODO
                    index = index + 1

            else:
                self.bot.send_message(message.chat.id, "Utente non autorizzato")

        @self.bot.message_handler(commands=['add'])
        def wait_for_link(message):
            if str(message.chat.id) == str(CHATID):
                self.bot.send_message(CHATID, "Mandami il link della ricerca da aggiungere")
                self.context = 1
            else:
                self.bot.send_message(message.chat.id, "Utente non autorizzato")

        @self.bot.message_handler(func=lambda message: "https://www.subito.it" in message.text)
        def add_link_to_list(message):
            if str(message.chat.id) == str(CHATID):
                if self.context == 1:
                    nuovaRicerca = message.text
                    print("Inserendo nuovo link..")
                    self.magazziniere.aggiungiRicerca(nuovaRicerca)
                    self.bot.send_message(CHATID, "Link aggiunto correttamente")
                else:
                    self.bot.send_message(CHATID, "Errore di contesto")
                self.context = 0
            else:
                self.bot.send_message(message.chat.id, "Utente non autorizzato")


        @self.bot.message_handler(commands=['remove'])
        def wait_for_index_to_remove(message):
            if str(message.chat.id) == str(CHATID):
                self.context = 2
                self.bot.send_message(CHATID, "Inserisci il numero della ricerca da eliminare")
            else:
                self.bot.send_message(message.chat.id, "Utente non autorizzato")

        @self.bot.message_handler(func=lambda message: "" in message.text)
        def remove_link_from_list(message):
            if str(message.chat.id) == str(CHATID):
                if self.context == 2:
                    self.magazziniere.rimuoviRicerca(int(message.text))
                    self.bot.send_message(CHATID, "Elemento rimosso")
                else:
                    self.bot.send_message(CHATID, "Errore nella rimozione")
                self.context = 0
            else:
                self.bot.send_message(message.chat.id, "Utente non autorizzato")


        self.bot.infinity_polling(interval=4, timeout=20)

