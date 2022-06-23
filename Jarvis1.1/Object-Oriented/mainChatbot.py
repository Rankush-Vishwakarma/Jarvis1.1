# -*- coding: utf-8 -*-
"""
Created on Fri Jan 14 20:49:15 2022

@author: rvishwakar23
"""

from MakeChatbot import *
from TrainingChatbot_1 import TrainChatbot
import pyjokes
def get_joke():
    return pyjokes.get_joke(language="en", category="neutral")
if __name__ == '__main__':
    try:
        train = TrainChatbot()    
        train.chatbot()
        prediction = Predication()
        intents = json.loads(open('chats.json').read())
        try:
            print("Press Ctrl+c to interrupt or \' /exit \' to exit  ")
            while True:
                msg = input(Fore.GREEN +  "input message  ")
                if not '/exit' in msg:
                    #ints = predict_class(msg)
                    ints = prediction.predict_class(msg)
                    #res = get_response(ints, intents)
                    res = prediction.get_response(ints, intents)
                    if 'joke' in res or 'joke' in msg or 'tell me ' in msg:
                        if 'joke' in res:
                            print(res+'\t'+get_joke())
                        else:
                            print(get_joke())
                    else:
                        print(res)
                else:
                    print('bye sir!')
                    break
        except KeyboardInterrupt:
            print('thankyou for using')
            pass
    except Exception as e:
        print(Fore.RED+f'Got some exception {e}')
        Fore.RESET
   


