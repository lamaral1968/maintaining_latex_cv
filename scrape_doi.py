__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017-2018, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Production"


from bs4 import BeautifulSoup
from splinter import Browser
import pymongo
from my_settings import PUBLICATION_TYPES, FLAGS, URLS
from my_mongo_db_login import DB_LOGIN_INFO


if __name__ == "__main__":
    connection = pymongo.MongoClient(DB_LOGIN_INFO['credentials'], DB_LOGIN_INFO['port'])
    db = connection['amaral_cv_data']

    print('Opened connection')

    # Create session for retrieval of data
    #
    cross_ref_url = URLS['doi']
    with Browser('chrome') as browser:
        for pub_type in PUBLICATION_TYPES:
            collection = db['publications' + '_' + pub_type.lower()]
            print('\n\n', pub_type.upper())

            paper_ids = []
            for paper in collection.find():
                paper_ids.append(paper['_id'])
            print('There are {} papers in this group'.format(len(paper_ids)))

            for paper_id in paper_ids:
                update = False
                if FLAGS['update_DOIs']:
                    update = True
                else:
                    paper = collection.find_one({'_id': paper_id})
                    if 'doi' not in paper.keys():
                        update = True

                if update:
                    title = paper['Title'].lower()
                    first_author = paper['Authors'].split()[0].replace("\`", '').replace("\'", '').replace("\:", '').lower()
                    paper_code = paper['Year'] + ' ' + first_author + ' ' + title
                    print(paper_code)

                    if 'doi' not in paper.keys():
                        new_title = title
                        new_author = first_author
                        success_flag = False
                        flag = 0

                        while True:
                            browser.visit(cross_ref_url)
                            browser.fill('auth', new_author)
                            browser.fill('title', paper['Journal'])
                            browser.fill('atitle', new_title)
                            if not paper['Volume']:
                                browser.fill('volume', paper['Volume'])
                            browser.fill('year', paper['Year'])
                            browser.find_by_name('view_records').click()

                            soup = BeautifulSoup(browser.html, 'html.parser')
                            item = soup.find('table', {'width': 600})

                            for child in item.findAll('tr'):
                                tmp = str( child.text )
                                if 'http' in tmp:
                                    print(tmp)
                                    collection.update_one( {'_id': paper_id}, {'$set': {'doi': tmp.strip()}} )
                                    success_flag = True
                                    if flag == 'title':
                                        collection.update_one({'_id': paper_id}, {'$set': {'Title_doi': new_title}})
                                    elif flag == 'author':
                                        collection.update_one({'_id': paper_id}, {'$set': {'Author_doi': new_author}})
                                    break

                            if success_flag:
                                break
                            else:
                                print(paper_code)
                                print('Not successful in getting doi')

                                a = input('Try with different title? [Y/n]  ')
                                if a == 'n' or a == 'N':
                                    a = input('Try with different author? [Y/n]  ')
                                    if a == 'n' or a == 'N':
                                        a = input('Enter doi? [Y/n]  ')
                                        if a == 'n' or a == 'N':
                                            break
                                        else:
                                            doi_input = input('Enter doi  ')
                                            collection.update_one({'_id': paper_id}, {'$set': {'doi': doi_input}})
                                            success_flag = True
                                            break
                                    else:
                                        new_author = input('Enter new name  ')
                                        flag = 'author'
                                else:
                                    new_title = input('Enter new title  ')
                                    flag = 'title'
