import json
import pandas as pd
from sys import exit
from copy import copy

#with open('./Json_files/publications_updated.json', 'r', encoding = 'utf-8') as file_in:
with open('./Json_files/publications.json', 'r', encoding='utf-8') as file_in:
    data = json.load(file_in)

article_types = ['Editorial Material', 'Review Articles', 'Research Articles', 'Other Publications']
print(article_types)

# Correct publications.xlsx file
writer = pd.ExcelWriter('./Data_files/publications_new.xlsx')
for key in article_types:
    df = pd.DataFrame(data[key])
    df.to_excel(writer, sheet_name = key)

writer.save()


# # Get dictionaries in order
# counter = 0
# citations = {}
# for key in article_types:
#     citations[key] = []
#     for i in range(len(data[key])):
#         paper_id = 'id_' + str(counter)
#
#         content = {'Sc_cites' : copy(data[key][i]['Sc_cites']),
#                    'Alt_score': '-', 'Paper_id': paper_id, 'Update_date': None}
#
#         del data[key][i]['Sc_cites']
#         del data[key][i]['WoS_cites']
#         del data[key][i]['GS_cites']
#         try:
#             del data[key][i]['Update_date']
#         except:
#             pass
#         data[key][i]['Paper_id'] = paper_id
#
#         for key2 in data[key][i].keys():
#             if not data[key][i][key2]:
#                 data[key][i][key2] = '-'
#
#         citations[key].append(copy(content))
#
#         counter += 1
#
# with open('./Json_files/publications.json', 'w', encoding = 'utf-8') as file_out:
#     json.dump(data, file_out, sort_keys = True, indent = 4)
#
# with open('./Json_files/impact.json', 'w', encoding = 'utf-8') as file_out:
#     json.dump(citations, file_out, sort_keys = True, indent = 4)
#

