import utils.dbManager as dbManager
import backgroundChecher
import telegramBot


def cliControl():
    print("Command line interface enabled")
    while 1:
        value = input("")

        if value == "help":
            print("Available commands:")
            print("- help\n- list\n- add\n- remove")

        elif value == "list":
            lista_ricerche = magazziniere.getListaRicerche()
            index = 1
            for ricerca in lista_ricerche:
                nome = magazziniere.getFileName(ricerca)
                print(str(index) + "> " + nome)
                index = index + 1

        elif value == "add":
            link = input("Inserisci il link della nuova ricerca: ")
            magazziniere.aggiungiRicerca(link)

        elif value == "remove":
            index = input("Inserisci il numero della ricerca da eliminare: ")
            magazziniere.rimuoviRicerca(int(index))

        else:
            print("Command not found, 'help' for a list of commands")


if __name__ == '__main__':

    # Oggetto condiviso, si occupa di gestire l'accesso alle risorse dei thread
    magazziniere = dbManager.FileManager()

    # Creo e start il thread del bot di Telegram
    tBot = telegramBot.TGBot(magazziniere)
    tBot.start()

    # Creo e start il thread che controlla se ci sono nuovi articoli
    backckThread = backgroundChecher.BackgroundChecker(magazziniere, tBot)
    backckThread.start()

    cliControl()
