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
    


def preprocessing(file):
    lemmatizer = WordNetLemmatizer()
    # reading the json file
    intents = json.loads(open(file).read())
    
    words = []
    classes = []
    documents = []
    ignore_latters = ['?','!','.',',',"'"]
    for intent in intents['intent']:
        for pattern in intent['pattern']:
            word_list = word_tokenize(pattern)
            words.extend(word_list)
            documents.append((word_list,intent['tag']))
            if intent['tag'] not in classes:
                classes.append(intent['tag'])
    words = [lemmatizer.lemmatize(word) for word in words if word not in ignore_latters]
    words = sorted(set(words))
    
    classes = sorted(set(classes))
    # saving into pickle file
    pickle.dump(words, open('words.pkl','wb'))
    pickle.dump(classes, open('classes.pkl','wb'))
    
    training = []
    
    output_empty = [0]* len(classes)
    
    for document in documents:
        bag = []
        word_patterns = document[0]
        word_patterns = [lemmatizer.lemmatize(word.lower()) for word in word_patterns]
        for word in words:
            bag.append(1) if word in word_patterns else bag.append(0)
        output_row = list(output_empty)
        output_row[classes.index(document[1])] = 1
        training.append([bag,output_row])
    random.shuffle(training)
    training = np.array(training,dtype=object)
    train_x = list(training[:-round(0.25 * len(training)),0])
    train_y = list(training[:-round(0.25 * len(training)),1])
    test_x = list(training[-round(0.25 * len(training)):,0])
    test_y = list(training[-round(0.25 * len(training)):,1])
    return train_x, train_y, test_x, test_y

def build_model(train_x, train_y, test_x, test_y):

    model= Sequential()
    model.add(Dense(128,input_shape=(len(train_x[0]),), activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(64,activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(len(train_y[0]),activation='softmax'))
    
    sgd = SGD(lr=0.01, decay=1e-6, momentum=0.9)
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'] )
    
    model.fit(np.array(train_x),np.array(train_y), epochs=200, batch_size=5, verbose=1 )
    accuracy = model.evaluate(test_x,test_y, batch_size=10000)[1] * 100
    print(f'Accuracy : {accuracy}')
    model.save('chatbot_model01.model')
    print('done')


    
