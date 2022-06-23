# -*- coding: utf-8 -*-
"""
Created on Mon Jan 17 17:26:20 2022

@author: rvishwakar23
"""
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import math
from loggingModule import makeLog
# Get default audio device using PyCAW
class VolumeController:
    #global currentVolumeDb
    def __init__(self):
        try:
            self._log = makeLog()
            self._devices = AudioUtilities.GetSpeakers()
            self._interface = self._devices.Activate(
                IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
            self._volume = cast(self._interface, POINTER(IAudioEndpointVolume))
        except Exception as e:
            self._log.error( str(e) +' from VolumeController.__init__()')
    def IncreaseVolume(self):
        try:   
            currentVolumeDb = self._volume.GetMasterVolumeLevel()
            self._volume.SetMasterVolumeLevel(currentVolumeDb + 6.0, None)
            if currentVolumeDb > -6.306526184082031:
                self._log.info('Maximum Volume reached')
                print('Maximum Volume reached')
                self._volume.SetMasterVolumeLevel(-0.0, None)    
                pass
        except Exception as e:
            self._log.error(str(e) +' from IncreaseVolume()')
            pass
    def DecreaseVolume(self): 
        try:
            currentVolumeDb = self._volume.GetMasterVolumeLevel()
            self._volume.SetMasterVolumeLevel(currentVolumeDb - 6.0, None)
            #print(currentVolumeDb)
            if currentVolumeDb < -48.30652618408203:
                print('Minimum volume reached')
                self._log.info('Minimum volume reached')
                self._volume.SetMasterVolumeLevel(-54.0, None)
                pass
        except Exception as e:
            self._log.error(str(e) +' from DecreaseVolume()')
            pass
        


# Get current volume 
