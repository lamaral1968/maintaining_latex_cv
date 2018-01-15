__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Production"


import pandas as pd
import json
from my_settings import NAMES_TO_SECTIONS

if __name__ == "__main__":

    full_dictionary = {'bio-info': None}
    full_dictionary.update(NAMES_TO_SECTIONS)
    print(full_dictionary)

    for filename in full_dictionary.keys():
        print(filename + '\n')

        # Get sheet names
        reader = pd.ExcelFile('./Data_files/' + filename + '.xlsx')

        data_dict = {'Order': reader.sheet_names}

        for sheet in reader.sheet_names:
            data_dict[sheet] = []
            data = reader.parse(sheet)
            for i in range(len(data)):
                temp_dict = {}
                for j in list(data):
                    if data.iloc[i][j] == '-':
                        temp_dict[j] = False
                    else:
                        temp_dict[j] = str(data.iloc[i][j])

                data_dict[sheet].append(temp_dict)

         # TODO (MAYBE) sort data loaded from Excel file

        file_json = './Json_files/' + filename + '.json'
        with open(file_json, 'w', encoding='utf-8') as file_out:
            json.dump(data_dict, file_out, sort_keys = True, indent = 4)

