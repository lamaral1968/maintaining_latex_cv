__author__ = "Amaral LAN"
__copyright__ = "Copyright 2017, Amaral LAN"
__credits__ = ["Amaral LAN"]
__license__ = "GPL"
__version__ = "1.0"
__maintainer__ = "Amaral LAN"
__email__ = "amaral@northwestern.edu"
__status__ = "Production"


import pandas as pd



def write_tex_file( filename, cv_author = 'Amaral LAN',
                    base_URL = 'https://amaral.northwestern.edu/publications' ):
    """
    Generates tex file with list of information for cv_author
    specified by filename

    inputs:
        filename -- str specifying type of information being processed
        cv_author -- str with name of cv author
        base_url -- srt with base url for abstracts of publications
    """

    names_to_sections = { 'appointments': 'Appointments',
                          'affiliations': 'Professional Affiliations',
                          'honors': 'Honors and\\newline Awards',
                          'service': 'Professional Service',
                          'support': 'Research Support',
                          'mentoring': 'Mentoring',
                          'publications': 'Publications',
                          'presentations': 'Presentations' }

    # Specify name of files and read data
    tex_file = './Tex_files/' + filename + '.tex'
    # Get sheet names
    reader = pd.ExcelFile('./Data_files/' + filename + '.xlsx')

    with open(tex_file, 'w', encoding='utf-8') as file_out:
        # Write Section title
        print(names_to_sections[filename] + '\n')
        file_out.write('\section' + '\n')
        file_out.write('{' + names_to_sections[filename] + '} \n')
        file_out.write('{' + names_to_sections[filename] + '} \n')
        file_out.write('{PDF:' + names_to_sections[filename][:10] + '} \n')
        file_out.write('\n')

        for sheet in reader.sheet_names:
            data = reader.parse(sheet)

            if len(reader.sheet_names) > 1:
                subsection = sheet.title()
                print(subsection)
                # Calculate number of trainees
                text = ''
                if filename == 'mentoring':
                    text = get_numbers(data, subsection)
                    print(text)
                file_out.write('\subsection' + '\n')
                file_out.write('{' + subsection + text + '} \n')
                file_out.write('{' + subsection + '} \n')
                file_out.write('{PDF:' + subsection[:12] + '} \n')
                file_out.write('\n')
                file_out.write('\GapNoBreak' + '\n')

            for i in range(len(data)-1, -1, -1):
                if filename == 'publications':
                    document = '\\NumberedItem{\\makebox[0.9cm][r]{' + '[{}]'.format(i + 1) + '}} \n'
                    document = document + for_publications(data.iloc[i], cv_author, base_URL)
                    file_out.write(document)

                else:
                    # Add period or date
                    if 'Year' in data.iloc[i].keys():
                            text = str( data.iloc[i]['Year'] )
                            width = 0.9
                            if 'Month' in data.iloc[i].keys():
                                width += 1.1
                                text = text + '--' + str( data.iloc[i]['Month'] )
                            file_out.write('\\NumberedItem{\\makebox[' + str(width) + 'cm][l]{' +
                                          '{}'.format(text) + '}} \n' )
                    else:
                        if str(data.iloc[i]['Year_end']) != '-':
                            file_out.write('\\NumberedItem{\\makebox[2.0cm][l]{' +
                                           '{}--{}'.format(data.iloc[i]['Year_begin'],
                                                           data.iloc[i]['Year_end']) +
                                           '}} \n')
                        else:
                            file_out.write('\\NumberedItem{\\makebox[2.0cm][l]{' +
                                           '{}'.format(data.iloc[i]['Year_begin'])
                                           + '}} \n')

                    # Different operations for different types of information
                    if 'Title' in data.iloc[i].keys():
                        if str(data.iloc[i]['Title']) != '-':
                            file_out.write('\\textit{' + data.iloc[i]['Title'] + '}   \n')

                            if 'Comment' in data.iloc[i].keys():
                                if str(data.iloc[i]['Comment']) != '-':
                                    file_out.write('[{}] \n'.format(data.iloc[i]['Comment']))

                            if 'Event' in data.iloc[i].keys():
                                if str(data.iloc[i]['Event']) != '-':
                                    file_out.write(' --- {} \n'.format(data.iloc[i]['Event']))

                            file_out.write('\\newline \n')

                    elif 'Trainee' in data.iloc[i].keys():
                        file_out.write('\\textit{' + '{}'.format(data.iloc[i]['Trainee']) + '}\n')
                        if str(data.iloc[i]['Status']) != '-':
                            file_out.write(' [{}] \n'.format(data.iloc[i]['Status']))

                        file_out.write('\\newline \n')

                        if str(data.iloc[i]['Current']) != '-':
                            file_out.write('\\textit{' + data.iloc[i]['Current'] + '}   \n')
                            file_out.write('\\newline \n')

                    elif 'Type' in data.iloc[i].keys():
                            if str(data.iloc[i]['Type']) != '-':
                                file_out.write('\\textit{' + '{}, '.format(data.iloc[i]['Type']) + '}\n')
                            if str(data.iloc[i]['Event']) != '-':
                                file_out.write('{} \n'.format(data.iloc[i]['Event']))
                            file_out.write('\\newline \n')


                    # Add unit and institution
                    if str(data.iloc[i]['Institution']) != '-':
                        if 'Unit' in data.iloc[i].keys():
                            if str(data.iloc[i]['Unit']) != '-':
                                file_out.write('{} \n'.format(data.iloc[i]['Unit']))
                                file_out.write('\\newline \n')

                        file_out.write('{} \n'.format(data.iloc[i]['Institution']))
                        file_out.write('\\newline ' + '\n')

                    if 'Location' in data.iloc[i].keys():
                        file_out.write('{} \n'.format(data.iloc[i]['Location']))
                        file_out.write('\\newline \n')

                    # Add honors for trainees
                    if 'Honors' in data.iloc[i].keys():
                        if str(data.iloc[i]['Honors']) != '-':
                            file_out.write('{' + '\\footnotesize Honors: {}'.format(data.iloc[i]['Honors']) +
                                           ' \n }')
                            file_out.write('\\newline \n')

                file_out.write('~ \n' + '\Gap' + '\n')
            file_out.write('~ \n' + '\Gap' + '\n')
            file_out.write('~ \n' + '\Gap' + '\n')
            file_out.write('~ \n' + '\Gap' + '\n')

    return True


