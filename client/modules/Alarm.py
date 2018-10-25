

import sys
import datetime
import re

import os
import subprocess


from xml.dom import minidom

import xml.etree.ElementTree as ET
from threading import Thread, Lock



WORDS = ["ALARM","ADD","CLOCK"]


alarmFile="/home/debian/beamy/XML/alarm.xml"

addAlarmFile="/home/debian/beamy/XML/addAlarm.xml"

Small = {
    'zero': 0,
    'one': 1,
    'two': 2,
    'three': 3,
    'four': 4,
    'five': 5,
    'six': 6,
    'seven': 7,
    'eight': 8,
    'nine': 9,
    'ten': 10,
    'eleven': 11,
    'twelve': 12,
    'thirteen': 13,
    'fourteen': 14,
    'fifteen': 15,
    'sixteen': 16,
    'seventeen': 17,
    'eighteen': 18,
    'nineteen': 19,
    'twenty': 20,
    'thirty': 30,
    'forty': 40,
    'fifty': 50,
    'sixty': 60,
    'seventy': 70,
    'eighty': 80,
    'ninety': 90
}

Magnitude = {
    'thousand':     1000,
    'million':      1000000,
    'billion':      1000000000,
    'trillion':     1000000000000,
    'quadrillion':  1000000000000000,
    'quintillion':  1000000000000000000,
    'sextillion':   1000000000000000000000,
    'septillion':   1000000000000000000000000,
    'octillion':    1000000000000000000000000000,
    'nonillion':    1000000000000000000000000000000,
    'decillion':    1000000000000000000000000000000000,
}

class NumberException(Exception):
    def __init__(self, msg):
        Exception.__init__(self, msg)

def text2num(s):
    a = re.split(r"[\s-]+", s)
    n = 0
    g = 0
    for w in a:
        x = Small.get(w, None)
        if x is not None:
            g += x
        elif w == "hundred":
            g *= 100
        else:
            x = Magnitude.get(w, None)
            if x is not None:
                n += g * x
                g = 0
            else:
                raise NumberException("Unknown number: "+w)
    return n + g



def addAlarm(profile, mic):

	while True:
            try:
                mic.say("When would you like to add?")
                alarmData = mic.activeListen()
                number=[]
                alarmTimeMinute=0

                list=re.sub("[^\w]", " ",  alarmData).split()
			
                for ext in list:
                    x=changeNumber(ext)
                    if isinstance(x,int):
                        number.append(x)
                    
                print(number)            
                alarmTimeHour=number[0]
                print(alarmTimeHour)
                for x in number:
                    alarmTimeMinute=alarmTimeMinute+x
                alarmTimeMinute=alarmTimeMinute-alarmTimeHour
                print(alarmTimeMinute)
		
		hour=alarmTimeHour
		appendingTime="am"
		
                if "today" in alarmData.lower():
                    dayNumber=datetime.datetime.today().weekday()+1
			
                if "tomorrow" in alarmData.lower():
                    dayNumber=datetime.datetime.today().weekday()+2
                            
                if "monday" in alarmData.lower():
                    dayNumber=1
                        
                if "tuesday" in alarmData.lower():
                    dayNumber=2
                            
                if "wednesday" in alarmData.lower():
                    dayNumber=3
                        
                if "thursday" in alarmData.lower():
                    dayNumber=4
                        
                if "friday" in alarmData.lower():
                    dayNumber=5
                            
                if "saturday" in alarmData.lower():
                    dayNumber=6
                        
                if "sunday" in alarmData.lower():
                    dayNumber=0
                        
                if "pm" in alarmData.lower():
                    appendingTime="pm"
                    hour=alarmTimeHour+12
                
               
                    
                           
                
		
                alarmDateDay=changeDay(dayNumber)
                mic.say("Added alarm  on "  + str(alarmDateDay) + " at " + str(alarmTimeHour) + ":" + str(alarmTimeMinute) + " " + appendingTime)
                mic.say("Is this what you wanted?")
                userResponse = mic.activeListen()

                if bool(re.search('Yes', userResponse, re.IGNORECASE)):
                    mic.say("Okay, your alarm was setup")
                    readAlarmXML(dayNumber,hour,alarmTimeMinute)
                    return
	
			

            except KeyError:

                mic.say("Could not add alarm ; check if internet issue.")
                mic.say("Would you like to attempt again?")
                responseRedo = mic.activeListen()

                if bool(re.search('No', responseRedo, re.IGNORECASE)):
                    return
			    
def readAlarmXML(dayNumber,hour,alarmTimeMinute):
    
        tree = ET.parse(alarmFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('day'):  
            elem.text = str(dayNumber)
            
        for elem in root.iter('hour'):  
            elem.text = str(hour)
            
        for elem in root.iter('minute'):  
            elem.text = str(alarmTimeMinute)
        
        for elem in root.iter('ID'):
            newID=int(elem.text)+1
            elem.text=str(newID)

        tree.write(alarmFile)
        
        
        
        tree = ET.parse(addAlarmFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            elem.text = "1"

        tree.write(addAlarmFile)

def changeDay(text):
    
        if text == 0:
            return "sunday"
        else:
            if text == 1:
                return "monday"
            else:
                if text == 2:
                    return "tuesday"
                else:
                    if text == 3:
                        return "wednesday"
                    else:
                        if text == 4:
                            return "thursday"
                        else:
                            if text == 5:
                                return "friday"
                            else:
                                if text == 6:
                                    return "saturday"
                                


def changeNumber(list):

        if "one" in list.lower():
            return 1
			
        elif "two" in list.lower():
            return 2
			
        elif "three" in list.lower():
            return 3
			
        elif "four" in list.lower():
            return 4
			
        elif "five" in list.lower():
            return 5
			
        elif "six" in list.lower():
            return 6
			
        elif "seven" in list.lower():
            return 7
        
        elif "eight" in list.lower():
            return 8
        
        elif "nine" in list.lower():
            return 9
        
        elif "ten" in list.lower():
            return 10
        
        elif "eleven" in list.lower():
            return 11
        
        elif "twelve" in list.lower():
            return 12
        
        elif "thirteen" in list.lower():
            return 13
        
        elif "fourteen" in list.lower():
            return 14
        
        elif "fifteen" in list.lower():
            return 15
        
        elif "sixteen" in list.lower():
            return 16
        
        elif "seventeen" in list.lower():
            return 17
        
        elif "eighteen" in list.lower():
            return 19
        
        elif "twenty" in list.lower():
            return 20
        
        elif "thirty" in list.lower():
            return 30
        
        elif "forty" in list.lower():
            return 40
        
        elif "fifty" in list.lower():
            return 50
        
        elif "sixty" in list.lower():
            return 60
        
        else:
            return "not a number"


def handle(text, mic, profile):
		
	if bool(re.search('Alarm', text, re.IGNORECASE)):
		addAlarm(profile,mic)



def isValid(text):
	return any(word in text.upper() for word in WORDS)
