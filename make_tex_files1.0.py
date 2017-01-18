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


if __name__ == "__main__":
    pystache.defaults.DELIMITERS = ('\|', '|/')  # Change delimiters to avoid conflicts with TeX
    renderer = pystache.Renderer(search_dirs=['./Formatting_files'])

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
                    result = renderer.render_name(filename, data[key][i])
                    file_out.write(result)

                # Inelegant way to add space between subsections
                file_out.write('\\vspace*{0.2cm}')





