import argparse

from scraper import *

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Get reviews from filmarks',
                                     usage='python3 fil.py [-u <username>] [-n]')
    parser.add_argument('-n', '--no-asking', help='ask nothing', action='store_true')
    parser.add_argument('-u', '--username', help='username', nargs='?')
    return parser.parse_args()

def main() -> None:
    args = parse_args()

    if args.username is None:
        user_name = input('Username: ')
    else:
        user_name = args.username

    require_sort = False
    if args.no_asking is False:
        while True:
            if (want_sort := input('Do you want to sort reviews by rate? y/n: ').lower()) in ['y', 'yes']:
                require_sort = True
                break
            elif want_sort in ['n', 'no']:
                break

    info_all = scrape(user_name)
    if require_sort:
        info_all = sort_rate(info_all)

    for info in info_all:
        print_info(info)

if __name__ == '__main__':
    main()