def for_publications( pub, cv_author, base_URL ):
    """
    Generates string with text to be printed to tex file

    input:
        pub: dictionary with reference info

    output:
        document: str with line to be printed
    """
    # Write title
    document = '\\href{' + base_URL + '{}'.format(pub['URL'][14:]) + '}\n'
    document += '{``' + '{}'.format(pub['Title']) + '"}'

    try:
        document += '\t (Scopus citations: {})'.format( int(pub['Citations']) )
    except:
        pass

    document += '\n\\newline \n'

    # Write authors
    authors = pub['Authors'].split(',')
    line = ''
    for author in authors:
        if author.strip() != cv_author:
            line += author.strip() + ', '
        else:
            line += '\\textbf{' + author.strip() + '}' + ', '
    document += line [:-2] + '\n\\newline \n'

    # Write reference
    line = '\\textit{' + pub['Journal'] + '} '
    if pub['Volume'] != '-':
        line += '{}'.format(pub['Volume'])
    line += ': {} '.format(pub['Pages'])
    line += '({}).'.format(pub['Year'])
    if pub['Comment'] != '-':
        line += ' [{}]'.format(pub['Comment'])

    line += '\n\n'
    document += line
    document += '\Gap' + '\n'

    return document


def get_numbers(data, subsection):
    """
    Calculates numbers of students of each type and returns string to be add to cv

    inputs:
        data -- dataframe with student information
        subsection -- name of sheet from Excel file

    outputs:
        text -- string
    """
    current = 0
    for i in range(len(data)):
        if data.iloc[i]['Year_end'] == 'present':
            current += 1

    text = ' [{} current, {} past'.format( current, len(data)-current )

    if subsection == "Graduate Students":
        ms = 0
        phd = 0
        for i in range(len(data)):
            if 'M.S' in data.iloc[i]['Trainee']:
                ms += 1
            elif 'Ph.D.' in data.iloc[i]['Trainee']:
                phd += 1
        text += ', of which {} Ph.D. and {} M.Sc.'.format(phd, ms)

    elif subsection == 'Other Trainees':
        hs = 0
        ugs = 0
        gs = 0
        for i in range(len(data)):
            if 'Undergrad' in data.iloc[i]['Status']:
                ugs += 1
            elif 'Graduate' in data.iloc[i]['Status']:
                gs += 1
            else:
                hs += 1
        text += ', of which {} graduate, {} undergraduate, and {} high-school students'.format(gs, ugs, hs)

    text += ']'

    return text


