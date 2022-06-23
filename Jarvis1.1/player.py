# -*- coding: utf-8 -*-
"""
Created on Tue Jan 18 18:15:41 2022

@author: rvishwakar23
"""

# importing vlc module
import vlc
  
# importing pafy module
import pafy
  
# url of the video
url = "https://www.youtube.com/watch?v=il_t1WVLNxk&list=PLqM7alHXFySGqCvcwfqqMrteqWukz9ZoE"
  
# creating pafy object of the video
video = pafy.new(url)
  
# getting stream at index 0
best = video.streams[0]
  
# creating vlc media player object
media = vlc.MediaPlayer(best.url)
  
# start playing video
media.play()