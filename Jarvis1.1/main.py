# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 13:27:43 2022

@author: rvishwakar23
"""
from trainingChatbot import *
from colorama import Fore
from Chatbot import *
import datetime
import pyjokes
from weather import GetWeather
from wikipediaModule import searchWikipedia
import webbrowser
from music import MusicPlayer
import pickle
import os
import playsound
from threading import *
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
import urllib.request
import re
import random
from emailer import emailSender
from fileVault import FileVault
from volumecontroler import VolumeController
import pyautogui
from CovidStat import RealTimeCovid
from Latestnews import speaker, news
import itertools
from audio_book import *
from TODO import *

covidStat = RealTimeCovid()
vault = FileVault()
volumectrl = VolumeController()
audiobookplayer = AudioBookPlayer()
todo = TODO()


def alarm(time):
    while True:
        try:
            # set_alarm_time = f"{hour}:{minute}"
            current_time_hour = datetime.datetime.now().hour
            current_time_min = datetime.datetime.now().minute
            current_time_hour = abs(current_time_hour - 12)
            currentTime = f"{current_time_hour}:{current_time_min}"
            # print(f"{currentTime}, {time}")
            # if int(current_time_hour) == int(hour)
            # And int(current_time_min) == int(minute):
            if currentTime == time:
                print("time to wake up sir")
                return playsound.playsound(r"C:\Users\rvishwakar23\
                                           \Music\Free_Meltdown-Alarm_SPASE01004.wav")
            if currentTime > time:
                break
        except Exception as e:
            print(e)
            pass


def get_joke():
    return pyjokes.get_joke(language="en", category="neutral")


def report_time():
    current_time = datetime.datetime.now().strftime('%I:%M %p')
    return current_time


def report_date():
    return f"Today date is: {datetime.date.today()}"


def cat_video():
    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=cat+video")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
    random_one = random.choice(video_ids)
    webbrowser.open("https://www.youtube.com/watch?v=" + random_one+'?autoplay=1')
    print('you can watch the video sir')


def getCMDText(cmd):
    pattern = 'tell me about '
    matched = re.search(pattern, cmd)
    return matched


def google_search():
    try:
        search_term = input('What do you want me to search ')
        search_url = f"https://www.google.com/search?q={search_term}"
        webbrowser.open(search_url)
    except Exception as google_exception:
        print('google search got some exception  sir ')


def youtube_search():
    try:
        search_term = input('What do you want me to search ')
        html = urllib.request.urlopen("https://www.youtube.com\
                                      /results?search_query=" + search_term.replace(' ', '+'))
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        random_one = random.choice(video_ids)
        webbrowser.open("https://www.youtube.com/watch?v=" + random_one)
        print('You can watch the video sir')
    except Exception as youtube_exception:
        print(f'youtube search got some exception {youtube_exception}')


def open_website():
    try:
        website = input('which website do you want to work with ')
        webbrowser.open(f'https://www.{website}.com')
    except Exception as website_exception:
        print('website opening got some exception sir')


if __name__ == '__main__':
    song_played = False
    Speaker = speaker()
    try:
        music = MusicPlayer()
        new_songs = input('Have you downloaded new songs : ')
        if os.path.exists('songs.pkl') and ('y' not in new_songs):
            with open('songs.pkl', 'rb') as f:
                _songs = pickle.load(f)
            print('songs have been loaded successfully ')
        else:
            music.loadSongs()
            with open('songs.pkl', 'rb') as f:
                _songs = pickle.load(f)
    except Exception as e:
        print(f'Got some exception {e}')
    try:
        intents, words, classes, model = chatbot()
    except Exception as e:
        print(Fore.RED + f'Got some exception {e}')
        Fore.RESET
    try:
        print("Press Ctrl+c to interrupt or \' /exit \' to exit  ")
        while True:
            msg = input(Fore.GREEN + "input message  ")
            if '/exit' not in msg:
                #msg = cleanText_(msg)
                ints = predict_class(msg)
                res = get_response(ints, intents)
                matched = getCMDText(msg)
                if 'joke' in res or 'joke' in msg or 'tell me another' in msg or 'another' in msg:
                    if 'joke' in res:
                        print(res + '\t' + get_joke())
                    else:
                        print(get_joke())
                elif matched is not None:
                    searchedTerm = msg[matched.end():]
                    wiki = searchWikipedia(searchedTerm)
                    wiki.getWikipedia()
                elif 'time' in msg:
                    print(f'current time is {report_time()}')
                elif 'today' in msg and 'date' in msg or 'date' in msg:
                    print(report_date())
                elif 'check weather' in msg or 'weather' in msg or 'environment' in msg:
                    weather = GetWeather('rewa')
                    weather.Weather()
                elif 'google' in msg:
                    google_search()
                elif 'youtube' in msg and 'video' in msg:
                    youtube_search()
                elif 'website' in msg:
                    open_website()
                elif 'play' in msg and 'song' in msg or ('change' in msg and 'song' in msg):
                    if music.play_a_different_song(_songs):
                        song_played = True
                elif 'stop' in msg and 'song' in msg:
                    music.stopSong()
                elif 'decrease' in msg:
                    if song_played:
                        music.decreaseVolumne()
                    else:
                        volumectrl.DecreaseVolume()
                elif 'increase' in msg:
                    if song_played:
                        music.increaseVolume()
                    else:
                        volumectrl.IncreaseVolume()
                elif 'set' in msg and 'volume' in msg:
                    volume = int(input('how much percentage you want to set '))
                    volume = float(volume / 100)
                    music.setVolume(volume)
                elif 'cat' in res or ('cat' in msg and 'video' in msg):
                    flag = input("Do you want me to play the cat video  ")
                    if 'y' in flag:
                        cat_video()
                    else:
                        print('ok sir')
                elif 'send' in msg and 'email' in msg:
                    sender = emailSender()
                    sender.send_email()
                elif 'change data' in msg:
                    password = pyautogui.password("Please tell\
                                                  me secret passcode to open your vault ")
                    print(vault.ChangeData(password))
                elif re.search('covid', msg) is not None:
                    try:
                        covidStat.getCovidStats()
                    except OSError:
                        pass
                    except Exception as e:
                        print(e)
                elif re.search('news', msg) is not None:
                    try:
                        pattern = 'news from '
                        Lindex = re.search(pattern, msg).end()
                        country = msg[Lindex:]
                        Topnews = news(country).getTopNews()
                        NumberOfNews = int(
                            input('how many news you want sir! '))
                        for key, value in dict(itertools.islice(
                                Topnews.items(), NumberOfNews)).items():
                            Speaker.speak(key)
                            Speaker.speak(value)
                    except OSError:
                        pass
                    except Exception as e:
                        print(e)
                elif 'alarm' in msg:
                    time = [x for x in msg.split() if x.isdigit()]
                    setTime = f"{time[0]}:{time[1]}"
                    alarm(setTime)
                elif 'audiobook' in msg or 'read my book' in msg:
                    audiobookplayer.LoadAndPlay()
                elif msg.startswith('add') and msg.endswith('tasklist'):
                    task = ' '.join(s[1:-2])
                    todo.AddTask(task)
                elif msg.startswith('remove') and msg.endswith('tasklist'):
                    task = ' '.join(s[1:-2])
                    todo.RemoveTask(task)
                elif msg.startswith('clear') and msg.endswith('tasklist'):
                    todo.ClearTasklist()
                elif msg.startswith('show') and msg.endswith('tasklist'):
                    todo.ShowTask()
                elif 'bye' in res or 'quit' in msg or 'exit' in msg:
                    print(res)
                    break
                else:
                    print(res)

            else:
                print('bye sir!')
                break

    except KeyboardInterrupt:
        print('thankyou for using')
        pass
