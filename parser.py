import requests
from bs4 import BeautifulSoup

class RBCParser:
    def __init__(self) -> None:
        self.url = 'https://www.rbc.ru/economics/'
        self.links = []
        self.parser_type = 'html.parser'
        self.links_class_name = 'item__link rm-cm-item-link js-rm-central-column-item-link'
        self.title_class_name = 'article__header__title-in js-slide-title'
        self.overview_class_name = 'article__text__overview'
        self.article_class_name = 'article__text article__text_free'
        self.datetime_class_name = 'article__header__date'
        self.data_store = []
                
    def scrape_links(self) -> None:
        response = requests.get(url=self.url)
        if (response.status_code != 200):
            print("Error: wrong status code", response.status_code)
            exit()

        scrape = BeautifulSoup(response.text, self.parser_type)
        self.links = [i['href'] for i in scrape.find_all('a', class_=self.links_class_name)]

    def scrape_datetime(self, scrape) -> str:
        date_element = scrape.find('time', class_=self.datetime_class_name)
        if date_element and 'datetime' in date_element.attrs:
            datetime_value = date_element['datetime']
        return datetime_value

    def scrape_article(self):
        count = 0
        for link in self.links:
            response = requests.get(link)
            if response.status_code != 200:
                print("Error: wrong status code", response.status_code)
                exit()

            scrape = BeautifulSoup(response.text, self.parser_type)
            article_inside = scrape.find("div", self.article_class_name)

            title = scrape.find('h1', class_=self.title_class_name).get_text(separator=" ", strip=True)
            datetime = self.scrape_datetime(scrape=scrape)
            overview = article_inside.find('div', class_=self.overview_class_name)
            if overview != None:
                overview = overview.get_text(separator=" ", strip=True)
            else:
                overview = '-'

            article_text = ' '.join([i.get_text(separator=" ", strip=True).replace('\xa0', ' ') for i in article_inside.find_all('p')])

            self.data_store.append({
                'title': title,
                'datetime': datetime,
                'overview': overview,
                'article_text': article_text,
                'source': 'РБК'
            })

    def get_full_data(self) -> list: #call this func only
        self.scrape_links()
        self.scrape_article()
        return self.data_store

            
            

