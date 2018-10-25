# -*- coding: utf-8-*-
import re
import logging
import difflib
import mpd
from client.mic import Mic
import os
from client import tts
from client import stt
from jasper import Jasper

from xml.dom import minidom

import xml.etree.ElementTree as ET
from threading import Thread, Lock


# Standard module stuff
WORDS = ["MUSIC" ]

commandFile="/home/debian/beamy/XML/command.xml"

commandMusicFile="/home/debian/beamy/XML/commandMusic.xml"

musicFile="/home/debian/beamy/media/music/"



def handle(text, mic, profile):
    """
    Responds to user-input, typically speech text, by telling a joke.

    Arguments:
        text -- user-input, typically transcribed speech
        mic -- used to interact with the user (for both input and output)
        profile -- contains information related to the user (e.g., phone
                   number)
    """
    

 

    mic.say("Starting music mode")
    handleForever(mic)
    mic.say("Exiting music mode")

    return


def isValid(text):
    """
        Returns True if the input is related to jokes/humor.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return any(word in text.upper() for word in WORDS)
               
               
def loadMusicNames(musicFile):
        
        musicNames=[]
        musicExtention=[]
        for music in os.listdir(musicFile):
            sep = '.'
            rest = music.split(sep, 1)[0]
            extention=music.split(sep, 1)[1]
            musicNames.append(rest)
            musicExtention.append(extention)
            print(rest)
            print(extention)
        return musicNames, musicExtention
    
    
def delegateInput(mic,input):

        command = input.upper()


        if "CONTINUE" in command:
            mic.say("Continue music")
            readCommandMusicXML("continue")
            return
        elif "PAUSE" in command:
            mic.say("Pausing music")
            readCommandMusicXML("pause")
            return
        elif any(ext in command for ext in ["LOUDER", "HIGHER"]):
            mic.say("Louder")
            readCommandMusicXML("volume up")
            return
        elif any(ext in command for ext in ["SOFTER", "LOWER"]):
            mic.say("Softer")
            readCommanMusicXML("volume down")
            return
        else:
            mic.say("Can you repeat")
            return

 

def handleForever(mic):
    
        
        musicNames,musicExtention=loadMusicNames(musicFile)
        mic.say("What music do you want to play")

        

        
        while True:    
            musicName = mic.activeListen()
            print(musicName)
            
            if any(s in musicName for s in musicNames):
                for i in [i for i,x in enumerate(musicNames) if (x == musicName)]:
                    completeName=musicName+"."+musicExtention[i]
                    print(completeName)
                    readCommandXML(completeName)
                    mic.say("Starting %s music" % musicName)
                
                while True :
                    command = mic.activeListen()
                    if any(ext in command for ext in ["quit", "stop"]):
                        mic.say("Closing music")
                        readCommandMusicXML("quit")
                        return
                    else:
                        delegateInput(mic,command)


            elif any(ext in musicName for ext in ["quit", "stop"]):
                mic.say("Closing music")
                readCommandMusicXML("quit")
                return
            else:
                mic.say("Can you repeat")
                 
            
                
                
                
            
                

 



 


      



def readCommandMusicXML(commandMusic):
    
        tree = ET.parse(commandMusicFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            elem.text = commandMusic
            
 

        tree.write(commandMusicFile)
        
        

def readCommandXML(musicName):
    
        tree = ET.parse(commandFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            elem.text = "play music"
        for elem in root.iter('name'):  
            elem.text = musicName 
 

        tree.write(commandFile)




