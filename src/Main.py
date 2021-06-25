import nltk, sys, re
from nltk.corpus import wordnet
from enchant.checker import SpellChecker
from autocorrect import Speller
import Timex,Utilities,Database
from LexicalFeatures import LexicalFeatures
from Event import Event
from nltk.tag import StanfordNERTagger
from Features import Features
from datetime import *

KEYWORDS = ['marriage', 'birthday', 'meeting', 'anniversary', 'seminar']
SYNONYMS_FOR_KEYWORDS = {}
PAST_TENSE_TAGS = ['VBD','VBN']
RESULT = []
TIMEX_TAG = "</TIMEX2>"
TIMEX_TAG_REGEX = r'<TIMEX2 .+>.+?</TIMEX2>'

def initialize():
    setupKeywords()
    customSynonym()
    Utilities.setupLog()
    
def customSynonym():
    SYNONYMS_FOR_KEYWORDS['seminar'].append('lecture')
    SYNONYMS_FOR_KEYWORDS['seminar'].append('class')
    SYNONYMS_FOR_KEYWORDS['meeting'].append('appointment')
    SYNONYMS_FOR_KEYWORDS['meeting'].append('visit')
    SYNONYMS_FOR_KEYWORDS['meeting'].append('call')

#perform spell correction
def performSpellCorrection(featureObj):
    checker = SpellChecker("en_US", featureObj.getText())
    spell = Speller(lang='en')
    for word in checker:
        word.replace(spell(word.word))
    featureObj.text=checker.get_text()
    featureObj.getLexicalFeatures().setSpellCorrection(checker.get_text())
    return featureObj

#get synonyms for given word
def getSynonyms(word):
    lemmas = []
    synsets = wordnet.synsets(word)
    for sense in synsets:
        lemmas += [re.sub("_", " ", lemma.name()) for lemma in sense.lemmas()]
    return list(set(lemmas))

def setupKeywords():
     # get all synonyms for given keywords
    global SYNONYMS_FOR_KEYWORDS
    for word in KEYWORDS:
        SYNONYMS_FOR_KEYWORDS[word] = getSynonyms(word)

def isRequiredEvent(obj, dict):
    for word in dict:
        for synonym in dict[word]:
            if synonym in obj.getText().lower():
                obj.getSemanticFeatures().setSynonym(str(dict[word]))
                return True, word
    return False, ""

def getCommandLineArgs():
    if len(sys.argv) < 2:
        print("ERROR: Usage: Main.py <input>")
        exit(1)
    return sys.argv[1]

def preProcessData(input):
    # read input file
    inputObjects = Utilities.parseInputFile(inputFileName)
    featureObjects = []
    for obj in inputObjects:
        featureObjects.append(performSpellCorrection(obj))
    return featureObjects

def performTagging(featureObjects):
    taggedLines = []
    for obj in featureObjects:
        taggedLine = ""
        try:
            taggedLine = Timex.tag(obj.getLexicalFeatures().getSpellCorrection().lower())
            date=datetime.today()
            taggedLine,timex_val = Timex.ground(taggedLine, date)
        except:
            taggedLine = ""

        if not Utilities.isEmpty(taggedLine):
            obj.getSyntacticFeatures().setTemporalTag(Utilities.firstMatching(TIMEX_TAG_REGEX, taggedLine))
            obj.setDate(timex_val)
            taggedLines.append(obj)
    return taggedLines

#check whether event is past
def isEventPast(obj):
    initialTokens = Utilities.split(obj.getText().lower(), " ")
    obj.getLexicalFeatures().setTokens(initialTokens)
    tokens = []

    for token in initialTokens:
        if not Utilities.isEmpty(token):
            tokens.append(token)

    taggedWords = nltk.pos_tag(tokens)
    obj.getSyntacticFeatures().setPOSTags(taggedWords)

    for (word, tag) in taggedWords:
        if tag in PAST_TENSE_TAGS:
            return True
    return False

#get location from stanford NER
def parseLocation(obj):
    event = re.sub("<TIMEX2>|</TIMEX2>", "", obj.getLexicalFeatures().getSpellCorrection())
    entities = []
    try:
        nerTagger = StanfordNERTagger( r"C:\Users\rahul\Desktop\stanford-ner-2020-11-17\classifiers\english.muc.7class.caseless.distsim.crf.ser.gz", r"C:\Users\rahul\Desktop\stanford-ner-2020-11-17\stanford-ner.jar")
        entities = nerTagger.tag(event.split())
    except:
        print("Unexpected error:", sys.exc_info()[0])

    result = ""
    for entity in entities:
        if entity[1] != 'O' and entity[1]!='DATE':
            result +=  " {}".format( entity[0] )
    obj.getSemanticFeatures().setLocation(result)
    return result

def setupEvent(obj, eventType):
    patientID=obj.getPatientID()
    eventDate = Utilities.parseDate(obj.getSyntacticFeatures().getTemporalTag())
    eventLocation = parseLocation(obj)
    if(eventLocation==""):
        eventLocation="none"
    return Event(patientID,eventType, eventDate, obj.getDate(), eventLocation)

if __name__ == '__main__':
    #initialize variables
    initialize()

    #read commmand line parameters
    inputFileName = getCommandLineArgs()

    #preprocess input data
    featureObjects = preProcessData(inputFileName)

    #perform temporal expression tagging
    taggedLines = performTagging(featureObjects)
    
    #select lines which have <TIMEX2> tag
    eventsList = Utilities.filter(taggedLines, TIMEX_TAG)
    
    #for lines identified as events, check each whether any word matches with synonyms for keywords
    for obj in eventsList:
        isRequired, eventType = isRequiredEvent(obj, SYNONYMS_FOR_KEYWORDS)
        
        if isRequired:
            eventObj = setupEvent(obj, eventType)
            obj.setEvent(eventObj)
            if not isEventPast(obj):
                Utilities.computePositives(obj)
                obj.setPredict("yes")
                RESULT.append([ obj.getEvent().patientID,
                                obj.getEvent().type,
                                obj.getEvent().rel_date,
                                obj.getEvent().abs_date,
                                obj.getEvent().location,
                                obj.getText()])
            else:
                if Utilities.isDateInFuture(obj.getSyntacticFeatures().getTemporalTag()):
                    obj.setPredict("yes")
                    Utilities.computePositives(obj)
                    RESULT.append([ obj.getEvent().patientID,
                                    obj.getEvent().type,
                                    obj.getEvent().rel_date,
                                    obj.getEvent().abs_date,
                                    obj.getEvent().location,
                                    obj.getText()])
                else:
                    Utilities.writeLog("Event Detected but is identified as past event :" + obj.getText())
        else:
            Utilities.writeLog("Event Detected but event type did not match with required events :" + obj.getText())
            
    #insert into database      
    Database.insert_into_database(RESULT)
    
    #count negatives
    Utilities.computeNegatives(featureObjects)

    #print evaluation metrics
    Utilities.printMetrics()
