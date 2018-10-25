# -*- coding: utf-8-*-
import re
import logging
import difflib
import mpd
from client.mic import Mic
import os


from xml.dom import minidom

import xml.etree.ElementTree as ET
from threading import Thread, Lock


# Standard module stuff
WORDS = ["VIDEO", "PLAY", "SHOW", "START" ]

commandFile="/home/debian/beamy/XML/command.xml"

commandVideoFile="/home/debian/beamy/XML/commandVideo.xml"

videoFile="/home/debian/beamy/media/video/"



def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, by telling a joke.

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    

 

    mic.say("Starting video mode")
    readCommandXML("TECHNOLOGY.mp4")

    return


def isValid(text):
    """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.upper() for word in WORDS)
               
               





      




        

def readCommandXML(videoName):
    
        tree = ET.parse(commandFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            elem.text = "play video"
        for elem in root.iter('name'):  
            elem.text = videoName 
 

        tree.write(commandFile)



