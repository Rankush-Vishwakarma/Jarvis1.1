# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 18:44:50 2022

@author: rvishwakar23
"""

try:
    import random
    import json 
    import pickle
    import numpy as np
    import nltk
    import colorama
    from colorama import Fore
    nltk.download('punkt')
    nltk.download('wordnet')     
    from nltk import word_tokenize
    from nltk.stem import WordNetLemmatizer
    from tensorflow.keras.models import Sequential
    from tensorflow.keras.layers import Dense, Activation, Dropout
    from tensorflow.keras.optimizers import SGD
except Exception as e:
    print(f"We have got some exception - {e}")

class Preprocessing:
    def __init__(self):
        self.lemmatizer = WordNetLemmatizer()
        self.words = []
        self.classes = []
        self.documents = []
        self.training = []
        self.ignore_latters = ['?','!','.',',',"'"]
        
    def preprocessing(self): 
        # reading the json file
        try:
            intents = json.loads(open('chats.json').read())
            for intent in intents['intent']:
                for pattern in intent['pattern']:
                    word_list = word_tokenize(pattern)
                    self.words.extend(word_list)
                    self.documents.append((word_list,intent['tag']))
                    if intent['tag'] not in self.classes:
                        self.classes.append(intent['tag'])
            self.words = [self.lemmatizer.lemmatize(word) for word in self.words if word not in self.ignore_latters]
            self.words = sorted(set(self.words))
            self.classes = sorted(set(self.classes))
            # saving into pickle file
            pickle.dump(self.words, open('words.pkl','wb'))
            pickle.dump(self.classes, open('classes.pkl','wb'))
        except Exception as e:
            print(f'Got some Exception while Preprocessing - {e}')
    
    def SplitTrainTestData(self):
        try:
            output_empty = [0]* len(self.classes)
            for document in self.documents:
                bag = []
                word_patterns = document[0]
                word_patterns = [self.lemmatizer.lemmatize(word.lower()) for word in word_patterns]
                for word in self.words:
                    bag.append(1) if word in word_patterns else bag.append(0)
                output_row = list(output_empty)
                output_row[self.classes.index(document[1])] = 1
                self.training.append([bag,output_row])
            random.shuffle(self.training)
            self.training = np.array(self.training,dtype=object)
            self.train_x = list(self.training[:,0])
            self.train_y = list(self.training[:,1])
            return self.train_x, self.train_y
        except Exception as e:
            print(f'Got some Exception while spliting the data - {e}')

class CNNmodel(Preprocessing):
    def __init__(self):
        self._lr = 0.01
        self._decay = 1e-6
        self._momentum = 0.9
        self._epochs = 200
        self._batch_size = 5
        self._verbose = 1
    def build_model(self,train_x, train_y):
        try:
            model= Sequential()
            model.add(Dense(128,input_shape=(len(train_x[0]),), activation='relu'))
            model.add(Dropout(0.5))
            model.add(Dense(64,activation='relu'))
            model.add(Dropout(0.5))
            model.add(Dense(len(train_y[0]),activation='softmax'))
            
            #sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9)
            sgd = SGD(lr=self._lr, decay=self._decay, momentum=self._momentum)
            model.compile(loss='categorical_crossentropy', optimizer=sgd, metrics=['accuracy'] )
            #model.fit(np.array(train_x),np.array(train_y), epochs=200, batch_size=5, verbose=1 )
            model.fit(np.array(train_x),np.array(train_y), epochs = self._epochs, batch_size=self._batch_size, verbose= self._verbose )
            model.save('chatbotModel.model')
            print('done')
        except Exception as e:
            print(f'Got some exception while building the model - {e}')
            
class TrainChatbot(CNNmodel):
    def __init__(self):
        self.preprocessing = Preprocessing()
        self.preprocessing.preprocessing()
        self.train_x, self.train_y = self.preprocessing.SplitTrainTestData()
        self.model = CNNmodel()
    def chatbot(self):
        #train_x, train_y = preprocessing()
        try:
            ask = input('\033[1;32m if you have made some changes in json file press Y/y to train the model ').lower()
            if ask == 'y':
                print(Fore.RED + 'chatbot model is training now ')
                self.model.build_model(self.train_x, self.train_y)
            else:
                print('Thankyou!')
        except Exception as e:
            print(f'Got some Exception while training the model - {e}')
        