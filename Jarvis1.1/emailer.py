# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 13:51:19 2022

@author: rvishwakar23

"""

from easygui import passwordbox, enterbox
import smtplib, ssl
import json
from smtplib import SMTPAuthenticationError
from loggingModule import makeLog
from fileVault import FileVault
import pyautogui
class emailSender:
    def __init__(self):
        self.log = makeLog()
        self._user_email  = ''
        self._port = 465  # For SSL
        self._smtp_server = "smtp.gmail.com"
        self._sender_email = "rkvishwakarma098@gmail.com"
        self.vault  = FileVault()
    def _loadEmail(self,user):
        with open('emails.json','r') as f:
            data = json.load(f)
        for key, value in data.items():
            if user in key:
                self._user_email =  value
        if len(self._user_email)>0:
            self.log.info(self._user_email)
            return self._user_email
        else:
            self.log.error( f'Sorry did not got the any email address with {user} name username')
            return f'Sorry did not got the any email address with {user} name username,\n  please save new email and username in the emails.json file  '
            
    def send_email(self):
        try:
            user = input("Please tell me the user name - ")
            receiver_email = self._loadEmail(user)
            if '@' in receiver_email:
                if self.vault.checkErr():
                    vaultPass =  pyautogui.password("You have not set up any password yet Please set a paswword")
                    self.vault.setPassword(vaultPass)
                    keys = self.vault.checkPassword(vaultPass)
                else:
                    vaultPass = pyautogui.password("Please tell me secret passcode to open your vault ")
                    keys = self.vault.checkPassword(vaultPass)
                password = keys['emailPassword']
                #password = passwordbox("What is your password ?")
                subject = input("tell me the subject ")
                content  = input("Tell me your message ")
                message = f"Subject: {subject}\n\n{content}\n"
                #print(message)    
                context = ssl.create_default_context()
                with smtplib.SMTP_SSL(self._smtp_server, self._port, context=context) as server:
                    server.login(self._sender_email, password)
                    server.sendmail(self._sender_email, receiver_email, message)
                print('Email sent successfully , Thankyou')
                self.log.info('Email sent successfully , Thankyou')
            else:
                self.log.error(f'Sorry did not got the any email address with {user}')
                print(receiver_email)
        except SMTPAuthenticationError :
            self.log.error(str(SMTPAuthenticationError) + "Please turn on less secure app from gmail. \n Hint: Go to this link and select Turn On https://www.google.com/settings/security/lesssecureapps")
            print("Please turn on less secure app from gmail. \n Hint: Go to this link and select Turn On https://www.google.com/settings/security/lesssecureapps")
        except Exception as e:
            self.log.error(str(e)+ 'from emailSender.send_email()')
            print(f'Got some exception - {e}')
            
            
        