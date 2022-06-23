# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 19:06:55 2022

@author: rvishwakar23
"""
try:
    import pygame
    pygame.init()
    
    import os
    import pickle
    import random
except Exception as e:
    print('Got some exception in importing the module')


class MusicPlayer:
    def __init__(self):
        self._currently_playing_song = None
        self._SongList = []
        self._paused = True
        self._played = False
        
    def loadSongs(self):
        print("Please wait i'm loading the songs ")
        _SongList = []
        dir_path = os.path.expanduser('~')
        main_folders = ['3d Objects','Desktop','Documents',
                        'Downloads','Music','Pictures','Videos']  
        for root, _, files in os.walk(dir_path):
            if len( root.split('\\'))>3 and root.split('\\')[3] in main_folders:
                for file in files: 
                    # change the extension from '.mp3' to 
                    # the one of your choice.
                    if file.endswith('.mp3'):
                        song_path = root+'\\'+str(file)
                        _SongList.append(song_path)
            else:
                pass
            
        with open('songs.pkl','wb') as f:
            pickle.dump(_SongList,f)
        print('Songs are now saved')
   
    
    def play_a_different_song(self,_songs=None):
        if type(_songs) == list:
            next_song = random.choice(_songs)
        else:
            next_song = _songs
        while next_song == self._currently_playing_song:
            next_song = random.choice(_songs)
        self._currently_playing_song = next_song
        pygame.mixer.music.load(next_song)
        pygame.mixer.music.play()
        self._paused = False
        self._played = True
        return self._played
        
        
    def pause_and_unpause(self):
        if not self._paused:
            self._paused = True
            pygame.mixer.music.pause()
        else:
            self._paused = False
            pygame.mixer.music.unpause()
            
    def stopSong(self):
        pygame.mixer.music.stop()
    def setVolume(self,volume):
        pygame.mixer.music.set_volume(float(volume))
    def increaseVolume(self):
        current_volume = pygame.mixer.music.get_volume()
        self.setVolume(current_volume+0.175)
    def decreaseVolumne(self):
        current_volume = pygame.mixer.music.get_volume()
        self.setVolume(current_volume-0.175)


if __name__ == '__main__':
    music = MusicPlayer()
    new_songs = input('Have you downloaded new songs : ')
    if os.path.exists('songs.pkl') and ('y' not in new_songs):
        print('songs are saved')
        with open('songs.pkl','rb') as f:
            _songsList = pickle.load(f)
    else:
       music.loadSongs()
       with open('songs.pkl','rb') as f:
           _songsList = pickle.load(f)