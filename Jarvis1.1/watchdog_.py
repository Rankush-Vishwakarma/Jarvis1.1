# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 12:15:16 2022

@author: rvishwakar23
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
# import the modules
# import time module, Observer, FileSystemEventHandler
import watchdog.events
import watchdog.observers
import time


class Handler(watchdog.events.PatternMatchingEventHandler):
	def __init__(self):
		# Set the patterns for PatternMatchingEventHandler
		watchdog.events.PatternMatchingEventHandler.__init__(self, patterns=['*.json'],
															ignore_directories=True, case_sensitive=False

	def on_modified(self, event):
		print("Watchdog received modified event - % s." % event.src_path)
		return True
		# Event is modified, you can process it now


if __name__ == "__main__":
	src_path = r"C:\Users\rvishwakar23\Desktop\data scientist\ineuron\Jarvis 1.1\Ai_chatbot"
	event_handler = Handler()
	observer = watchdog.observers.Observer()
	observer.schedule(event_handler, path=src_path, recursive=True)
	observer.start()
	try:
		while True:
			time.sleep(1)
	except KeyboardInterrupt:
		observer.stop()
	observer.join()
