import requests
from bs4 import BeautifulSoup
from configs.loginInfo import ConfigReader

def get_news_info():
    url = "https://tw-nba.udn.com/nba/index"


    response = requests.get(url)
    response.encoding = 'utf-8'

    soup = BeautifulSoup(response.text, 'html.parser')

    # print(soup)


    news_list = soup.find_all('li', class_='splide__slide')
    # print(news_list)
    output_list = []
    for news in news_list:
        title = news.find('a')['title']
        link = news.find('a')['href']
        item = {
            'title':title,
            'link':link
        }
        output_list.append(item)
        print(f"Title: {title}, Link: {link}")
        # print(output_list)
    return output_list

def get_db_url():
    Config = ConfigReader()
    db_config = Config.get_database_config()

    ip = db_config['host']
    user = db_config['user']
    port = db_config['port']
    password = db_config['password']
    database = db_config['database']

    return f"mysql+pymysql://{user}:{password}@{ip}:{port}",database

