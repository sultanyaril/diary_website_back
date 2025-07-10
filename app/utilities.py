from bs4 import BeautifulSoup


def remove_hypertext(html):
    return ' '.join(BeautifulSoup(html).findAll(text=True))