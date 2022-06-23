# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 19:47:24 2022

@author: rvishwakar23
"""

try:
    import random
    import json
    import pickle
    import numpy as np
    import nltk
    from nltk.stem import WordNetLemmatizer
    from tensorflow.keras.models import load_model
    from TrainingChatbot_1 import TrainChatbot
    import colorama
    from colorama import Fore
except Exception as e:
    print(f'Got some exception while importing the model - {e}')
    
    
class Preprocessing:
    global result
    def __init__(self):
        self._lemmatizer = WordNetLemmatizer()
        self.intents = json.loads(open('chats.json').read())
        self.words = pickle.load(open('words.pkl','rb'))
        self.classes = pickle.load(open('classes.pkl','rb'))
        self.model = load_model('chatbotModel.model')
    
    def clean_up_sentence(self,sentence):
        sentence_word = nltk.word_tokenize(sentence)
        sentence_word = [self._lemmatizer.lemmatize(word) for word in sentence_word]
        return sentence_word
    
    def bag_of_word(self,sentence):
        sentence_word = self.clean_up_sentence(sentence)
        bag = [0]*len(self.words)
        for w in sentence_word:
            for i, word in enumerate(self.words):
                if word == w:
                    bag[i] = 1
        return np.array(bag)
    
class Predication(Preprocessing):
    def __init__(self):
        self.return_list = []
        self.preprocess = Preprocessing()
        
    def predict_class(self,sentence):
        bow = self.preprocess.bag_of_word(sentence)
        res= self.preprocess.model.predict(np.array([bow]))[0]
        ERROR_THRESHOLD = 0.25
        result = [[i,r] for i , r in enumerate(res) if r > ERROR_THRESHOLD]
        result.sort(key=lambda x:x[1],reverse=True)
        #return_list = []
        for r in result:
            self.return_list.append({'intent':self.preprocess.classes[r[0]],'probability':str(r[1])})
        return self.return_list
    
    def get_response(self,intents_list,intent_json ):
        tag = intents_list[0]['intent']
        list_of_intents = intent_json['intent']
        for i in list_of_intents:
            if i['tag'] == tag:
                result = random.choice(i['responses'])
                break
        return result