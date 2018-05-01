__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017-2018, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.1"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Production"


import requests
import pymongo
import json
from my_settings import PUBLICATION_TYPES, FLAGS, URLS
from my_mongo_db_login import DB_LOGIN_INFO, DATABASE_NAME


if __name__ == "__main__":
    connection = pymongo.MongoClient(DB_LOGIN_INFO['credentials'], DB_LOGIN_INFO['port'])
    db = connection[DATABASE_NAME]
    print('\nOpened connection')

    url_altmetrics = URLS['altmetrics']
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
            if FLAGS['update_altmetrics']:
                update = True
            else:
                paper = collection.find_one({'_id': paper_id})
                if 'Alt_score' not in paper.keys():
                    update = True
                elif not paper['Alt_Score']:
                    update = True

            if update:
                title = paper['Title'].lower()
                first_author = paper['Authors'].split()[0].replace("\`",
                                                                   '').replace("\'",
                                                                               '').replace("\:",
                                                                                           '').lower()
                paper_code = paper['Year'] + ' ' + first_author + ' ' + title
                print(paper_code)

                if 'doi' in paper.keys():
                    doi = paper['doi'].split('.org/')
                    url = url_altmetrics + doi[1]
                    print(url)
                    res = requests.get(url)

                    flag = False
                    if res.status_code == 200:
                        try:
                            alt_x = json.loads(res.content.decode('utf-8'))
                            percentile = alt_x['context']['similar_age_3m']['pct']
                            score = alt_x['score']
                            flag = True
                        except:
                            pass

                    if flag:
                        collection.update_one({'_id': paper_id},
                                              {'$set': {'Alt_score': '{:.1f} (above {:.0f}\\%)'.format(score,
                                                                                                       percentile)}})
                    else:
                        collection.update_one({'_id': paper_id},
                                              {'$set': {'Alt_score': False}})
