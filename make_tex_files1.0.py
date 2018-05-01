__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017-2018, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Development"

import pystache
import pymongo
from copy import copy
from my_settings import SECTION_NAMES, COLLECTION_NAMES
from my_mongo_db_login import DB_LOGIN_INFO, DATABASE_NAME


if __name__ == "__main__":
    pystache.defaults.DELIMITERS = ('\|', '|/')  # Change delimiters to avoid conflicts with TeX
    renderer = pystache.Renderer(search_dirs=['./Formatting_files'])

    connection = pymongo.MongoClient(DB_LOGIN_INFO['credentials'], DB_LOGIN_INFO['port'])
    db = connection[DATABASE_NAME]
    print('\nOpened connection')

    # Create tex files for title block
    #
    collection = db['bio-info']
    data = collection.find_one()
    for filename in ['variables', 'title_block']:
        tex_file = './Tex_files/' + filename + '.tex'
        print('\n' + filename + '\n' + tex_file )

        with open(tex_file, 'w', encoding='utf-8') as file_out:
            result = renderer.render_name(filename, data)
            file_out.write(result)

    # Create tex files for all other sections of CV
    #
    section_list = copy( list(SECTION_NAMES.keys()) )
    section_list.remove('bio-info')
    for filename in section_list:
        tex_file = './Tex_files/' + filename + '.tex'
        print('\n' + filename + '\n' + tex_file )

        with open(tex_file, 'w', encoding='utf-8') as file_out:
            # Create section header
            if SECTION_NAMES[filename] is not None:
                result = renderer.render_name('section', {'NAME': SECTION_NAMES[filename],
                                                          'Clean_NAME': list(SECTION_NAMES[filename].split())[0]}
                                          )
                file_out.write(result)

            for name in COLLECTION_NAMES[filename]:
                if name is None:
                    name = filename
                else:
                    print(name)
                    result = renderer.render_name('subsection', {'NAME': name, 'Clean_NAME': name.replace(' ', '_')})
                    file_out.write(result)
                    name = filename + '_' + name.lower()

                data = []
                for document in db[name].find():
                    data.append(document)

                for i in range(len(data)-1, -1, -1):
                    if filename == 'publications':
                        data[i]['Authors'] = data[i]['Authors'].replace('Amaral LAN', '{\\textbf{Amaral LAN}}')

                        try:
                            logic_citations = bool(data[i]['GS_cites']) or \
                                              bool(data[i]['Scopus_cites']) or \
                                              bool(data[i]['WoS_cites'])
                            logic_altmetrics = bool(data[i]['Alt_score'])
                        except:
                            logic_citations = False
                            logic_altmetrics = False

                        data[i].update({'Citations': logic_citations, 'Altmetrics': logic_altmetrics})
                    else:
                        result = renderer.render_name(filename, data[i])
                        file_out.write(result)

                # Sort publications by year of publication and then by title
                #
                if filename == 'publications':
                    data.sort(key = lambda k: (k['Year'], k['Title']))
                    for i in range(len(data)-1, -1, -1):
                        data[i].update({'Number': str(i + 1)})
                        if 'Alt_score' in data[i].keys():
                            temp_string = data[i]['Alt_score']
                            if temp_string != False:
                                data[i]['Alt_score'] = temp_string.replace('%', '\\%')
                        # print(data[i]['Citations'], data[i]['Altmetrics'], temp_string)
                        result = renderer.render_name(filename, data[i])
                        file_out.write(result)

                # Inelegant, but effective, way to add space between subsections
                #
                file_out.write('\\vspace*{0.2cm}')





