# -*- coding: utf-8-*-
import Queue
import atexit
from modules import Gmail
from apscheduler.schedulers.background import BackgroundScheduler
import logging

from xml.dom import minidom
import os
import xml.etree.ElementTree as ET
from threading import Thread, Lock
import datetime
from client.mic import Mic

magicFile=os.path.abspath("Desktop/beamy/button/XML/magic.xml")

class Notifier(object):

    class NotificationClient(object):

        def __init__(self, gather, timestamp):
            self.gather = gather
            self.timestamp = timestamp

        def run(self):
            self.timestamp = self.gather(self.timestamp)

    def __init__(self, profile,mic):
        self._logger = logging.getLogger(__name__)
        self.q = Queue.Queue()
        self.profile = profile
        self.notifiers = [self.NotificationClient(self.handleMagicNotifications, None)]
        self.mic=mic

        if 'gmail_address' in profile and 'gmail_password' in profile:
            self.notifiers.append(self.NotificationClient(
                self.handleEmailNotifications, None))
        else:
            self._logger.warning('gmail_address or gmail_password not set ' +
                                 'in profile, Gmail notifier will not be used')

        sched = BackgroundScheduler(timezone="UTC", daemon=True)
        sched.start()
        sched.add_job(self.gather, 'interval', seconds=30)
        atexit.register(lambda: sched.shutdown(wait=False))

    def gather(self):
        [client.run() for client in self.notifiers]

    def handleEmailNotifications(self, lastDate):
        """Places new Gmail notifications in the Notifier's queue."""
        emails = Gmail.fetchUnreadEmails(self.profile, since=lastDate)
        if emails:
            lastDate = Gmail.getMostRecentDate(emails)

        def styleEmail(e):
            return "New email from %s." % Gmail.getSender(e)

        for e in emails:
            self.q.put(styleEmail(e))

        return lastDate
    
    
    def handleMagicNotifications(self,lastDate):
        
        print("ok")
        start=readMagicXML()
        print(start)
        if start == "1":
            print("ok")
            lastDate=datetime.datetime.now()
            self.mic.say("Showing magic")
            while True :
                    command = self.mic.activeListen()
                    if any(ext in command for ext in ["quit", "stop"]):
                        self.mic.say("Closing magic")
                        changeMagicXML("quit")
                        return
                    else:
                        self.mic.say("Can you repeat")
        return lastDate
        
        

    def getNotification(self):
        """Returns a notification. Note that this function is consuming."""
        try:
            notif = self.q.get(block=False)
            return notif
        except Queue.Empty:
            return None

    def getAllNotifications(self):
        """
            Return a list of notifications in chronological order.
            Note that this function is consuming, so consecutive calls
            will yield different results.
        """
        notifs = []

        notif = self.getNotification()
        while notif:
            notifs.append(notif)
            notif = self.getNotification()

        return notifs
    
def readMagicXML():
    
        tree = ET.parse(magicFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            return elem.text

def changeMagicXML(text):

        tree = ET.parse(magicFile)  
        root = tree.getroot()

        # changing a field text
        for elem in root.iter('etat'):  
            elem.text == text
                
        tree.write(magicFile)  
     


