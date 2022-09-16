import requests
from bs4 import BeautifulSoup
import json


url = "https://mishka-knizhka.ru/skazki-pro-mashinki/"

headers = {
    "accept": "text/css,*/*;q=0.1",
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.163 Safari/537.36 OPR/67.0.3575.137"
}


def get_tales_urls():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    cards = soup.find_all("article", itemprop="blogPost")
    for card in cards:
        yield card.find("a").get("href")


def parse_tale():

    tales = []
    for tale_url in get_tales_urls():
        tale = {'url': tale_url}
        response = requests.get(tale['url'], headers=headers)
        soup = BeautifulSoup(response.text, "lxml")
        name = soup.find("h1").text.split("—")
        for i in range(len(name)):
            name[i] = name[i].strip()
        tale['name'] = name
        paragraphs = soup.find("div", class_="entry-content").find_all("p")

        tale['intro'] = paragraphs[0].text
        tale['text'] = ''
        for paragraph in paragraphs[1:]:
            cur_par = paragraph.text
            tale['text'] += cur_par
            if cur_par:
                tale['text'] += '\n'
        tales.append(tale)

    with open('tale.json', 'a') as jsn:
        json.dump(tales, jsn, indent=4, ensure_ascii=False)


def main():
    parse_tale()


if __name__ == '__main__':
    main()
