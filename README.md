# To start a new venv

python3 -m venv venv

# To activate venv

venv\Scripts\activate

# To install

python3 -m pip install -r requirements.txt

# To deactivate venv

deactivate

# To run file

0. Add file .env
1. Add the file into a folder and point the loader.py to it
2. Run `python3 loader.py "path/to/file"`
   e.g. `python3 loader.py "COMP9517/Course Outline.pdf"`
   or
   Run `python3 topic_extractor.py "path/to/file"`
   e.g. `python3 topic_extractor.py "COMP1511/Course Outline.pdf`
