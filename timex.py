import re
import string
import os
import sys
import pandas as pd
from datetime import *; from dateutil.relativedelta import *
import calendar

numbers = "(^a(?=\s)|one|two|three|four|five|six|seven|eight|nine|ten| \
          eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen| \
          eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty| \
          ninety|hundred|thousand)"
day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
week_day = "(monday|tuesday|wednesday|thursday|friday|saturday|sunday)"
months = "(january|february|march|april|may|june|july|august|september| \
          october|november|december)"
dmy = "(year|day|week|month)"
rel_day = "(today|yesterday|tomorrow|tonight|tonite)"
exp1 = "(before|after|earlier|later|ago)"
exp2 = "(this|next|last)"
iso = "\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+"
year = "((?<=\s)\d{4}|^\d{4})"
regxp1 = "((\d+|(" + numbers + "[-\s]?)+) " + dmy + "s? " + exp1 + ")"
regxp2 = "(" + exp2 + " (" + dmy + "|" + week_day + "|" + months + "))"

reg1 = re.compile(regxp1, re.IGNORECASE)
reg2 = re.compile(regxp2, re.IGNORECASE)
reg3 = re.compile(rel_day, re.IGNORECASE)
reg4 = re.compile(iso)
reg5 = re.compile(year)

hashmonths = {
    'january': 1,
    'february': 2,
    'march': 3,
    'april': 4,
    'may': 5,
    'june': 6,
    'july': 7,
    'august': 8,
    'september': 9,
    'october': 10,
    'november': 11,
    'december': 12}

def hashnum(number):
    if re.match(r'one|^a\b', number, re.IGNORECASE):
        return 1
    if re.match(r'two', number, re.IGNORECASE):
        return 2
    if re.match(r'three', number, re.IGNORECASE):
        return 3
    if re.match(r'four', number, re.IGNORECASE):
        return 4
    if re.match(r'five', number, re.IGNORECASE):
        return 5
    if re.match(r'six', number, re.IGNORECASE):
        return 6
    if re.match(r'seven', number, re.IGNORECASE):
        return 7
    if re.match(r'eight', number, re.IGNORECASE):
        return 8
    if re.match(r'nine', number, re.IGNORECASE):
        return 9
    if re.match(r'ten', number, re.IGNORECASE):
        return 10
    if re.match(r'eleven', number, re.IGNORECASE):
        return 11
    if re.match(r'twelve', number, re.IGNORECASE):
        return 12
    if re.match(r'thirteen', number, re.IGNORECASE):
        return 13
    if re.match(r'fourteen', number, re.IGNORECASE):
        return 14
    if re.match(r'fifteen', number, re.IGNORECASE):
        return 15
    if re.match(r'sixteen', number, re.IGNORECASE):
        return 16
    if re.match(r'seventeen', number, re.IGNORECASE):
        return 17
    if re.match(r'eighteen', number, re.IGNORECASE):
        return 18
    if re.match(r'nineteen', number, re.IGNORECASE):
        return 19
    if re.match(r'twenty', number, re.IGNORECASE):
        return 20
    if re.match(r'thirty', number, re.IGNORECASE):
        return 30
    if re.match(r'forty', number, re.IGNORECASE):
        return 40
    if re.match(r'fifty', number, re.IGNORECASE):
        return 50
    if re.match(r'sixty', number, re.IGNORECASE):
        return 60
    if re.match(r'seventy', number, re.IGNORECASE):
        return 70
    if re.match(r'eighty', number, re.IGNORECASE):
        return 80
    if re.match(r'ninety', number, re.IGNORECASE):
        return 90
    if re.match(r'hundred', number, re.IGNORECASE):
        return 100
    if re.match(r'thousand', number, re.IGNORECASE):
      return 1000

def tag(text):

    timex_found = []

    found = reg1.findall(text)
    #print(found)
    found = [a[0] for a in found if len(a) > 1]
    #print(found)
    for timex in found:
        timex_found.append(timex)

    found = reg2.findall(text)
    found = [a[0] for a in found if len(a) > 1]
    for timex in found:
        timex_found.append(timex)

    found = reg3.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg4.findall(text)
    for timex in found:
        timex_found.append(timex)

    found = reg5.findall(text)
    for timex in found:
        timex_found.append(timex)
    #print(timex_found)

    for timex in timex_found:
        text = re.sub(timex + '(?!</TIMEX2>)', '<TIMEX2>' + timex + '</TIMEX2>', text)
    #print(text)

    return text

