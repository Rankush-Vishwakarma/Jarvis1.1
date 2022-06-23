# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 10:19:37 2022

@author: rvishwakar23
"""

import bcrypt
from cryptography.fernet import Fernet
import json 
from json import JSONDecodeError
from loggingModule import makeLog
class FileVault:
    def __init__(self):
        self._log = makeLog()
        self._filename = 'vault.json'
        self._key = open("key.key", "rb").read()
        
    def checkErr(self):
        try:
            loaded_file_success = False
            if not loaded_file_success:
                f = open(self._filename,'rb')
                data = json.loads(f.read())
                loaded_file_success = True
                self._log.debug('_file_Loading__success')
            
        except JSONDecodeError as e:
            if 'value' in str(e):
                loaded_file_success = False
                self._log.error('loaded_file_success = False')
            else:
                loaded_file_success =  e  
                self._log.error(loaded_file_success)
        finally:
            return loaded_file_success
        
    
    def _write_key(self):
        """
        Generates a key and save it into a file
        """
        try:
            key = Fernet.generate_key()
            with open("key.key", "wb") as key_file:
                key_file.write(key)
            self._log.info('Fernet key has been written successfully')
        except Exception as e:
            self._log.error(e)
   
    def _encrypt(self):
        """
        Given a self._filename (str) and key (bytes), it encrypts the file and write it
        """
        try:
            f = Fernet(self._key)
            checkfile = self.checkErr()
            if type(checkfile) == bool and checkfile == True:
                with open(self._filename, "rb") as file:
                    file_data = file.read()
                if len(file_data) != 0: 
                    encrypted_data = f.encrypt(file_data)
                    with open(self._filename, "wb") as file:
                       file.write(encrypted_data)
                    self._log.info('File has been encrypted successfully')
                    return True
                else:
                    self._log.debug('vault.json file is empty')
            else:
                self._log.error(checkfile+' from _encrypt()')
                return checkfile
        except Exception as e:
            self._log.error(e)
            
    
    def _decrypt(self):
        """
        Given a self._filename (str) and key (bytes), it decrypts the file and write it
        """
        try:
            f = Fernet(self._key)
            with open(self._filename, "rb") as file:
                # read the encrypted data
                encrypted_data = file.read()
            # decrypt data
            
            decrypted_data = f.decrypt(encrypted_data)
            self._log.info('Successfully decrypted')  
            return decrypted_data
        except Exception as e:
            self._log.error(str(e)+' from _decrypt()')
            
        #return 
            

            
    def ChangeData(self,password):
        try:
            #password =  input('Please tell me you password ')
            password = bytes(password, 'utf-8')
            hashed = open("Hashed.key", "rb").read()
            if bcrypt.hashpw(password, hashed) == hashed:
                decrypted_data = self._decrypt() 
                with open(self._filename, "wb") as file:
                    file.write(decrypted_data) 
                self._log.debug('Decrypted Sucessfully you can change the data')
                return 'Decrypted Sucessfully you can change the data'
            else:
                self._log.error('Password is wrong') 
                return 'Password is wrong'
        except Exception as e:
            self._log.error(str(e)+' from changeData()')
    
    def setPassword(self,password):
        try:
            password = bytes(password, 'utf-8')
            # Hash a password for the first time, with a certain number of rounds
            hashed = bcrypt.hashpw(password, bcrypt.gensalt(14))
            canEncrypt = self._encrypt()
            if type(canEncrypt)==bool and canEncrypt == True:
                print('Encypted successfully')
                with open("Hashed.key", "wb") as key_file:
                    key_file.write(hashed) 
                self._log.debug('Hashed  key has been saved successfully')
                print('Hashed  key has been saved successfully')
            else:
                self._log.error(canEncrypt=' from setPassword()')
                print(canEncrypt)
        except Exception as e:
            self._log.error(str(e) +' from setPassword()')
            print('Exception found')
       
    
    def checkPassword(self,password):
        try:
            password = bytes(password, 'utf-8')
            hashed = open("Hashed.key", "rb").read()
            if bcrypt.hashpw(password, hashed) == hashed:
                decrypted_data = self._decrypt() 
                print( 'Decrypted Sucessfully')
                self._log.debug('Decrypted Sucessfully')
                return json.loads(decrypted_data.decode('utf-8'))
            else:
                self._log.error('Password is wrong from checkPassword()')
                print( 'Password is wrong')
        except Exception as e:
            self._log.error(str(e) +' from checkPassword()')
            print(str(e) +' from checkPassword()')

if __name__ == '__main__':
    vault = FileVault()
    if vault.checkErr():
        print('Not Encrypted')
        password = input("tell me passwrod so that i can setup ")
        vault.setPassword(password)
    else:
        print('already Encrypted')
        password = input("tell me secret passcode to open your vault ")
        dict_ = vault.checkPassword(password)

"""
if __name__ == "__main__":
    self._filename = 'vault.json'
    #write_key()
    
    if  checkErr(self._filename):
        print('Not Encrypted')
        password = input("tell me passwrod so that i can setup ")
        setPassword(password, self._filename, key)
    else:
        print(' already Encrypted')
        password = input("tell me secret passcode to open your vault ")
        checkPassword(password, self._filename, key)
        root.grid_rowconfigure(0, weight=1)
        root.grid_columnconfigure(0, weight=1)
"""