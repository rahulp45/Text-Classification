# **Description** #
Identify calender events with date,time and location(if present) from text.

 ## **NLP Modules** ##
* NLTK – WordNet, Spell correction, Named Entity Recognition, DateTime, Calender 

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
- Mongodb installed(Latest Version)
- pip install Flask 

Input Data Format:
-------------------------
- Import the attached .csv file on MongoDB with DB name "sampleInput" and collection name "Details"
- Format:
      • PatientID
      • Text
      • Actual class label("YES" or "NO")
 
Output Format:
-------------------------
- Output will be stored in the database named "Actions" with collection name "Events"

How to run:
---------------
python Main.py

Note: See projectDescription.txt for in depth exploring
