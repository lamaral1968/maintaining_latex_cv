# If your Excel file contains sheets with different names, please make changes here to match
#
PUBLICATION_TYPES = ['Editorial Material', 'Review Articles', 'Research Articles', 'Other Publications']

# Change values to True in case you want to update all values (for example, enough time has passed since last update)
#
FLAGS = {'update_scopus': False, 'update_gs': False, 'update_altmetrics': False, 'update_DOIs': False}

# key is name of Excel file, value is title of section in CV
#
SECTION_NAMES = {'appointments': 'Appointments',
                 'education': 'Education',
                 'affiliations': 'Professional Affiliations',
                 'honors': 'Honors and\\newline Awards',
                 'service': 'Professional Service',
                 'support': 'Research Support',
                 'mentoring': 'Mentoring',
                 'publications': 'Publications',
                 'presentations': 'Presentations',
                 'bio-info': None
                 }

#key is name of Excel file, value is list of modifiers of collection names in database
#
COLLECTION_NAMES = {'appointments': [None],
                    'education': [None],
                    'affiliations': [None],
                    'honors': [None],
                    'service': ['Northwestern University Service', 'External Service'],
                    'support': [None],
                    'mentoring': ['Graduate Students', 'Postdoctoral Fellows', 'Junior Faculty', 'Other Trainees'],
                    'publications': PUBLICATION_TYPES,
                    'presentations': ['Invited Presentations', 'Contributed Presentations'],
                    'bio-info': ['Variables', 'Title_block']
                    }

# URLs for different sites from where impact information is scraped.
# Most are straightforward. Not Scopus. To get URL for Scopus, go to website (https://www.scopus.com/),
# search for your publications, and copy URL of webpage with your publications
#
URLS = {'doi': 'https://www.crossref.org/guestquery/',
        'altmetrics': 'https://api.altmetric.com/v1/doi/',
        'google_scholar': 'https://scholar.google.com',
        'scopus': ('https://www.scopus.com/results/results.uri?cc=10&sort=plf-f&' +
                  'src=s&nlo=1&nlr=20&nls=afprfnm-t&sid=69d05dfbbfb7bd8575fbb5344425c24e&' +
                  'sot=anl&sdt=aut&sl=40&s=AU-ID%28%22Amaral%2c+Lu%c3%ads+A.Nunes%22+7103217924%29&' +
                  'ss=plf-f&ps=r-f&editSaveSearch=&origin=resultslist&zone=resultslist'),
        }


