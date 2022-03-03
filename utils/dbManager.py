import threading
import utils.scraper as sc
import os

FILERICERCHE = 'database/ricerche.txt'


class FileManager:
    def __init__(self):
        self.mutex = threading.Lock()

    def aggiungiRicerca(self, link):
        #print("Aggiungo link alle ricerche.txt")
        self.mutex.acquire()
        f = open(FILERICERCHE, 'a')
        f.write('%s\n' % link)
        print("aggiunto alle ricerche:" + link)
        f.close()
        self.mutex.release()

    def rimuoviRicerca(self, index):
        # Prima leggo tutte le righe, poi le riscrivo tutte tranne la riga [indice] che salto

        # Popolo la lista delle ricerche
        lista_richerche = self.getListaRicerche()

        # Salvo in linkDaEliminare la stringa del link da eliminare
        # Servirà poi per eliminare il file nella cartella [links]
        counter = 1
        for ricerca in lista_richerche:
            if counter == index:
                linkDaEliminare = ricerca
            counter = counter + 1

        # Elimino la ricerca dal file ricerche.txt
        self.mutex.acquire()
        with open('%s' % FILERICERCHE, 'w') as f:
            counter = 1
            for ricerca in lista_richerche:
                if counter != index:
                    f.write('%s\n' % ricerca)
                counter = counter + 1
        f.close()

        # Ora elimino il file dalla cartella links (se esiste)
        nomeFile = self.getFileName(linkDaEliminare)
        if os.path.exists("database/links/"+nomeFile+".txt"):
            os.remove("database/links/"+nomeFile+".txt")
            print("File eliminato")
        else:
            print("Il file non era ancora stato creato")
        self.mutex.release()

    def getListaRicerche(self):
        self.mutex.acquire()
        f = open('%s' % FILERICERCHE, 'r')
        lista_ricerche = [riga.rstrip('\n') for riga in open(FILERICERCHE)]
        self.mutex.release()
        return lista_ricerche

    def getFileName(self,linkRicerca):
        start = str(linkRicerca).find("?q=") + len("?q=")
        if '&' in linkRicerca: # serve perchè le ricerche fatte della homepage sono diverse da quelle normali
            end = str(linkRicerca).find("&")
            nomeFile = linkRicerca[start:end] # trova il nome file a partire dalla query
        else:
            nomeFile = linkRicerca[start:]  # trova il nome file a partire dalla query
        return nomeFile

    #ritorna una lista con i link non già presenti
    def trovaNuoviLink(self, linkRicerca):

        # Apro/creo il file di testo con i link già trovati per una determinata ricerca.
        # Il nome del file è determinato dalla query, sottostringa del link 'ricerca' dato.
        nomeFile = self.getFileName(linkRicerca)

        # Trovo la lista di tutti gli annunici aprendo il link della ricerca utilizzando utils/scraper.py
        link_annunci = sc.queryScraper(linkRicerca)

        # SEZIONE CRITICA
        self.mutex.acquire()
        f = open('database/links/'+nomeFile+'.txt', 'a+')
        old_link_annunci = [riga.rstrip('\n') for riga in open('database/links/'+nomeFile+'.txt')]
        new_link_annunci = []
        for link_annuncio in link_annunci:
            if link_annuncio not in old_link_annunci:
                print("Nuovo annuncio trovato: " + link_annuncio)
                new_link_annunci.append(link_annuncio)
                f.write('%s\n' % link_annuncio)
        f.close()
        self.mutex.release()
        # FINE SEZIONE CRITICA

        return new_link_annunci