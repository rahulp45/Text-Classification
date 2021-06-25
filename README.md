# **Description** #
Identify calender events with date,time and location(if present) from text.

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
        • Under the Heading Download see NER verion 4.2.0
    - Make sure to include the path of NER
- Mongodb installed

Input Data Format:
-------------------------
- A CSV file whose sentences labeled as 'yes' or 'no' after every sentence with patientID in th start
(see sampleInput.csv)

How to run:
---------------
python main.py inputfilename
