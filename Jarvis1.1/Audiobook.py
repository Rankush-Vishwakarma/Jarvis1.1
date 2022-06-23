# -*- coding: utf-8 -*-
"""
Created on Sat Jan 15 19:06:55 2022

@author: rvishwakar23
"""
try:
    import os
    import pickle
    import random
except Exception as e:
    print('Got some exception in importing the module')


class AudiobookPlayer:
    def __init__(self):
        self._PDFList = []
        self._paused = True
        self._played = False

    def loadPdfs(self):
        print("Please wait i'm loading the all your pdfs ")
        _PDFList = []
        dir_path = os.path.expanduser('~')
        main_folders = ['3d Objects', 'Desktop', 'Documents',
                        'Downloads', 'Music', 'Pictures', 'Videos']
        for root, _, files in os.walk(dir_path):
            if len(root.split('\\')) > 3 and root.split(
                    '\\')[3] in main_folders:
                for file in files:
                    # change the extension from '.mp3' to
                    # the one of your choice.
                    if file.endswith('.pdf'):
                        pdf_path = root + '\\' + str(file)
                        _PDFList.append(pdf_path)
            else:
                pass

        with open('pdfs.pkl', 'wb') as f:
            pickle.dump(_PDFList, f)
        print('I have all your pdfs are now saved')


if __name__ == '__main__':
    pdfs = AudiobookPlayer()
    new_songs = input('Have you downloaded new pdf : ')
    if os.path.exists('pdfs.pkl') and ('y' not in new_songs):
        print('pdfs are saved')
        with open('pdfs.pkl', 'rb') as f:
            _pdfs = pickle.load(f)
    else:
        pdfs.loadPdfs()
        with open('pdfs.pkl', 'rb') as f:
            _pdfs = pickle.load(f)
