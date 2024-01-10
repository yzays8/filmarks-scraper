import requests

from bs4 import BeautifulSoup
from bs4.element import Tag

def is_long_review(content_card: Tag) -> bool:
    if content_card.find('span', class_='c-content-card__readmore-review') is None:
        return False
    return True

def get_information(content_card: Tag) -> dict:
    info = {}

    if is_long_review(content_card):
        url_moreReview = 'https://filmarks.com' + content_card.find('span', class_='c-content-card__readmore-review').find('a').get('href')
        content_more = BeautifulSoup(requests.get(url_moreReview).text, 'html.parser')
        info['title'] = content_more.find('div', class_='p-timeline-mark__title').text
        if (temp:=content_more.find('div', class_='c-rating__score').text) == '-':
            info['rate'] = -1
        else:
            info['rate'] = float(temp)
        info['review'] = content_more.find('div', class_='p-mark__review').text
    else:
        info['title'] = content_card.find('h3', class_='c-content-card__title').text
        if (temp:=content_card.find('div', class_='c-rating__score').text) == '-':
            info['rate'] = -1
        else:
            info['rate'] = float(temp)
        info['review'] = content_card.find('p', class_='c-content-card__review').text

    return info

def print_info(info: dict) -> dict:
    print('Title: ' + info['title'])
    if info['rate'] == -1:
        print('Rate: -')
    else:
        print('Rate: ' + str(info['rate']))
    if info['review'] == '':
        print('Review: -\n')
    else:
        print('Review: ' + info['review'] + '\n')

def sort_rate(info_all: list) -> list:
    return sorted(info_all, key=lambda x: x['rate'])
