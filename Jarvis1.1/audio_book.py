# -*- coding: utf-8 -*-
"""
Created on Sat Feb  5 23:35:21 2022

@author: rvishwakar23
"""

from Audiobook import *
import pyttsx3
import PyPDF2
from Latestnews import speaker
from gtts import gTTS
from os.path import exists
from alive_progress import alive_bar
from progress.bar import Bar
from time import sleep
import os.path
from os import path
from progress.spinner import MoonSpinner
import warnings
from music import MusicPlayer
import threading
import sys
warnings.filterwarnings("ignore")
global background
from loggingModule import makeLog

def background(f):
    '''
    a threading decorator
    use @background above the function you want to run in the background
    '''
    def backgrnd_func(*a, **kw):
        threading.Thread(target=f, args=a, kwargs=kw, daemon=True).start()
    return backgrnd_func
 
class AudioBookPlayer:
    def __init__(self):
        self._log = makeLog()
        try:
            self.FoundFile = False
            self.pdfs = AudiobookPlayer()
            self.music = MusicPlayer()
            self._log.info('intialized successfully')
        except exception as e:
            self._log.error('unsucessful initalization')
            sys.exit

    def checkFileExit(self,filename):
        if path.exists(f"{filename}_audiobook.mp3"):
            return os.path.abspath(f"{filename}_audiobook.mp3")
        else:
            return None
        
    def returnPdfPath(self,filename):
        file = ''
        new_songs = input('Have you downloaded new pdf : ')
        if os.path.exists('pdfs.pkl') and ('y' not in new_songs):
            print('pdfs are saved')
            self._log.debug('pdfs have been already saved  in pdfs.pkl file')
            with open('pdfs.pkl','rb') as f:
                _pdfs = pickle.load(f)
        else:
           self.pdfs.loadPdfs()
           self._log.debug('Loaded the all pdfs from respective default libaray')
           with open('pdfs.pkl','rb') as f:
               _pdfs = pickle.load(f)
        
        for i in _pdfs:
            if filename in i.lower():
                self._log.info('got the file sir')
                self.FoundFile = True
                file =  i
        if self.FoundFile:
            return file
        else:
            sys.exit 
            
    def getReader(self,path):
        try:
            book = open(path, 'rb')
            pdfReader = PyPDF2.PdfFileReader(book)
            self._log.info('pdfReader object has been inititialized successfully.')
            return pdfReader
        except Exception as e:
            self._log.error(f'Got exception while intializing the pdfReader {e}')
    
    @background
    def saveAudio(self,gttobj,AudioFileName):
        try:
            self._log.info('Audio conversion job has been submitted to the background')
            gttobj.save(f"{AudioFileName}_audiobook.mp3")
            self._log.info('Audio file has been generated in the same folder sucessfully')
        except Exception as e:
            self._log.error('Not able to save AudioBook file thankyou!')
            pass
    
 
    def LoadAndPlay(self):
        try:
            all_text = ''
            textbook = []
            i,k,n=0,0,0
            speak = speaker()
            filename = input('tell me your pdf name ')
            pdfPath = self.returnPdfPath(filename)
            if pdfPath != False:
                reader = self.getReader(pdfPath)
                pages = reader.numPages
                AudioFileName1 = pdfPath.split('\\')[-1]
                AudioFileName = AudioFileName1.split('.')[0]
                if self.checkFileExit(AudioFileName) == None:
                    print(f'Found the File successfully with name as {AudioFileName1}')
                    self._log.info(f'Found the File successfully with name as {AudioFileName1}')
                    try:
                        for p in range(i,pages):
                            page = reader.getPage(p) 
                            text = page.extractText()
                            textbook.append(text)
                    except Exception as e:
                        self._log.error(e)
                   
                    try:
                            all_text = ''.join(textbook)
                            gt_obj = gTTS(all_text)
                    except Exception as e:
                        self._log.debug(e)
                        pass
                    print('\nplease wait i\'m converting into audiobook.\t\t Processing…')
                    try:
                        self.saveAudio(gt_obj,AudioFileName)
                        print('\n Audiobook Conversion Job has been submitted, will be available to play after some time thankyou ')
                    except Exception as e:
                        print('\n Audiobook Conversion Job has been aborted ')
                        self._log.error('Audiobook Conversion Job has been aborted ')
                        pass
                    print('playing some page for you sir! ')
                    self._log.info('user demand for playing some page')
                    while True:
                        try:
                            page = reader.getPage(n) 
                            text = page.extractText()
                            speak.speak(text)
                            ask = input('Do you want me to play next page to you sir')
                            if 'y' in ask:
                                n+=1
                                self._log.info('user requested for playing another page')
                                continue
                            else:
                                break
                        except Exception as e:
                            print(f'got exception {e}')
                            self._log.debug(f'got exception {e}')
                            pass
                        except KeyboardInterrupt:
                            self._log.debug('User has tried to interrupt the service')
                            break
                else:
                    try:
                        print('An Audiobook is already present in the directory. ')
                        self._log.info('An Audiobook is already present in the directory. ')
                        audiobook = self.checkFileExit(AudioFileName)
                        audiobook = audiobook.replace("\'", "\\")
                        self.music.play_a_different_song(audiobook)
                        self._log.info(f'Audio book {AudioFileName} has been played sucessfully')
                    except Exception as e:
                        print('file is still in conversion process please wait few second')
                        self._log.debug('file is still in conversion process please wait few second or doesn\'nt exit right now')
            else:
                sys.exit
        except Exception as e:
            self._log.error(e)
            print(e)
        except KeyboardInterrupt:
            self._log.debug('User has tried to interrupt the service')
            pass
            

#if __name__ == '__main__':
    
    
    #choice = int(input('1. do you want me to play the pdf file? \n2. do you want me to save the file?\t'))
    