import glob
import json
import requests
import pandas as pd
from bs4 import BeautifulSoup

session = requests.Session()


def login():
    print('Login')
    datas = {
        'username': 'user',
        'password': 'user12345'
    }

    result = session.post('http://localhost:5000/login', data=datas)

    soup = BeautifulSoup(result.text, 'html.parser')

    page_item = soup.find_all('li', attrs={'class': 'page-item'})
    total_page_item = len(page_item) - 2

    return total_page_item


def get_urls(page):
    print('Getting urls....{}'.format(page))

    params = {
        'page': page
    }

    result = session.get('http://localhost:5000/', params=params)

    soup = BeautifulSoup(result.text, 'html.parser')
    titles = soup.find_all('h4', attrs={'class': 'card-title'})
    urls = []

    for title in titles:
        url = title.find('a')['href']
        urls.append(url)

    return urls


def get_detail(url):
    print('Get detail {} '. format(url))
    result = session.get('http://localhost:5000'+url)

    soup = BeautifulSoup(result.text, 'html.parser')
    title = soup.find('title').text.strip()
    price = soup.find('h4', attrs={'class': 'card-price'}).text.strip()
    stock = soup.find('span', attrs={'class': 'card-stock'}).text.strip().replace('stock: ', '')
    category = soup.find('span', attrs={'class': 'card-category'}).text.strip().replace('category: ', '')
    description = soup.find('p', attrs={'class': 'card-text'}).text.strip().replace('Description: ', '')

    dict_data = {
        'title': title,
        'price': price,
        'stock': stock,
        'category': category,
        'description': description
    }

    with open('./results/{}.json'.format(url.replace('/', '')), 'w') as outfile:
        json.dump(dict_data, outfile)

def create_csv():
    files = sorted(glob.glob('./results/*.json'))

    datas = []

    for file in files:
        with open(file) as json_file:
            data = json.load(json_file)
            datas.append(data)

    df = pd.DataFrame(datas)
    df.to_csv('results_scrap.csv', index=False)

    print('csv generated.....')

def run():
    total_pages = login()

    options = int(input('Input option number:\n1.collection all url\n2.get etail semua product\n3.create csv \n'))
    if options == 1:
        total_urls = []
        for i in range(total_pages):
            page = i + 1
            urls = get_urls(page)
            total_urls += urls
        with open('all_url_product.json', 'w') as outfile:
            json.dump(total_urls, outfile)

    if options == 2:
        with open('all_url_product.json') as json_file:
            all_url = json.load(json_file)
        for url in all_url:
            get_detail(url)

    if options == 3:
        create_csv()






if __name__ == '__main__':
    run()