import nltk, sys, re
from nltk.corpus import wordnet
from enchant.checker import SpellChecker
from autocorrect import Speller
import timex,Utilities
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
    

def performSpellCorrection(featureObj):
    checker = SpellChecker("en_US", featureObj.getText())
    spell = Speller(lang='en')
    for word in checker:
        word.replace(spell(word.word))
    featureObj.text=checker.get_text()
    featureObj.getLexicalFeatures().setSpellCorrection(checker.get_text())
   
    return featureObj

def getSynonyms(word):
    lemmas = []
    synsets = wordnet.synsets(word)
    for sense in synsets:
        lemmas += [re.sub("_", " ", lemma.name()) for lemma in sense.lemmas()]
    return list(set(lemmas))

def setupKeywords():
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
        print("ERROR: Usage: Main.py <input> <output>")
        exit(1)

    return sys.argv[1], sys.argv[2]

def preProcessData(input):
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
            taggedLine = timex.tag(obj.getLexicalFeatures().getSpellCorrection().lower())
            date=datetime.today()
            taggedLine,timex_val = timex.ground(taggedLine, date)
        except:
            taggedLine = ""

        if not Utilities.isEmpty(taggedLine):
            obj.getSyntacticFeatures().setTemporalTag(Utilities.firstMatching(TIMEX_TAG_REGEX, taggedLine))
            obj.setDate(timex_val)
            taggedLines.append(obj)

    return taggedLines


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

def parseLocation(obj):
    event = re.sub("<TIMEX2>|</TIMEX2>", "", obj.getLexicalFeatures().getSpellCorrection())
    entities = []
    try:
        nerTagger = StanfordNERTagger( r"C:\Users\rahul\Desktop\stanford-ner-2020-11-17\classifiers\english.muc.7class.distsim.crf.ser.gz", r"C:\Users\rahul\Desktop\stanford-ner-2020-11-17\stanford-ner.jar")
        entities = nerTagger.tag(event.split())
    except:
        print("Unexpected error:", sys.exc_info()[0])

    result = ""
    for entity in entities:
        if entity[1] != 'O':
            result +=  " {}".format( entity[0] )
    
    obj.getSemanticFeatures().setLocation(result)
    return result

def setupEvent(obj, eventType):
    eventDate = Utilities.parseDate(obj.getSyntacticFeatures().getTemporalTag())
    eventLocation = parseLocation(obj)
    if(eventLocation==""):
        eventLocation="none"
    return Event(eventType, eventDate, obj.getDate(), eventLocation)

if __name__ == '__main__':
    initialize()

    inputFileName, outputFileName = getCommandLineArgs()

    featureObjects = preProcessData(inputFileName)

    taggedLines = performTagging(featureObjects)

    eventsList = Utilities.filter(taggedLines, TIMEX_TAG)

    for obj in eventsList:
        isRequired, eventType = isRequiredEvent(obj, SYNONYMS_FOR_KEYWORDS)
        
        if isRequired:
            eventObj = setupEvent(obj, eventType)
            obj.setEvent(eventObj)
            if not isEventPast(obj):
                Utilities.computePositives(obj)
                obj.setPredict("yes")
                RESULT.append(["Event:"+obj.getEvent().type,
                                "When:"+ obj.getEvent().rel_date,
                                "Date:"+obj.getEvent().abs_date,
                                "Location:"+ obj.getEvent().location,
                                 "Text:"+ obj.getText()])
            else:
                if Utilities.isDateInFuture(obj.getSyntacticFeatures().getTemporalTag()):
                    obj.setPredict("yes")
                    Utilities.computePositives(obj)
                    RESULT.append(["Event:"+ obj.getEvent().type,
                                     "When:"+ obj.getEvent().rel_date,
                                     "Date:"+ obj.getEvent().abs_date,
                                     "Location:"+ obj.getEvent().location,
                                     "Text:"+ obj.getText()])
                else:
                    Utilities.writeLog("Event Detected but is identified as past event :" + obj.getText())
        else:
            Utilities.writeLog("Event Detected but event type did not match with required events :" + obj.getText())

    for feature in RESULT:
        Utilities.writeOutput(outputFileName, feature)
    Utilities.writeOutput(outputFileName,"\n")

    Utilities.computeNegatives(featureObjects)

    Utilities.printMetrics()
