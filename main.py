# -*- coding: utf-8 -*-
"""main.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1za1yoW4JTDpfmxwWJuRqPhEWCzFvGJOY
"""

# Copyright 2020, Adwith Malpe, All Rights Reserved.

import nltk #natural language toolkit
#nltk.download()
from nltk.stem.lancaster import LancasterStemmer #used to stem words
stemmer = LancasterStemmer()

import numpy 
import tflearn
import tensorflow
import random
import json
import pickle

#use json to read in the file and loop through it and see all the data and how to read it into python script
#used to train model

with open("intents.json") as file: 
  data = json.load(file)


#get all patterns and determine what group they are in
#tags = groupings

try:
  with open("data.pickle", "rb") as f:
    words, labels, training, output = pickle.load(f)
  
except:
  words = []
  labels = []
  docs_x = []
  docs_y = []

  #loop through all dictionaries within data list
  for intent in data["intents"]:
    for pattern in intent["patterns"]:
      #stemming takes in each word in patterns and brings it down to the root word
      #tokenize: get all the words in the pattern
      wrds = nltk.word_tokenize(pattern) #returns list with all of the different words in it
      words.extend(wrds)
      docs_x.append(wrds) #append pattern of words
      docs_y.append(intent["tag"])

    if intent["tag"] not in labels:
        labels.append(intent["tag"])

  #remove duplicate elements using set
  words = [stemmer.stem(w.lower()) for w in words if w != "?"]
  words = sorted(list(set(words)))

  labels = sorted(labels)

  training = []
  output = []

  out_empty = [0 for _ in range(len(labels))]

  for x, doc in enumerate(docs_x):
    bag = []

    wrds = [stemmer.stem(w) for w in doc]

    for w in words:
      if w in wrds:
        bag.append(1)
      else:
        bag.append(0)

    output_row = out_empty[:] #make a copy
    output_row[labels.index(docs_y[x])] = 1

    training.append(bag)
    output.append(output_row)

  training = numpy.array(training)
  output = numpy.array(output)

  with open("data.pickle", "wb") as f:
    pickle.dump((words, labels, training, output), f)

#build model using tflearn

tensorflow.reset_default_graph()

net = tflearn.input_data(shape=[None, len(training[0])])
net = tflearn.fully_connected(net, 8)
net = tflearn.fully_connected(net, 8)

net = tflearn.fully_connected(net, len(output[0]), activation = "softmax") #softmax gives a probabilty to each of the neurons
net = tflearn.regression(net) #in a regression model, we aim to predict the outoput of a continuous value
model = tflearn.DNN(net) #deep neural network (DNN)

try:
  model.load('model.tflearn')

except:
  model.fit(training, output, n_epoch=1000, batch_size = 8, show_metric=True)
  model.save("model.tflearn")  

    
def bag_of_words(s, words):
  bag = [0 for _ in range(len(words))]

  s_words = nltk.word_tokenize(s)
  s_words = [stemmer.stem(word.lower()) for word in s_words]

  for se in s_words:
    for i, w in enumerate(words):
      if w == se:
        bag[i] = 1

  return numpy.array(bag)     

def chat():
  print("Hello my name is Jarvis, how may I be of service? (Type quit to stop)")
  while True:
    inp = input("You: ")
    if inp.lower() == "quit":
      break

    results = model.predict([bag_of_words(inp, words)])[0]
    results_index = numpy.argmax(results) #gives the index of the greatest value in the list
    tag = labels[results_index]
    
    if results[results_index] > 0.85:
      #open up json file, find specific tag, and then select response
      for tg in data["intents"]:
        if tg['tag'] == tag:
          responses = tg['responses']
    
      print("Jarvis: " + random.choice(responses))
      print()

    else:
      misunderstanding = ["I don't understand.", "Could you try asking something else?", "I still don't understand."]
      print("Jarvis: " + random.choice(misunderstanding))
      print()
  
chat()