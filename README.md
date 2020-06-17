# Jarvis-Chatbot
In this repo, you will find a chatbot that I have created in python using imported libraries and conda. This is my first chatbot that responds to general questions and can carry on a basic conversation with an accuracy of 99.2%. Jarvis will only repond to questions above an accuracy of 85% match, otherwise, he will prompt the user to input a different question and that he does not understand. Jarvis will also tell you about what Tesla cars you can purchase today. You can ask Jarvis questions about who he is, how he is doing, what can you buy, and what are the hours of the Tesla store. This chatbot has limited responses and is randomized through an imported random function. I have programmed this chatbot to respond to questions he does not understand as well. The JSON file has all the intents and will be modified more so that Jarvis can further communicate with a user when trained with a larger input data set. 

Listed Intents: greeting, goodbye, age, name, shop, hours

TO RUN THIS PROGRAM, INSTALL THE FOLLOWING:
Python 3.6: https://www.python.org/downloads/
Anaconda: https://www.anaconda.com/

nltk (command: pip install nltk)
numpy (command: pip install numpy)
tflearn (command: pip install tflearn)
tensorflow (command: pip install tensorflow)
