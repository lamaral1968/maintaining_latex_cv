import json
from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep
from random import randint
from datetime import date, timedelta


def match_ids(key, i, data, impact):
    """
    Match paper_id from publications and impact Json files

    :param key: str
    :param i: int
    :param data: dict
    :param impact: dict

    :return: update_lag, index: datetime.timedelta, int
    """
    #
    paper_id = data[key][i]['Paper_id']

    exists_in_impact = False
    for j in range(len(impact[key])):
        if impact[key][j]['Paper_id'] == paper_id:
            index = j
            exists_in_impact = True
            break

    # Create if it does not exist
    if not exists_in_impact:
        index = -1
        impact[key].append({})
        impact[key][-1]['Paper_id'] = paper_id
        impact[key][-1]['Alt_score'] = False
        impact[key][-1]['Sc_score'] = False
        impact[key][-1]['Update_date'] = None

    else: # Fix possible mistakes
        if impact[key][index]['Alt_score'] == '-':
            paper['Alt_score'] = False
        if impact[key][index]['Sc_cites'] == '-':
            paper['Sc_score'] = False

    # Check date of last update
    date_tuple = impact[key][index]['Update_date']
    if date_tuple != None:
        last_date = date(date_tuple[0], date_tuple[1], date_tuple[2]-1)
        update_lag = date.today() - last_date
    else:
        update_lag = timedelta(days = 500)

    return update_lag, index


if __name__ == '__main__':
    # Load json data
    json_file = './Json_files/publications.json'
    with open(json_file, 'r', encoding='utf-8') as file_in:
        data = json.load(file_in)

    json_file = './Json_files/impact.json'
    with open(json_file, 'r', encoding='utf-8') as file_in:
        impact = json.load(file_in)

    article_types = ['Editorial Material', 'Review Articles', 'Research Articles', 'Other Publications']
    print(article_types)

    # Create session for retrieval of data
    #
    url = "https://scholar.google.com"
    CVname = 'Amaral'

    with Browser() as browser:
        browser.visit(url)
        flag = True
        for key in article_types:
            for i in range(len(data[key])):
                paper = {}
                print(paper)
                paper['Title_Json'] = data[key][i]['Title']
                update_lag, index = match_ids(key, i, data, impact)
                print(impact[key][index]['Paper_id'], data[key][i]['Paper_id'], data[key][i]['Title'])
                if update_lag.days < 21:
                    print(update_lag.days)
                    break

                print(browser.url)
                browser.fill('q', data[key][i]['Title'] + ' ' + CVname)
                button = browser.find_by_name('btnG')
                button.click()
                if flag:
                    input('Enter key')
                    flag = False

                sleep(3)
                print(browser.url)

                if browser.url == url:
                    input('Enter key')
                    browser.fill('q', data[key][i]['Title'] + ' ' + CVname)
                    button = browser.find_by_name('btnG')
                    button.click()
                    print(browser.url)

                # Get html code and parse information
                html_content = browser.html
                soup = BeautifulSoup(html_content, 'html.parser')
                title = soup.find('h3', {'class': 'gs_rt'})
                print(title.text.encode('utf-8'))
                paper['Title_gs'] = title.text
                match = soup.find('div', {'class': 'gs_ri'})
                children = match.findAll('div')
                paper['Reference'] = children[0].text

                cites = children[2].findAll()
                paper['GS_cites'] = False
                paper['WoS_cites'] = False
                for item in cites:
                    if 'Cited by' in item.text:
                        paper['GS_cites'] = int(item.text.split()[-1])
                    if 'Web of' in item.text:
                        paper['WoS_cites'] = int(item.text.split(':')[1])
                print('---', paper['GS_cites'], paper['WoS_cites'])

                # Update citation information if there is a match of paper titles
                is_match = True
                if paper['Title_gs'].lower()[-15:] != paper['Title_Json'].lower()[-15:]:
                    if paper['Title_gs'].lower()[:15] != paper['Title_Json'].lower()[:15]:
                        is_match = False

                print(is_match)
                if is_match:
                    impact[key][index]['Update_date'] = (date.today().year, date.today().month, date.today().day)
                    impact[key][index]['WoS_cites'] = paper['WoS_cites']
                    impact[key][index]['GS_cites'] = paper['GS_cites']

                # Save data as json often so as not to loose data
                if not (i%10):
                    print('----------------Saving now!')
                    json_file = './Json_files/impact.json'
                    with open(json_file, 'w', encoding='utf-8') as file_out:
                        json.dump(impact, file_out, sort_keys = True, indent = 4)

                del paper
                sleep(4 + randint(0, 5))