def write_intro_tex_file():
    """
    Creates the tex file with all demographic information

    input:
        None
    output:
        None
    """
    reader = pd.ExcelFile('./Data_files/bio-info.xlsx')

    # Create file with variable definitions
    with open('./Tex_files/variables.tex', 'w', encoding='utf-8') as file_out:
        for sheet in reader.sheet_names:
            data = reader.parse(sheet)

            for i in range(len(data)):
                if data.iloc[i]['Key'] != 'CVColor':
                    file_out.write('\\newcommand{\\' + data.iloc[i]['Key'] + '}{' +
                                   data.iloc[i]['Value'] + '} \n')
                else:
                    index = i

        file_out.write('\n% PDF settings and properties. \n' +
                       '\hypersetup{pdftitle={\CVTitle}, pdfauthor={\CVAuthor}, pdfsubject={\CVWebpage}, ' +
                       'pdfcreator={XeLaTeX}, pdfproducer={}, pdfkeywords={}, pdfpagemode={}, ' +
                       'bookmarks=true, unicode=true, bookmarksopen=true, pdfstartview=FitH, ' +
                       'pdfpagelayout=OneColumn, pdfpagemode=UseOutlines, hidelinks, breaklinks} \n')

    # Create file with title block information
    with open('./Tex_files/title_block.tex', 'w', encoding='utf-8') as file_out:
        file_out.write('\\addname{\\CVAuthor} \n\n')
        file_out.write('\definecolor{CVColor}{RGB}{' + data.iloc[index]['Value'] + '}\n\n')
        file_out.write('\hspace*{0.1cm} \colorrule{CVColor}{1.8pt}{\\textwidth} \n\n')
        file_out.write('\\addphoto{\CVPhoto} \n\n')
        file_out.write('\\vspace*{-4.0cm} \n\\begin{minipage}{0.79\\textwidth} \n')
        file_out.write('\\footnotesize \n')
        file_out.write('\par\hspace*{0.23cm}\CVDepartment \\hfill \CVTelephone \n')
        file_out.write('\par\hspace*{0.23cm}\CVUniversity \\hfill \CVTwitter ~(Twitter)\n')
        file_out.write('\par\hspace*{0.23cm}\CVAddressOne \\hfill \CVSkype  ~(Skype)\n')
        file_out.write('\par\hspace*{0.23cm}\CVAddressTwo \\hfill \href{mailto: \CVEmail}\CVEmail \n')
        file_out.write('\par\hspace*{0.23cm}\CVAddressThree \\hfill \href{\CVOrcid}\CVOrcid  \n')
        file_out.write('\par\hspace*{0.23cm}\CVAddressFour \\hfill \href{\CVPublons}\CVPublons \n')
        file_out.write('\par\hspace*{0.23cm} \\hfill \href{\CVGoogleScholar}{\CVGoogleScholar} \n')
        file_out.write('\par\hspace*{0.23cm} \\hfill \href{\CVWebpage}\CVWebpage  \n')
        file_out.write('\end{minipage} \n\n')


if __name__ == "__main__":
    write_intro_tex_file()

    for filename in ['appointments', 'honors', 'service', 'support', 'mentoring',
                     'publications', 'presentations']:
        out = write_tex_file(filename)


