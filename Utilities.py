from datetime import datetime
import logging, random, copy, re, csv
import logging.config
from Features import Features

TRUE_POSITIVE = 0.0
FALSE_POSITIVE = 0.0
FALSE_NEGATIVE = 0.0
TRUE_NEGATIVE = 0.0

TIMEX_TAG = "</TIMEX2>"
TIMEX_TAG_REGEX = r'<TIMEX2 .+>.+?</TIMEX2>'

def days(d1, d2):
    d1 = datetime.strptime(d1, "%Y-%m-%d")
    d2 = datetime.strptime(d2, "%Y-%m-%d")
    return abs((d1 - d2).days)

def split(sentence, delimiter):
    return sentence.split(delimiter)

def isEmpty(string):
    return string == '' or string == None

def parseInputFileText(inputFileName):
    inputString = ""
    with open(inputFileName, 'r') as inputFile:
        for line in inputFile:
            inputString = "{}{}".format(inputString, line.strip())
    return inputString

def incrementTP():
    global TRUE_POSITIVE
    TRUE_POSITIVE += 1

def parseInputFile(inputFileName):
    featureObjects = []
    with open(inputFileName, 'r') as inputFile:
        csvFile = csv.reader(inputFile)
        for line in csvFile:
            feature = Features(line[0],line[1])
            #print(feature.actual)
            featureObjects.append(feature)
            
    return featureObjects

def setupLog():
    logging.basicConfig(level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s',
        filename='eventDetector.log',
        filemode='w')

def parseDate(line):
    if TIMEX_TAG in line:
        r = re.compile(TIMEX_TAG_REGEX)
        dates = r.findall(line)
        return re.sub("<\/?TIMEX2([^<.]+)?>", "", dates[0])

    return ""

def filter(taggedLines, searchString):
    events = []
    for taggedLine in taggedLines:
        if searchString in taggedLine.getSyntacticFeatures().getTemporalTag():
            events.append(taggedLine)

    return events

def firstMatching(pattern, string):
    expression = re.compile(pattern)
    results = expression.findall(string)
    return results[0] if len(results) > 0 else ""

def remove(pattern, string):
    return re.sub(pattern, "", string)

def isDateInFuture(event):
    date = firstMatching(r'val=.+>', event)
    date = remove(r"(>.+\/?TIMEX2>)|(val=)|'|\"", date)

    if len(date) == 4:
        return int(datetime.now().year) < int(date)
    elif len(date) == 10:
        return days(date, datetime.now().strftime("%Y-%m-%d")) > 0
    elif len(date) == 7 and 'W' in date:
        return datetime.now().isocalendar()[1] <= int(date[5:])
    else:
        return False

def writeLog(line):
    #print line
    logging.warn(line)

def computePrecision(obj):
    global TRUE_POSITIVE, FALSE_POSITIVE
    if obj.getActual() == "yes":
        TRUE_POSITIVE += 1
    else:
        FALSE_POSITIVE += 1

def computeRecall(featureObjects):
    global FALSE_NEGATIVE, TRUE_NEGATIVE
    for obj in featureObjects:
        if obj.getActual() == "no" and obj.getPredicted() == "yes":
            FALSE_NEGATIVE += 1
        elif obj.getActual() == "no" and obj.getPredicted() == "no":
            TRUE_NEGATIVE += 1

def writeOutput(outputFileName, row):
    with open(outputFileName, 'a') as outputFile:
        outputCSV = csv.writer(outputFile)
        outputCSV.writerow(row)

def printMetrics():
    print("TP: {}, FP : {}, FN: {}, TN: {}".format(TRUE_POSITIVE, FALSE_POSITIVE, FALSE_NEGATIVE, TRUE_NEGATIVE))
    print("Precision : {}".format(TRUE_POSITIVE/(TRUE_POSITIVE+FALSE_POSITIVE)))
    print("Recall : {}".format(TRUE_POSITIVE / (TRUE_POSITIVE + FALSE_NEGATIVE)))
    print("Accuracy : {}".format((TRUE_POSITIVE+TRUE_NEGATIVE)/(TRUE_POSITIVE+TRUE_NEGATIVE+FALSE_POSITIVE+FALSE_NEGATIVE)))
