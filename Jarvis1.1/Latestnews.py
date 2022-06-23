# -*- coding: utf-8 -*-
"""
Created on Thu Jan 20 18:49:56 2022

@author: rvishwakar23
"""

import pyttsx3
import requests
import json
import time
import re
import sys
from bs4 import BeautifulSoup
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

class speaker:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.voices = self.engine.getProperty('voices')
        self.engine.setProperty('voice', self.voices[1].id)
        self.engine.setProperty('rate',190)
    def speak(self,transcribed_query):
        try:
            print(transcribed_query)
            self.engine.say(transcribed_query)
            self.engine.runAndWait()
        except KeyboardInterrupt:
            print('Thankyou...')
        
    
class news:
    def __init__(self, country):
        self.success = False
        self.country = country
        self.code = {}
    def getCountryCode(self,maxattempt = 4):
        attempt = 1
        while not self.success:
            try:
                try:
                    code = {}
                    countrycode = requests.get('https://www.iban.com/country-codes',verify=False)
                    soup = BeautifulSoup(countrycode.text, 'html.parser')
                    table = soup.find_all('table')[0].tbody
                    data = map(lambda x: (x.findAll(text=True)[1],x.findAll(text=True)[3]),table.findAll('tr'))
                    for i in data:
                       x = re.sub("[\(\[].*?[\)\]]", "", i[0]).replace('.','').lower()
                       code[x] = i[1].lower()
                    if code:
                        self.success = True
                        return code
                    else:
                        self.success = False
                        return None
                except:
                    self.success = False
                    print('not available, trying...')
            except:
                if attempt == maxattempt:
                    self.success = False
                    break
                attempt +=1
            
    def getTopNews(self):
        country_code = ''
        News = {}
        code = self.getCountryCode()
        if  self.success:
            for key,value in code.items():
                if self.country in key:
                    country_code = value
            #print(country_code)   
            url = f'https://newsapi.org/v2/top-headlines?country={country_code}&category=business&apiKey=2f12c53134b14cb4b28a407ec6fa53fb'
            try:
                response = requests.get(url, verify=False)
                Allnews = json.loads(response.text)
                for news in Allnews['articles']:
                    News[str(news['title'])] = str(news['description'])
                return News
            except Exception as e:
                print("can, t access link, plz check you internet ", str(e))
        else:
            print("Didn't get any country code")
        