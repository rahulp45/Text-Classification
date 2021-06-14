# **Description** #
Identify future calendar events with date and time from text. Five events – Marriage, Birthday Party, Meeting Anniversary, Seminar will be included in scope.

 ## **NLP Modules** ##
* NLTK – WordNet, Spell correction, Timex, Named Entity Recognition, DateTime, Calender

Pre-requisites:
-------------------
- Install nltk, pyenchant and autocorrect.
    - pip install nltk
    - pip install pyenchant
    - pip install autocorrect
- Stanford NER
    - Download jar files from http://nlp.stanford.edu/software/stanford-ner-2014-06-16.zip
    - Make sure to include the path of NER in parseLocation function in Main.py

Input Data Format:
-------------------------
- A file whose sentences labeled as "yes" or "no" after ','

How to run:
---------------
python main.py inputfilename outputfilename
