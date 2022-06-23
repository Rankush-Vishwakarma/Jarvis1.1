import random
import json
import pickle
import numpy as np
import nltk
import time
import pandas as pd
import nltk.corpus
import string
import unicodedata
from nltk.corpus import stopwords
import spacy
import re
import requests
import contractions
from textblob import TextBlob
from nltk.stem import WordNetLemmatizer
from tensorflow.keras.models import load_model
import colorama
from colorama import Fore
from trainingChatbot import *
from loggingModule import makeLog
lemmatizer = WordNetLemmatizer()

global result

log = makeLog()

def loadModel():
    try:
        intents = json.loads(open('chats.json').read())
        words = pickle.load(open('words.pkl','rb'))
        classes = pickle.load(open('classes.pkl','rb'))
        model = load_model('chatbot_model01.model')
        log.info('model loaded Sucessfully')
        print('model loaded Sucessfully ')
        return intents, words, classes, model
    except Exception as e:
        print('Got some exception while importing the pre-trained Model')


def cleanText_(text):  
  """
    0. convert abbr. to original text i am using https://www.webopedia.com/reference/text-abbreviations/
    1. normalize the text.
    2. Removing Unicode Characters
    3. Removing Stopwords
    4. Stemming and Lemmatization
    5. remove puctuations.
    6. removing special and accented charcters
    7. removing numbers
  """
 

  gotAbbribiation = False

  nltk.download('stopwords',quiet=True)
  nlp_lemm = spacy.load('en_core_web_sm')#,parse=True, tag=True, entity=True)

  # removing emails and replacing it with its username
  text = ' '.join([i.split('@')[0] if '@' in i else i for i in text.split()])

  # fetching the abbribiation list
  try:
    url = requests.get('https://dexatel.com/blog/text-abbreviations/')
    df = pd.read_html(url.text)
    df = df[0]
    df.columns = df.iloc[0] 
    df = df[1:]
    df.set_index(["Abbreviations"], inplace = True)
    abbrDict = df.to_dict()['Meaning']
    abbrDict  = dict((k.lower(), v )  for k, v in abbrDict.items() if type(k) == str)
    gotAbbribiation = True
  except Exception as e:
    gotAbbribiation = False
    print(f'Got some exception'+str(e))
 
  # removing the numbers
  text = "".join([i for i in text if not re.search('\d',i)])
  #text = "".join(newText)

  # normalization to lower case
  text = text.lower()

  # handling the contraction in text 
  text = contractions.fix(text)

  # removing https/https links charcters
  text = re.sub(r"http\S+", "", text)

  # removing stopwords
  #text = " ".join([word for word in text.split() if word not in (stopwords.words('english'))])

  # lemmetizing 
  text = nlp_lemm(text)
  text = " ".join([word.lemma_ if word.lemma_ != '-pron-' else word.text for word in text])

  # removing the puctuations
  text = "".join([ch for ch in text if ch not in string.punctuation])

  # removing the accented characters 
  text = unicodedata.normalize('NFKD',text).encode('ascii','ignore').decode('utf-8','ignore')

  # changing the abbribiations
  if gotAbbribiation:
    text = " ".join([abbrDict[i] if i in abbrDict.keys() else i for i in  text.split()])
  
  return str(text)

def clean_up_sentence(sentence):
    cleaned_sentence  = cleanText_(sentence)
    sentence_word = nltk.word_tokenize(sentence)
    sentence_word = [lemmatizer.lemmatize(word) for word in sentence_word]
    return sentence_word

def bag_of_word(sentence):
    sentence_word = clean_up_sentence(sentence)
    bag = [0]*len(words)
    for w in sentence_word:
        for i, word in enumerate(words):
            if word == w:
                bag[i] = 1
    return np.array(bag)

def predict_class(sentence):
    bow = bag_of_word(sentence)
    res= model.predict(np.array([bow]))[0]
    ERROR_THRESHOLD = 0.25
    result = [[i,r] for i , r in enumerate(res) if r > ERROR_THRESHOLD]
    result.sort(key=lambda x:x[1],reverse=True)
    return_list = []
    for r in result:
        return_list.append({'intent':classes[r[0]],'probability':str(r[1])})
    return return_list

def get_response(intents_list,intent_json ):
    tag = intents_list[0]['intent']
    list_of_intents = intent_json['intent']
    for i in list_of_intents:
        if i['tag'] == tag:
            result = random.choice(i['responses'])
            break
    return result
    
def chatbot():
    global intents, words, classes, model
    train_x, train_y, test_x, test_y = preprocessing('chats.json')
    ask = input('\033[1;32m if you have made some changes in json file press Y/y to train the model ').lower()
    if 'y' in ask:
        print(Fore.BLUE + 'chatbot model is training now ')
        build_model(train_x, train_y, test_x, test_y)
        intents, words, classes, model = loadModel()
    else:
        intents, words, classes, model = loadModel()
    return intents, words, classes, model

