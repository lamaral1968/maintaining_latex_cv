# amaral-lab.org

The premise for this project is that LaTeX is a better system to create a large academic CV than Word.
Unfortunately, the choice of LaTeX means that the number of people able to help maintain the CV up-to-date
is not large. This is due to the fact that most, if not all, academic support staff lacks experience with
LaTeX.

I developed this Python package in order to be able to create the `*.tex` files need by LaTeX from information
maintained in Excel files and, thus, enable individuals lacking experience with LaTeX to help maintain a large
academic CV.

## Input files (needing maintenance)

This package requires the existence of 8 Excel files and one image file in the folder Data_files.
See examples provided.

Note the use of `-` for empty fields!

Please do not change variable names!

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


## Generating CV

In order to create your CV, you will need to:

1. Run `make_tex_files.py`

This will create a set of `*.tex` files that are stored in the folder `Tex_files`.

2. Compile `myCV.tex`

You will need to compile the file several times in order for the value of some variables (such as total
number of pages) to propagate.


## Modifying output

You can edit `myCV.tex` in order to ignore some of the sections, reorder sections, change paper format,
change font size, and so on.

You can edit `CV-Preamble.tex` (located in the folder `Data_files`) in order to change other aspects of the
CV such as font types and spacing between items.
