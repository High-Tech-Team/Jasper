# -*- coding: utf-8-*-
import re
import datetime
import struct
import urllib
import feedparser
import requests
import bs4
import subprocess
from client.app_utils import getTimezone
from semantic.dates import DateService

WORDS = ["WEATHER", "TODAY", "TOMORROW"]





def handle(text, mic, profile):
    mic.say("Showing weather")
    subprocess.call(["pm2", "start","mm"])
    handleForever(mic)
    subprocess.call(["pm2", "stop","mm"])
    return


def handleForever(mic):


        while True:    
            videoName = mic.activeListen()

            if any(ext in videoName for ext in ["quit", "stop"]):
                mic.say("Closing weather")
                return
            else:
                mic.say("Can you repeat")
                

def isValid(text):
    """
        Returns True if the text is related to the weather.

        Arguments:
        text -- user-input, typically transcribed speech
    """
    return bool(re.search(r'\b(weathers?|temperature|forecast|outside|hot|' +
                          r'cold|jacket|coat|rain)\b', text, re.IGNORECASE))
