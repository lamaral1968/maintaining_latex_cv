__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017-2018, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Production"


import pymongo
import pandas as pd
from my_settings import SECTION_NAMES
from my_mongo_db_login import DB_LOGIN_INFO, DATABASE_NAME


if __name__ == "__main__":
    connection = pymongo.MongoClient(DB_LOGIN_INFO['credentials'], DB_LOGIN_INFO['port'])
    db = connection[DATABASE_NAME]
    print('\nOpened connection')

    for filename in sorted(SECTION_NAMES.keys()):
        print('\n', filename.upper())

        # Get number of sheets and their names
        reader = pd.ExcelFile('./Data_files/' + filename + '.xlsx')
        n_sheets = len(reader.sheet_names)

        if n_sheets == 1:
            # Create collections from scratch every time
            collection = db[filename]
            collection.drop()

            collection = db[filename]
            sheet = reader.sheet_names[0]
            documents = []
            data = reader.parse(sheet)
            for i in range(len(data)):
                temp_dict = {}
                for j in list(data):
                    if data.iloc[i][j] == '-':
                        temp_dict[j] = False
                    else:
                        temp_dict[j] = str(data.iloc[i][j])
                documents.append(temp_dict)

            print(filename)
            collection.insert_many(documents)
        else:
            if filename != 'publications':
                # Create collections from scratch every time
                for sheet in reader.sheet_names:
                    collection_name = filename + '_' + sheet.lower()
                    collection = db[collection_name]
                    collection.drop()

                    collection = db[collection_name]
                    documents = []
                    data = reader.parse(sheet)
                    for i in range(len(data)):
                        temp_dict = {}
                        for j in list(data):
                            if data.iloc[i][j] == '-':
                                temp_dict[j] = False
                            else:
                                temp_dict[j] = str(data.iloc[i][j])
                        documents.append(temp_dict)
                    print(collection_name)
                    collection.insert_many(documents)
            else:
                # Add documents to collections but retain information for existing documents
                for sheet in reader.sheet_names:
                    collection_name = 'publications' + '_' + sheet.lower()
                    collection = db[collection_name]
                    print('\n\n', sheet.upper(), '--', collection_name)

                    paper_ids = []
                    for paper in collection.find():
                        paper_ids.append(paper['_id'])

                    data = reader.parse(sheet)
                    documents = []
                    for i in range(len(data)):
                        temp_dict = {}
                        for j in list(data):
                            if data.iloc[i][j] == '-':
                                temp_dict[j] = False
                            else:
                                temp_dict[j] = str(data.iloc[i][j])

                        # Create paper_code for paper in excel file
                        ex_title = temp_dict['Title'].lower()
                        ex_first_author = temp_dict['Authors'].split()[0].replace("\`",
                                                                                  '').replace("\'",
                                                                                              '').replace("\:",
                                                                                                          '').lower()
                        ex_paper_code = temp_dict['Year'] + ' ' + ex_first_author + ' ' + ex_title
                        temp_dict['paper_code'] = ex_paper_code
                        print(ex_paper_code)

                        update = True
                        for paper_id in paper_ids:
                            paper = collection.find_one({'_id': paper_id})
                            paper_code = paper['paper_code']
                            if ex_paper_code == paper_code:
                                update = False
                                break

                        if update:
                            documents.append(temp_dict)
                    if len(documents) > 0:
                        collection.insert_many(documents)

