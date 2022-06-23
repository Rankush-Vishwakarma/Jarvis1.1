# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 11:18:15 2022

@author: rvishwakar23
"""
import wikipedia
import re
import unicodedata
import string
import requests
from loggingModule import makeLog

class searchWikipedia:
    def __init__(self, query):
        self.query = query
        self.log = makeLog()
    
    def remove_special_char(self,text):
      pattern  = r'[^a-zA-Z0-9]'
      return re.sub(pattern, ' ', text)
  
    def remove_accent(self,text):
      new_text = unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode('utf-8','ignore')
      return new_text
    
    def remove_punctuations(self,messy_words):
      clean_list = [ch for ch in messy_words if ch not in string.punctuation]
      clean_str = "".join(clean_list)
      return clean_str
    
    def getWikipedia(self):
        try:
            result = wikipedia.summary(self.query, sentences=4)
            result = self.remove_special_char(result)
            result= self.remove_accent(result)
            result = self.remove_punctuations(result)
            print(result)
            self.log.info('search has been completed.')
            #speak(result)
        except requests.exceptions.SSLError as request_err:
            #speak('sir we have got the request handshake error')
            print('sir we have got the request handshake error')
            self.log.error(request_err)
        except wikipedia.exceptions.PageError as p:
            #speak('Sorry sir page not found')
            print('Sorry sir page not found')
            self.log.error(p)
        except ValueError as v:
            #speak('use search function sir you have not said Title or Pageid')
            print('use search function sir you have not said Title or Pageid')
            self.log.error(v)
        except wikipedia.exceptions.DisambiguationError as ambigious:
            #speak('Ambiguity found on the keyword sir, please use wikipedia again')
            print('Ambiguity found on the keyword sir, please use wikipedia again')
            self.log.error(ambigious)
        except ConnectionError as conn:
            print('There is no internet connection')
            self.log.error(conn)
        except Exception as e:
            print('Got some exception please check log file.')
            self.log.error(e)