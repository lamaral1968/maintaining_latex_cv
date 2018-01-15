__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Development"

import pystache
import json
from my_settings import NAMES_TO_SECTIONS


def match_ids(key, i, data, impact):
    """
    Match paper_id from publications and impact Json files

    :param key: str
    :param i: int
    :param data: dict
    :param impact: dict

    :return: index: int
    """
    #
    index = False  # This initialization is here to avoid a program crash when trying
                   # to match papers to impact.json file
    paper_id = data[key][i]['Paper_id']
    for j in range(len(impact[key])):
        if impact[key][j]['Paper_id'] == paper_id:
            index = j
            break

    return index


if __name__ == "__main__":
    pystache.defaults.DELIMITERS = ('\|', '|/')  # Change delimiters to avoid conflicts with TeX
    renderer = pystache.Renderer(search_dirs=['./Formatting_files'])

    # Load citations
    json_file = './Json_files/impact.json'
    with open(json_file, 'r', encoding='utf-8') as file_in:
        impact = json.load(file_in)

    # Create contact and title block
    json_file = './Json_files/bio-info.json'
    with open(json_file, 'r', encoding='utf-8') as file_in:
        data = json.load(file_in)

    print(data['Sheet1'][0])

    for filename in ['variables', 'title_block']:
        tex_file = './Tex_files/' + filename + '.tex'
        print('\n' + filename + '\n' + tex_file )

        with open(tex_file, 'w', encoding='utf-8') as file_out:
            result = renderer.render_name(filename, data['Sheet1'][0])
            file_out.write(result)

    # Create tex files for all other sections of CV
    for filename in NAMES_TO_SECTIONS.keys():
        tex_file = './Tex_files/' + filename + '.tex'
        print('\n' + filename + '\n' + tex_file )

        with open(tex_file, 'w', encoding='utf-8') as file_out:
            # Create section header
            result = renderer.render_name('section',
                                          {'NAME': NAMES_TO_SECTIONS[filename],
                                           'Clean_NAME': list(NAMES_TO_SECTIONS[filename].split())[0]}
                                          )
            file_out.write(result)

            json_file = './Json_files/' + filename + '.json'
            with open(json_file, 'r', encoding = 'utf-8') as file_in:
                data = json.load(file_in)

            order_of_subsections = data['Order']
            print(order_of_subsections)
            for key in order_of_subsections:
                if key != 'Sheet1':
                    # Create subsection header in case there are multiple worksheets
                    print(key)
                    result = renderer.render_name('subsection',
                                                  {'NAME': key,
                                                   'Clean_NAME': key.replace(' ', '_')}
                                                  )
                    file_out.write(result)

                for i in range(len(data[key])-1, -1, -1):
                    data[key][i].update({'Number': str(i+1)})
                    if filename == 'publications':
                        index = match_ids(key, i, data, impact)
                        #print(key, index, impact[key][index])
                        data[key][i]['Authors'] = data[key][i]['Authors'].replace('Amaral LAN',
                                                                                  '{\\textbf{Amaral LAN}}')

                        try:
                            logic_citations = bool(impact[key][index]['GS_cites']) or \
                                              bool(impact[key][index]['Sc_cites']) or \
                                              bool(impact[key][index]['WoS_cites'])

                            data[key][i].update({'GS_cites': impact[key][index]['GS_cites'],
                                                 'WoS_cites': impact[key][index]['WoS_cites'],
                                                 'Sc_cites': impact[key][index]['Sc_cites']})
                        except:
                            logic_citations = False
                        data[key][i].update({'Citations': logic_citations})

                    result = renderer.render_name(filename, data[key][i])
                    file_out.write(result)

                # Inelegant, but effective, way to add space between subsections
                file_out.write('\\vspace*{0.2cm}')





