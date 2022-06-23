# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 15:44:30 2022

@author: rvishwakar23
"""

import pickle
from os import path
from loggingModule import makeLog


class TODO:
    def __init__(self):
        self._TASKLIST = []
        self._log = makeLog()

    def AddTask(self, task):
        try:
            if path.exists(f"tasks.dat"):
                self._TASKLIST = pickle.load(open("tasks.dat", "rb"))
                self._log.info('task file already exits and loaded \
                               sucessfully')
            self._TASKLIST.append(task)
            pickle.dump(self._TASKLIST, open("tasks.dat", "wb"))
            self._log.info('task has been saved in tasks.dat file \
                           successfully ')
        except Exception as e:
            self._log.error(e)

    def ShowTask(self):
        try:
            _TASKLIST = pickle.load(open("tasks.dat", "rb"))
            if len(_TASKLIST) != 0:
                print(_TASKLIST)
            else:
                self._log.debug('There is no pending task sir')
                print('There is no pending task sir')
        except Exception as e:
            self._log(e)

    def RemoveTask(self, task):
        try:
            _TASKLIST = pickle.load(open("tasks.dat", "rb"))
            for i in _TASKLIST:
                if task in i:
                    _TASKLIST.remove(i)
                    self._log.info(f'{i} Task has been removed successfully')
            pickle.dump(_TASKLIST, open("tasks.dat", "wb"))
        except Exception as e:
            print(e)

    def ClearTasklist(self):
        try:
            _TASKLIST = []
            pickle.dump(_TASKLIST, open("tasks.dat", "wb"))
        except Exception as e:
            self._log.error(e)
