import bs4, requests

# Ritorna i link trovati dalla ricerca
def queryScraper(ricerca):
    print("<Scraper>: Finding objects for query --> "+ ricerca)

    response = requests.get(ricerca)
    response.raise_for_status()

    # salvo il testo html della pagina
    soup=bs4.BeautifulSoup(response.text, 'html.parser')
    div_annunci=soup.find('div', class_='jsx-4116751698 items visible')
    a_annunci=div_annunci.find_all('a')
    link_annunci = [] #tutti gli annunci trovati sono in questo array
    for a_annuncio in a_annunci:
        link_annuncio = str(a_annuncio.get('href'))
        link_annunci.append(link_annuncio)

    return link_annunci