def ground(tagged_text, base_date):

    timex_regex = re.compile(r'<TIMEX2>.*?</TIMEX2>', re.DOTALL)
    timex_found = timex_regex.findall(tagged_text)
    #print(timex)
    timex_found = map(lambda timex:re.sub(r'</?TIMEX2.*?>', '', timex),timex_found)
    #print(timex_found)

    for timex in timex_found:
        timex_val = 'UNKNOWN' 
        timex_val_ori='UNKNOWN'

        timex_ori = timex 
        #print(timex)
        if re.search(numbers, timex, re.IGNORECASE):
            split_timex = re.split(r'\s(?=days?|months?|years?|weeks?)', \
                                                              timex, re.IGNORECASE)
            value = split_timex[0]
            unit = split_timex[1]
            num_list = map(lambda s:hashnum(s),re.findall(numbers + '+', \
                                          value, re.IGNORECASE))
            timex = str(sum(num_list)) + ' ' + unit
            #print(timex)
        
        month = ""
        if re.match(r'\d+[/-]\d+[/-]\d+ \d+:\d+:\d+\.\d+', timex):
            dmy = re.split(r'\s', timex)[0]
            dmy = re.split(r'/|-', dmy)
            timex_val = str(dmy[2]) + '-' + str(dmy[1]) + '-' + str(dmy[0])
            timex_val_ori=timex_val
            #print(timex_val)

        elif re.match(r'\d{4}', timex):
            timex_val = str(timex)
            timex_val_ori=timex_val
            
        elif re.match(r'tonight|tonite|today', timex, re.IGNORECASE):
            timex_val = str(base_date)
            timex_val_ori=timex_val
 
        elif re.match(r'yesterday', timex, re.IGNORECASE):
            timex_val = str(base_date + relativedelta(days=-1))
            timex_val_ori=timex_val
   
        elif re.match(r'tomorrow', timex, re.IGNORECASE):
            timex_val = str(base_date + relativedelta(days=+1))
            timex_val_ori=timex_val

        elif re.match(r'last ' + week_day, timex, re.IGNORECASE):
            day=timex.split()[1]
            #print(day)
            if day=="monday":
                timex_val = str(base_date + relativedelta(weeks =-1,weekday=MO(0)))
            elif day=="tuesday":
                timex_val = str(base_date + relativedelta(weeks =-1,weekday=TU(0))) 
            elif day=="wednesday":
                timex_val = str(base_date + relativedelta(weeks =-1,weekday=WE(0)))
            elif day=="thursday":
                timex_val = str(base_date + relativedelta(weeks =-1,weekday=TH(0)))
            elif day=="friday":
                timex_val = str(base_date + relativedelta(weeks =-1,weekday=TU(0)))
            elif day=="saturday":
                timex_val = str(base_date + relativedelta(weeks =-1,weekday=SA(0)))
            elif day=="sunday":
                timex_val = str(base_date + relativedelta(weeks =-1,weekday=SU(0)))
            timex_val_ori=timex_val
       
        elif re.match(r'this ' + week_day, timex, re.IGNORECASE):
            day=timex.split()[1]
            if day=="monday":
                timex_val = str(base_date + relativedelta(weeks =0,weekday=MO(0)))
            elif day=="tuesday":
                timex_val = str(base_date + relativedelta(weeks =0,weekday=TU(0)))
            elif day=="wednesday":
                timex_val = str(base_date + relativedelta(weeks =0,weekday=WE(0)))
            elif day=="thursday":
                timex_val = str(base_date + relativedelta(weeks =0,weekday=TH(0)))
            elif day=="friday":
                timex_val = str(base_date + relativedelta(weeks =0,weekday=TU(0)))
            elif day=="saturday":
                timex_val = str(base_date + relativedelta(weeks =0,weekday=SA(0)))
            elif day=="sunday":
                timex_val = str(base_date + relativedelta(weeks =0,weekday=SU(0)))
            timex_val_ori=timex_val

        elif re.match(r'next ' + week_day, timex, re.IGNORECASE):
            day=timex.split()[1]
            if day=="monday":
                timex_val = str(base_date + relativedelta(weeks =+1,weekday=MO(0)))
            elif day=="tuesday":
                timex_val = str(base_date + relativedelta(weeks =+1,weekday=TU(0)))
            elif day=="wednesday":
                timex_val = str(base_date + relativedelta(weeks =+1,weekday=WE(0)))
            elif day=="thursday":
                timex_val = str(base_date + relativedelta(weeks =+1,weekday=TH(0)))
            elif day=="friday":
                timex_val = str(base_date + relativedelta(weeks =+1,weekday=TU(0)))
            elif day=="saturday":
                timex_val = str(base_date + relativedelta(weeks =+1,weekday=SA(0)))
            elif day=="sunday":
                timex_val = str(base_date + relativedelta(weeks =+1,weekday=SU(0)))
            timex_val_ori=timex_val

        elif re.match(r'last week', timex, re.IGNORECASE):
            year = (base_date + relativedelta(weeks=-1)).year
            week = (base_date + relativedelta(weeks=-1)).isocalendar()[1]
            timex_val = str(year) + 'W' + str(week)
            timex_val_ori=str(year)+'-'+str(week)
            
        elif re.match(r'this week', timex, re.IGNORECASE):
            year = (base_date + relativedelta(weeks=0)).year
            week = (base_date + relativedelta(weeks=0)).isocalendar()[1]
            timex_val = str(year) + 'W' + str(week)
            timex_val_ori=str(year)+'-'+str(week)
            
        elif re.match(r'next week', timex, re.IGNORECASE):
            year = (base_date + relativedelta(weeks=+1)).year
            week = (base_date + relativedelta(weeks=+1)).isocalendar()[1]
            timex_val = str(year) + 'W' + str(week)
            timex_val_ori=str(year)+'-'+str(week)
      
        elif re.match(r'last ' + months, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year - 1) + '-' + str(month)
            timex_val_ori=timex_val

        elif re.match(r'this ' + months, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year) + '-' + str(month)
            timex_val_ori=timex_val

        elif re.match(r'next ' + months, timex, re.IGNORECASE):
            month = hashmonths[timex.split()[1]]
            timex_val = str(base_date.year + 1) + '-' + str(month)
            timex_val_ori=timex_val
            
        elif re.match(r'last month', timex, re.IGNORECASE):
            if base_date.month == 1:
                timex_val = str(base_date.year - 1) + '-' + '12'
            else:
                timex_val = str(base_date.year) + '-' + str(base_date.month - 1)
            timex_val_ori=timex_val

        elif re.match(r'this month', timex, re.IGNORECASE):
                timex_val = str(base_date.year) + '-' + str(base_date.month)
                timex_val_ori=timex_val

        elif re.match(r'next month', timex, re.IGNORECASE):
            if base_date.month == 12:
                timex_val = str(base_date.year + 1) + '-' + '1'
            else:
                timex_val = str(base_date.year) + '-' + str(base_date.month + 1)
            timex_val_ori=timex_val

        elif re.match(r'last year', timex, re.IGNORECASE):
            timex_val = str(base_date.year - 1)
            timex_val_ori=timex_val

        elif re.match(r'this year', timex, re.IGNORECASE):
            timex_val = str(base_date.year)
            timex_val_ori=timex_val

        elif re.match(r'next year', timex, re.IGNORECASE):
            timex_val = str(base_date.year + 1)
            timex_val_ori=timex_val
            
        elif re.match(r'\d+ days? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date + relativedelta(days=-offset))
            timex_val_ori=timex_val
           
        elif re.match(r'\d+ days? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date + relativedelta(days=+offset))
            timex_val_ori=timex_val
            
        elif re.match(r'\d+ weeks? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            year = (base_date + relativedelta(weeks=-offset)).year
            week = (base_date + \
                            relativedelta(weeks=-offset)).isocalendar()[1]
            timex_val = str(year) + 'W' + str(week)
            timex_val_ori=str(year)+'-'+str(week)
            
        elif re.match(r'\d+ weeks? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            year = (base_date + relativedelta(weeks=+offset)).year
            week = (base_date + relativedelta(weeks=+offset)).isocalendar()[1]
            timex_val = str(year) + 'W' + str(week)
            timex_val_ori=str(year)+'-'+str(week)
            
        elif re.match(r'\d+ months? (ago|earlier|before)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])
            if (base_date.month - offset % 12) < 1:
                extra = 1
            year = str(base_date.year - offset // 12 - extra)
            month = str((base_date.month - offset % 12) % 12)

            if month == '0':
                month = '12'
            timex_val = year + '-' + month
            timex_val_ori=timex_val

        elif re.match(r'\d+ months? (later|after)', timex, re.IGNORECASE):
            extra = 0
            offset = int(re.split(r'\s', timex)[0])
            if (base_date.month + offset % 12) > 12:
                extra = 1
            year = str(base_date.year + offset // 12 + extra)
            month = str((base_date.month + offset % 12) % 12)
            if month == '0':
                month = '12'
            timex_val = year + '-' + month
            timex_val_ori=timex_val

        elif re.match(r'\d+ years? (ago|earlier|before)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date.year - offset)
            timex_val_ori=timex_val

        elif re.match(r'\d+ years? (later|after)', timex, re.IGNORECASE):
            offset = int(re.split(r'\s', timex)[0])
            timex_val = str(base_date.year + offset)
            timex_val_ori=timex_val

        timex_val = re.sub(r'\s.*', '', timex_val)
        timex_val_ori = re.sub(r'\s.*', '', timex_val_ori)
        #print(timex_val)

        tagged_text = re.sub('<TIMEX2>' + timex_ori + '</TIMEX2>', '<TIMEX2 val=\"' \
            + timex_val + '\">' + timex_ori + '</TIMEX2>', tagged_text)

    return tagged_text,timex_val_ori
