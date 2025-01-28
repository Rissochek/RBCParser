import requests
from bs4 import BeautifulSoup

# URL главной страницы РБК
url = 'https://www.rbc.ru/economics/'

# Получаем HTML-код страницы
response = requests.get(url)
print(f'Статус ответа: {response.status_code}')  # Отладочное сообщение

info = dict()

# Проверяем, что запрос успешен
if response.status_code == 200:
    # Парсим HTML-код с помощью BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Находим все заголовки новостей
    links = soup.find_all('a', class_='item__link rm-cm-item-link js-rm-central-column-item-link')
    print(f'Найдено заголовков: {len(links)}')  # Отладочное сообщение

    print(links[0]['href']) #nice

    paper = requests.get(links[0]['href'])
    if paper.status_code == 200:
        paper_soup = BeautifulSoup(paper.text, "html.parser")
        articles = paper_soup.find_all('h1', class_= "article__header__title-in js-slide-title")
        date_element = paper_soup.find('time', class_='article__header__date')
        if date_element and 'datetime' in date_element.attrs:
            datetime_value = date_element['datetime']
            print(f'Дата и время: {datetime_value}')
        print(articles[0].get_text(strip=True))
        data = paper_soup.find_all('div', class_="article__text article__text_free")
        info = data[0].find_all('p')
        for inf in info:
            print(inf.get_text(separator=" ", strip=True))
        overview = data[0].find_all('div', class_="article__text__overview")
        print(overview[0].get_text(separator=" ", strip=True))


else:
    print(f'Ошибка при получении страницы: {response.status_code}')