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
from nltk.metrics import distance
from my_settings import PUBLICATION_TYPES, FLAGS, URLS
from my_mongo_db_login import DB_LOGIN_INFO, DATABASE_NAME


if __name__ == "__main__":
    connection = pymongo.MongoClient(DB_LOGIN_INFO['credentials'], DB_LOGIN_INFO['port'])
    db = connection[DATABASE_NAME]
    print('\nOpened connection')

    # Scrape Scopus citation data
    #
    url_scopus = URLS['scopus']
    with Browser('chrome') as browser:
        scopus_papers = []
        browser.visit(url_scopus)
        a = input('Enter key')

        counter = 0
        while True:
            soup = BeautifulSoup(browser.html, 'html.parser')
            results_table = soup.find('table', {'id': 'srchResultsList'})
            rows = results_table.findAll('tr')
            for row in rows:
                columns = row.findAll('td')
                if len(columns) == 5:
                    title = columns[0].text.strip()
                    authors = columns[1].text.strip()
                    year = columns[2].text.strip()
                    reference = columns[3].text.strip()
                    citations = columns[4].text.strip()

                    first_author = authors.split()[0].lower().strip(',').strip()

                    # There are issues with alternative last names for some of my publications
                    #           Delete 'if' conditions below or replace in case you have similar issues
                    #
                    if first_author == 'nunes':
                        first_author = 'amaral'
                    if first_author == 'auto':
                        first_author = 'moreira'

                    # Scopus includes citations to versions published in book chapters and
                    # includes statement about open access. These must be removed
                    #
                    clean_title = title.lower().replace('open access', ' ').replace('book chapter', ' ').strip()
                    scopus_id = (year + ' ' + first_author + ' ' + clean_title)

                    scopus_papers.append({'_id': scopus_id, 'title': title, 'year': year, 'authors': authors,
                                          'journal': reference, 'citations': citations})
            print(len(scopus_papers))
            print('done cleanly')

            # Click for next page -- issue arises when getting to last set of pages since there no longer is a
            #                        button to advance several pages at once
            #
            try:
                button = browser.find_link_by_partial_href('NextPageButton')
                if counter < 5:
                    button.first.click()
                    counter += 1
                else:
                    button.last.click()
            except:
                break
        print('Got all Scopus papers')

    # Add collected citations to database by matching papers
    #
    for pub_type in PUBLICATION_TYPES:
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
            if FLAGS['update_scopus']:
                update = True
            else:
                paper = collection.find_one({'_id': paper_id})
                if 'Scopus_cites' not in paper.keys():
                    update = True
                elif not paper['Scopus_cites']:
                    update = True

            if update:
                new_title = paper['Title']
                new_author = paper['Authors'].split()[0]

                flag = 0
                matches = []
                while len(matches) == 0:
                    title = new_title.lower()
                    first_author = new_author.replace("\`", '').replace("\'", '').replace("\:", '').lower()
                    paper_code = paper['Year'] + ' ' + first_author + ' ' + title
                    print('----', paper_code)

                    for i, scopus in enumerate(scopus_papers):
                        if scopus['_id'][:] == paper_code[:].strip():
                            matches.append(i)
                        elif distance.edit_distance(scopus['_id'], paper_code.strip()) < 5:
                            if scopus['_id'][:4] == paper_code[:4]:
                                matches.append(i)

                    if len(matches) == 0:
                        print(paper_code)
                        print('Not successful in matching')
                        a = input('Try with different title? [Y/n]  ')
                        if a == 'n' or a == 'N':
                            a = input('Try with different author? [Y/n]  ')
                            if a == 'n' or a == 'N':
                                break
                            else:
                                new_author = input('Enter new name  ')
                                flag = 'author'
                        else:
                            new_title = input('Enter new title  ')
                            flag = 'title'

                # Add Scopus specific information and Scopus citations
                # These could be used to avoid entering correct information for paper matching with Scopus
                #
                if flag == 'title':
                    collection.update_one({'_id': paper_id}, {'$set': {'Title_scopus': new_title}})
                elif flag == 'author':
                    collection.update_one({'_id': paper_id}, {'$set': {'Author_scopus': new_author}})

                citations = 0
                for k in matches:
                    citations += int(scopus_papers[k]['citations'])
                    scopus_papers.pop(k)
                    collection.update_one({'_id': paper_id}, {'$set': {'Scopus_cites': citations}})
                    print(citations, matches, '---', len(scopus_papers))