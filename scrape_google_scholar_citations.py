__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017-2018, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Production"

import pymongo
from bs4 import BeautifulSoup
from splinter import Browser
from time import sleep
from random import randint
from nltk.metrics import distance
from my_settings import PUBLICATION_TYPES, FLAGS, URLS
from my_mongo_db_login import DB_LOGIN_INFO, DATABASE_NAME


if __name__ == "__main__":
    connection = pymongo.MongoClient(DB_LOGIN_INFO['credentials'], DB_LOGIN_INFO['port'])
    db = connection[DATABASE_NAME]
    print('\nOpened connection')

    # Get WoS and Google Scholar citation counts
    url_gs = URLS['google_scholar']
    CVname = 'Amaral'
    with Browser('chrome') as browser:
        for pub_type in PUBLICATION_TYPES:
            flag = True
            collection_name = 'publications' + '_' + pub_type.lower()
            collection = db[collection_name]
            print('\n\n', pub_type.upper(), '--', collection_name)

            # Because we will be writing to database, which will change order of documents,
            # I collect a list of indices before any changes are made
            #
            paper_ids = []
            for paper in collection.find():
                paper_ids.append(paper['_id'])
            print('There are {} papers in this group'.format(len(paper_ids)))

            for paper_id in paper_ids:
                update = False
                if FLAGS['update_gs']:
                    update = True
                else:
                    paper = collection.find_one({'_id': paper_id})
                    if 'GS_cites' not in paper.keys():
                        update = True
                    elif paper['GS_cites'] == False:
                        update = True

                if update:
                    sleep(randint(0, 5))
                    title = paper['Title'].lower()
                    first_author = paper['Authors'].split()[0].replace("\`",
                                                                       '').replace("\'",
                                                                                   '').replace("\:",
                                                                                               '').lower()
                    paper_code = paper['Year'] + ' ' + first_author + ' ' + title
                    print(paper_code)

                    browser.visit(url_gs)
                    browser.fill('q', paper_code + ' ' + paper['Journal'])
                    button = browser.find_by_name('btnG')
                    button.click()
                    # Slow things down first time around because of browser coming up
                    if flag:
                        input('Enter information by browser and then enter something here')
                        flag = False


                    # Get html code and parse information
                    #
                    html_content = browser.html
                    soup = BeautifulSoup(html_content, 'html.parser')
                    tmp = soup.find('h3', {'class': 'gs_rt'})

                    # Google will find out you are scrapping and will send you test to make sure you are not a robot
                    # This will give you a change to answer tests to its satisfaction.
                    # At that point, answer question with any key
                    try:
                        title_gs = tmp.text
                        title_gs = title_gs.replace('&', 'and').lstrip('[PDF]').lstrip('[HTML]').lower()
                    except:
                        input('Enter information by browser and then enter something here')
                        browser.fill('q', paper_code + ' ' + paper['Journal'])
                        button = browser.find_by_name('btnG')
                        button.click()

                    match = soup.find('div', {'class': 'gs_ri'})
                    children = match.findAll('div')
                    reference_gs = children[0].text

                    cites = children[2].findAll()

                    gs_cites = False
                    wos_cites = False
                    for item in cites:
                        if 'Cited by' in item.text:
                            gs_cites = int(item.text.split()[-1])
                        if 'Web of' in item.text:
                            wos_cites = int(item.text.split(':')[1])

                    # Update citation information if there is a match of paper titles
                    is_match = False
                    if title_gs == title:
                        is_match = True
                    elif distance.edit_distance(title_gs, title) < 3:
                        is_match = True

                    print(is_match)
                    print(title_gs.encode('utf-8'))
                    print(title)
                    print('---', gs_cites, wos_cites)

                    if is_match:
                        collection.update_one({'_id': paper_id}, {'$set': {'GS_cites': gs_cites,
                                                                           'WoS_cites': wos_cites}})
                    else:
                        print('Titles were not a match!')
                        a = input('Do you want to update citations nonetheless?   [Y/n]')
                        if a.lower() != 'n':
                            collection.update_one({'_id': paper_id}, {'$set': {'GS_cites': gs_cites,
                                                                               'WoS_cites': wos_cites}})





