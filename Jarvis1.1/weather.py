# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 23:06:25 2022

@author: rvishwakar23
"""
try:
    import bs4
    from bs4 import BeautifulSoup
    import requests
    import pandas as pd
    from datetime import datetime
    import ssl
    import socket
    import urllib3
    import OpenSSL
    import warnings
    import os
    from loggingModule import makeLog
    import sys
    import pyautogui
    from fileVault import FileVault
    from requests.packages.urllib3.exceptions import InsecureRequestWarning
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    warnings.filterwarnings('ignore', '.*do not.*', )
except Exception as e:
    print(f'Got exception in importing the module')
    
class GetWeather:
    def __init__(self,city):
        self.city_name = city
        #self.API_key = 'dda7bf778dc00c1970b70960b35f1417'
        try:
            self.log = makeLog()
            #self.API_key = os.environ.get('weather_API_key')
            self.vault = FileVault()
            #if self.API_key == None:
            #    self.log.debug('Api key has not been set')
            #    print("API key has not been set please set API key with ' weather_API_key' name")
            #    self.API_key = pyautogui.prompt('Please enter you openweather API key ')
            if self.vault.checkErr():
                password =  pyautogui.password("You have not set up any password yet Please set a paswword")
                self.vault.setPassword(password)
                keys = self.vault.checkPassword(password)
            else:
                password = pyautogui.password("Please tell me secret passcode to open your vault ")
                keys = self.vault.checkPassword(password)
                
            self.API_key = keys['API_key']
            
        except Exception as e:
            self.log.error(e)
    def __report_time(self):
        current_time = datetime.now().strftime('%I:%M %p')
        return current_time
    
    def Weather(self):
        try:
            #API_key = 'dda7bf778dc00c1970b70960b35f1417'
            complete_api = f"https://api.openweathermap.org/data/2.5/weather?q={self.city_name}&appid={self.API_key}"
            
            api_link = requests.get(complete_api, verify=False)
            api_data = api_link.json()
            if api_data['cod'] == '404':
                self.log.error('404 error is comming out check the city name please')
                print(f'invalid city {self.city_name}, please check your city')
            else:
                temp_city = ((api_data['main']['temp'])-273.15)
                weather_description = api_data['weather'][0]['description']
                humidity = api_data['main']['humidity']
                wind_speed = api_data['wind']['speed']
                degree_sign = u"\N{DEGREE SIGN}"
                print(f'_____________________________________\n\n weather stat for - {self.city_name} city at {self.__report_time()}\n_____________________________________\n')
                print(f'current temprature\t {round(temp_city)} {degree_sign}C \ncurrent weather\t\t {weather_description}\ncurrent humidity\t {humidity}\ncurrent wind speed\t {wind_speed} km/hr')
                self.log.info('Weather stats has been showned successfully.')
        except  requests.exceptions.ConnectionError as conn:
            print('there is no Network please check your internet connection')
            self.log.error(f'Internet Connection is not available - {conn}')
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ReadTimeout, requests.exceptions.Timeout,
                    requests.exceptions.SSLError, requests.exceptions.ConnectionError, ssl.SSLError, AttributeError,
                    ConnectionRefusedError, socket.timeout, urllib3.exceptions.ReadTimeoutError, OpenSSL.SSL.WantReadError,
                    urllib3.exceptions.DecodeError, requests.exceptions.ContentDecodingError) as err:
            print(f'SSL : bad handshake certificate is not downloaded - {err} ')
            self.log.error(f'SSL : bad handshake certificate is not downloaded - {err} ')
        except Exception as e:
            print(f'Got some unkonwn Exception - {e}')
            self.log.error(f'Got some unkonwn Exception - {e}')
        