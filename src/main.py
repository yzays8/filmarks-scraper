import argparse
import requests
import sys

from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag

from scraper import *

def main() -> None:
    parser = argparse.ArgumentParser(description='Get reviews from filmarks',
                                     usage='python3 fil.py [-u <username>] [-n]')
    parser.add_argument('-n', '--no-asking', help='ask nothing', action='store_true')
    parser.add_argument('-u', '--username', help='username', nargs='?')
    args = parser.parse_args()

    if args.username is not None:
        user_name = args.username
    else:
        user_name = input('Username: ')
    url_user = 'https://filmarks.com/users/' + user_name
    info_all = []
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
            info = get_information(content_card)
            info_all.append(info)
            print_info(info)
        i += 1
        url_user = 'https://filmarks.com/users/' + user_name + '?page=' + str(i)

    if args.no_asking is not True:
        print('---------------------------------------------------\n')
        while True:
            if (want_sort := input('Do you want to sort reviews by rate? y/n: ')).lower() in ['y', 'yes']:
                for info in sort_rate(info_all):
                    print_info(info)
                break
            elif want_sort.lower() in ['n', 'no']:
                break

if __name__ == '__main__':
    main()