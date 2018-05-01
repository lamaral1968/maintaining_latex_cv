# Luis Amaral (amaral-lab.org)

The premise for this project is that LaTeX is a better system to create a large academic CV than Word.
Unfortunately, the choice of LaTeX means that the number of people able to help maintain the CV up-to-date
is not large. This is due to the fact that most, if not all, academic support staff lacks experience with
LaTeX.

I developed this Python package in order to be able to create the `*.tex` files need by LaTeX from information
maintained in Excel files and, thus, enable individuals lacking experience with LaTeX to help maintain a large
academic CV.

## Data being maintained

This package requires the existence of 8 Excel files and one image file in the folder Data_files.
See examples provided.

Note the use of `-` for empty fields!

**Do not change variable names unless you know what you are doing!**

### appointments.xlsx

This file contains a list of appointments in chronological order (oldest to newest).


### bio-info.xlsx

This file contains a values of relevant variables used in the creation of the CV. Provide three integers
between 0 and 255 (RGB) for determining the color of the horizontal bar and of the font for section and
subsection names.


### honors.xlsx

This file contains a list of honors and awards in chronological order (oldest to newest).


### mentoring.xlsx

This file contains several lists of trainees in chronological order (oldest to newest). You can change the
names of the worksheets and those changes will be reflected in the CV.

### presentations.xlsx

This file contains several lists of presentations in chronological order (oldest to newest). You can change
the number of worksheets and the names of the worksheets and those changes will be reflected in the CV.

### publications.xlsx

This file contains several lists of publications in chronological order (oldest to newest). You can change the
number of worksheets and the names of the worksheets and those changes will be reflected in the CV.

### service.xlsx

This file contains several lists of instances of professional service in chronological order (oldest to
newest). You can change the number of worksheets and the names of the worksheets and those changes will
be reflected in the CV.

### support.xlsx

This file contains a list of grants in chronological order (oldest to newest).


## Formatting of output

I use `*.mustache` files to separate logic from output. The logic part is confined to Python code,
while LaTeX output is declared in the `*.mustache` files stored in the folder `Formatting_files`.  If you
want to change the format of the CV, and know LaTeX, you can edit the `*.mustache` files.

You must edit `CV-Preamble.tex` (located in the folder `Formatting_files`) in order to change other aspects of the
CV such as font types and spacing between items.

You must edit `myCV.tex` (located in the main directory) in order to ignore some of the sections, reorder sections,
change page format, and so on.


## Generating CV

In order to create your CV, you will need to:

1. Create Excel files

2. Update `my_mongo_db_login.py`

3. Run `create_mongo_db.py`

4. Run `scrape_doi.py`

5. Run `scrape_altmetrics.py`

6. Run `scrape_scopus_citations.py`

7. Run `scrape_google_scholar_citations.py`

8. Run `make_tex_files.py`

This will create a set of `*.tex` files that are stored in the folder `Tex_files`.

9. Compile `myCV.tex`

You will need to compile the file a couple of times in order for the value of some variables (such as total
number of pages) to propagate.
