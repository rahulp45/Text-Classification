# **Description** #
Identify events with date and time from text. Five events – Marriage, Birthday Party, Meeting Anniversary, Seminar will be included in scope.

 ## **NLP Modules** ##
* NLTK – WordNet, Spell correction, Timex, Named Entity Recognition, DateTime, Calender

Pre-requisites:
-------------------
- Install nltk, pyenchant and autocorrect.
    - pip install nltk
    - pip install pyenchant
    - pip install autocorrect
- Stanford NER
    - Download zip file for NER from https://nlp.stanford.edu/software/CRF-NER.html
    - Make sure to include the path of NER in parseLocation function in Main.py

Input Data Format:
-------------------------
- A file whose sentences labeled as "yes" or "no" after ','
(see sampleInput.csv)

How to run:
---------------
python main.py inputfilename outputfilename
