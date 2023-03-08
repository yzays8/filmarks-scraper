import requests
from bs4 import BeautifulSoup

def is_long_review(content_card):
    if content_card.find('span', class_='c-content-card__readmore-review') is None:
        return False
    else:
        return True

def exist_review(soup):
    if soup.find('div', class_='p-contents-list') is None:
        return False
    else:
        return True

def get_information(content_card):
    info_dict = {}
    if is_long_review(content_card):
        url_moreReview = 'https://filmarks.com' + content_card.find('span', class_='c-content-card__readmore-review').find('a').get('href')
        content_more = BeautifulSoup(requests.get(url_moreReview).text, 'html.parser')
        info_dict['title'] = content_more.find('div', class_='p-timeline-mark__title').text
        if (temp:=content_more.find('div', class_='c-rating__score').text) == '-':
            info_dict['rate'] = -1
        else:
            info_dict['rate'] = float(temp)
        info_dict['review'] = content_more.find('div', class_='p-mark__review').text
    else:
        info_dict['title'] = content_card.find('h3', class_='c-content-card__title').text
        if (temp:=content_card.find('div', class_='c-rating__score').text) == '-':
            info_dict['rate'] = -1
        else:
            info_dict['rate'] = float(temp)
        info_dict['review'] = content_card.find('p', class_='c-content-card__review').text
    return info_dict

def print_info(info_dict):
    print('Title: ' + info['title'])
    if info['rate'] == -1:
        print('Rate: -')
    else:
        print('Rate: ' + str(info['rate']))
    if info['review'] == '':
        print('Review: -\n')
    else:
        print('Review: ' + info['review'] + '\n')

def sort_rate(info_all):
    return sorted(info_all, key=lambda x: x['rate'])


if __name__ == '__main__':
    user_name = input('Username: ')
    url_user = 'https://filmarks.com/users/' + user_name
    info_all = []
    is_first_page = True
    i = 1
    while True:
        res = requests.get(url_user)
        soup = BeautifulSoup(res.text, 'html.parser')
        if is_first_page:
            status = soup.find('p', class_='main__status')
            if status is not None:
                if status.text == '404 Not Found':
                    print('Username not found')
                    exit()
            is_first_page = False
        if exist_review(soup):
            content_set = soup.find_all('div', class_='c-content-card')
            for content_card in content_set:
                info = get_information(content_card)
                info_all.append(info)
                print_info(info)
        else:
            break
        i += 1
        url_user = 'https://filmarks.com/users/' + user_name + '?page=' + str(i)

    print('---------------------------------------------------\n')
    while True:
        if (want_sort := input('Do you want to sort reviews by rate? y/n: ')) == 'y':
            for info in sort_rate(info_all):
                print_info(info)
            break
        elif want_sort == 'n':
            break