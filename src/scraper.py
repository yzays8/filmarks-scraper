import requests
import re
import sys

from typing import Dict, List

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

def is_long_review(content_card: Tag) -> bool:
    if content_card.find('span', class_='c-content-card__readmore-review') is None:
        return False
    return True

def get_info(content_card: Tag) -> Dict[str, str]:
    info: Dict[str, str] = {}

    if is_long_review(content_card):
        url_more_review = 'https://filmarks.com' + content_card.find('span', class_='c-content-card__readmore-review').find('a').get('href')
        content_more = BeautifulSoup(requests.get(url_more_review).text, 'html.parser')
        title_str: str = content_more.find('div', class_='p-timeline-mark__title').text
        match = re.search(r'(.+)\(([0-9]+)[^0-9]+\)', title_str)
        info['title'] = match.group(1)
        info['year'] = match.group(2)
        if (temp := content_more.find('div', class_='c-rating__score').text) == '-':
            info['rate'] = -1
        else:
            info['rate'] = float(temp)
        info['review'] = content_more.find('div', class_='p-mark__review').text
    else:
        title_str = content_card.find('h3', class_='c-content-card__title').text
        match = re.search(r'(.+)\(([0-9]+)[^0-9]+\)', title_str)
        info['title'] = match.group(1)
        info['year'] = match.group(2)
        if (temp := content_card.find('div', class_='c-rating__score').text) == '-':
            info['rate'] = -1
        else:
            info['rate'] = float(temp)
        info['review'] = content_card.find('p', class_='c-content-card__review').text

    assert info['title'] is not None
    assert info['year'] is not None
    assert info['rate'] is not None
    assert info['review'] is not None

    return info

def print_info(info: List[Dict[str, str]]) -> None:
    print('Title: ' + info['title'])
    print('Year: ' + info['year'])
    if info['rate'] == -1:
        print('Rate: -')
    else:
        print('Rate: ' + str(info['rate']))
    if info['review'] == '':
        print('Review: -\n')
    else:
        print('Review: ' + info['review'] + '\n')

def sort_rate(info_all: List[Dict[str, str]]) -> List[Dict[str, str]]:
    return sorted(info_all, key=lambda x: x['rate'])

def scrape(user_name: str) -> List[Dict[str, str]]:
    url_user = f'https://filmarks.com/users/{user_name}'
    info_all: List[Dict[str, str]] = []
    is_first_page = True
    i = 1
    while True:
        res = requests.get(url_user, timeout=(3.0, 7.5))
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError as e:
            if res.status_code == 404:
                if is_first_page:
                    sys.exit('Username not found')
                break
            elif res.status_code != 200:
                sys.exit('Connection error: ' + str(res.status_code))
        except requests.exceptions.Timeout as e:
            sys.exit('Timeout error')

        is_first_page = False

        soup = BeautifulSoup(res.text, 'html.parser')
        content_set: ResultSet[Tag] = soup.find_all('div', class_='c-content-card')
        for content_card in content_set:
            info = get_info(content_card)
            info_all.append(info)
        i += 1
        url_user = f'https://filmarks.com/users/{user_name}?page={str(i)}'
    return info_all
