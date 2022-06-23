# -*- coding: utf-8 -*-
"""
Created on Sun Feb 13 12:47:04 2022

@author: rvishwakar23
"""

# To access Spotipy
import spotipy
# To View the API response
import json
from tenacity import retry, stop_after_attempt

# To open our song in our default browser
import webbrowser
from selenium import webdriver
import json
from selenium.webdriver.common.keys import Keys
import spotipy
from retry import retry
import webbrowser
from time import sleep
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

loginSucess = False
songPlayed = False
loginCount = 0

allreadyLogin = False

username = '315yjv3ud45yakwwanfkdh6izbbm'
clientID = 'b196968f58db4db0a7af5c4f714e5292'
clientSecret = '8ed8fd57dc1942baa91aa7e3cf90528a'
redirectURI = 'http://google.com/'

oauth_object = spotipy.SpotifyOAuth(clientID,clientSecret,redirectURI)
token_dict = oauth_object.get_access_token()
token = token_dict['access_token']
spotifyObject = spotipy.Spotify(auth=token)
user = spotifyObject.current_user()
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# To print the response in readable format.
print(json.dumps(user,sort_keys=True, indent=4))


def ClickedLoginButton(maxAttempt = 5):
    LoginButtonPressed = False
    attempt = 0
    while attempt<maxAttempt:
        sleep(1)
        try:   
            loggedIN = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/button')
            if loggedIN.accessible_name == 'Rankush':
                break
                return
        except:
            if not LoginButtonPressed:
                try:
                    login = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/div[5]/button[2]').click()
                    LoginButtonPressed = True
                    print('Login button pressed suceessfully ')
                    break
                except:
                    LoginButtonPressed = False
                    attempt+=1
                    print(f'attempting Login button ... {attempt}')
                
def ClickedUserName(maxAttempt=5):
    attempt = 0
    UserKeysSendSuccess = False
    while attempt<maxAttempt:
        sleep(1)
        try:
            loggedIN = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/button')
            if loggedIN.accessible_name == 'Rankush':
                break
                return
        except:
            if not UserKeysSendSuccess:
                try:
                    username = browser.find_element_by_xpath('//*[@id="login-username"]')
                    username.send_keys('rankush.vishwakarma46@gmail.com')
                    password = browser.find_element_by_xpath('//*[@id="login-password"]')
                    password.send_keys('Iamtheceo01@')
                    loging = browser.find_element_by_xpath('//*[@id="login-button"]').click()
                    UserKeysSendSuccess = True
                    print('user key send and login successfully.')
                    break
                except:
                    UserKeysSendSuccess = False
                    attempt+=1
                    print(f'attempting username ... {attempt}')
                
def login(maxAttempt=5):
    attempt  = 0
    loginSucess = False
    while attempt<maxAttempt:
        sleep(1)
        try:
            loggedIN = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[1]/header/button')
            if loggedIN.accessible_name == 'Rankush':
                break
                return
        except:
            try:
                closeTrust = browser.find_element_by_xpath('//*[@id="onetrust-close-btn-container"]/button').click()
                loginSucess = True
                allreadyLogin = True
                print('Closed the trust page crosee and logged in  successfully  ')
                break
            except:
                attempt+=1
                loginSucess = False
                print(f'attempting Login success ... {attempt}')
    return loginSucess
    
def PlayAndPauseSong(maxAttempt=5):
    attempt  = 0
    songPlayed = False
    while attempt<maxAttempt and not songPlayed:
        sleep(1)
        try:
            playbutton = browser.find_element_by_xpath('//*[@id="main"]/div/div[2]/div[3]/div[1]/div[2]/div[2]/div/div/div[2]/main/section/div[3]/div/button[1]').click()
            print('Song has opened in your browser.')
            songPlayed = True
            break
        except Exception as e:
            attempt+=1
            songPlayed = False
            print(f'attempting Playing song success ... {attempt}')
def searchNewSong():
    searchQuery = input("Enter Song Name: ")
    # Search for the Song.
    searchResults = spotifyObject.search(searchQuery,1,0,"track")
    # Get required data from JSON response.
    tracks_dict = searchResults['tracks']
    tracks_items = tracks_dict['items']
    song = tracks_items[0]['external_urls']['spotify']
    
    # Open the Song in Web Browser
    browser.get(song)
    
while True:
    print("Welcome, "+ user['display_name'])
    print("0 - Exit")
    print("1 - Search for a Song")
    songPlayed = False
    choice = int(input("Your Choice: "))
    if choice == 1 :
        # Get the Song Name.
        searchNewSong()
        if not allreadyLogin:
            ClickedLoginButton()
            ClickedUserName()
            loginSucess = login()
            allreadyLogin = True
        else:
            pass
        PlayAndPauseSong()
        
    elif choice == 0:
        break
    else:
        print("Enter valid choice.")
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        