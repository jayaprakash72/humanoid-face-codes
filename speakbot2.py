# -*- coding: utf-8 -*-
"""
Created on Wed Jun  9 20:03:59 2021

@author: jay
"""



import pyttsx3
import webbrowser
import requests
import smtplib
import random
import speech_recognition as sr
import wikipedia
import datetime
import wolframalpha
import os
import sys
import bs4
import selenium
from selenium import webdriver
from bs4 import BeautifulSoup
import pyjokes
import requests 
import json    
from datetime import datetime
import time
import json
from googletrans import Translator
import winsound
from win10toast import ToastNotifier
import pickle
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer
lemmatizer = WordNetLemmatizer()

from keras.models import load_model
model = load_model('chatbot_model.h5')
import json
import random

engine = pyttsx3.init('sapi5')

client = wolframalpha.Client('Your_App_ID')

voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)


intents = json.loads(open('intents.json').read())
words = pickle.load(open('words.pkl','rb'))
classes = pickle.load(open('classes.pkl','rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words

# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0]*len(words)  
    for s in sentence_words:
        for i,w in enumerate(words):
            if w == s: 
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print ("found in bag: %s" % w)
    return(np.array(bag))

def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words,show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i,r] for i,r in enumerate(res) if r>ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list

def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if(i['tag']== tag):
            result = random.choice(i['responses'])
            break
    return result

def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


def speak(audio):
    print('Computer: ' + audio)
    engine.say(audio)
    engine.runAndWait()

def jarvis():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold =  1
        audio = r.listen(source)
    try:
        query = r.recognize_google(audio, language='en-in')
        #print('User: ' + query + '\n')
    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query = str(input('Command: '))
    
        
    return query
    



    
def myCommand():
  
    m = sr.Recognizer()                                                                                  
    with sr.Microphone() as source:                                                                      
        print("Listening...")
        m.pause_threshold =  2
        audio = m.listen(source)
    
    try:
        query1 = m.recognize_google(audio, language='en-in')
        print('User: ' + query1 + '\n')
       
    except sr.UnknownValueError:
        speak('Sorry sir! I didn\'t get that! Try typing the command!')
        query1 = str(input('Command: '))
    return query1

def timer(rem,sec):
    notificator=ToastNotifier()
    notificator.show_toast("reminder",f"""alaram will go off in (sec) seconds,""",duration=sec)
    notificator.show_toast(f"reminder",rem,duration=sec)
    #speak(rem)
    
    frequency=2500
    duration=1000
    winsound.Beep(frequency,duration)
    speak("you have "+rem+"sir")

def translation(info,des):
    translator=Translator()
    translated_sentance=translator.translate(info,dest=des)
    try:
        print(translated_sentance.pronunciation)
        speak(translated_sentance.pronunciation)
        print(translated_sentance.text)
    except Exception as e:
        print(e)
        
        
api_dict={"business":"https://newsapi.org/v2/top-headlines?country=in&category=business&apiKey=e2f54a69ba8b40108d5ff9713d935bf5","entertainmeant":"https://newsapi.org/v2/top-headlines?country=in&category=entertainment&apiKey=e2f54a69ba8b40108d5ff9713d935bf5","health":"https://newsapi.org/v2/top-headlines?country=in&category=health&apiKey=e2f54a69ba8b40108d5ff9713d935bf5","sports":"https://newsapi.org/v2/top-headlines?country=in&category=sports&apiKey=e2f54a69ba8b40108d5ff9713d935bf5","technology":"https://newsapi.org/v2/top-headlines?country=in&category=technology&apiKey=e2f54a69ba8b40108d5ff9713d935bf5"}


def  search_web(input):
    driver=webdriver.firefox()
    driver.implicitly_wait(1)
    driver.maximize_window()
    
    if 'youtube' in input.lower():
        speak('opening in youtube sir')
        indx=input.lower().split.index('youtube')
        query1=input.split()[indx+1:]
        driver.get("http://www.youtube.com/results?search_query1="+'+'.join(query1))
        return
    elif 'wikipedia' in input.lower():
        speak('opening wikipedia sir')
        indx=input.lower().split.index('wikipedia')
        query1=input.split()[indx+1:]
        driver.get("https://en.wikipedia.org/wiki/"+'+'.join(query1))
        return
    elif 'search' in input:
        
        indx=input.lower().split.index('google')
        query1=input.split()[indx+1:]
        driver.get("http://www.google.com/search?q="+'+'.join(query1))
        return
    else:
        driver.get("http://www.google.com/search?q="+'+'.join(input.split()))
    return

def time():
    #currenth=int(datetime.datetime.now().hour)
    #currentm=int(datetime.datetime.now().minutes)
   # currents=int(datetime.datetime.now().seconds)
    now = datetime.now()

    #current_time = now.strftime("%H hours: %M minutes: %S seconds:")
    current_time=now.strftime("%Y/%m/%d %I hours:%M minutes:%S seconds")
    print("Current Time =", current_time)
    speak(current_time)
    #print(currenth+":"+currentm+":"+currents)
    #speak(currenth+":"+currentm+":"+currents)
    return

if __name__ == "__main__":
     
        query = jarvis();
        query = query.lower()
        if 'jarvis' in query:
            now=datetime.now()
            currentH = int(now.strftime("%H"))
            if currentH >= 0 and currentH < 12:
                speak('Good Morning sir !')
                speak('Hello Sir, I am your Jarvis!')
                speak('How may I help you?')
            
            if currentH >= 12 and currentH < 18:
                speak('Good Afternoon sir!')
                speak('Hello Sir, I am your Jarvis!')
                speak('How may I help you?')
                
            if currentH >= 18 and currentH !=0:
                speak('Good Evening sir!')
                speak('Hello Sir, I am your Jarvis!')
                speak('How may I help you?')
       
   

while True:
            
                
           
                
        query1 = myCommand();
        query1 = query1.lower()
        res=chatbot_response(query1)
        
     
        if 'time' in res:
            time()
        elif 'tell me a joke' in res:
            a=(pyjokes.get_joke(language='en',category='all'))
            speak(a)
        elif'current weather'in res:
            speak("which city weather do you want sir:")
            location=myCommand()
            complete_api_link="https://api.openweathermap.org/data/2.5/weather?q="+location+"&appid="+"197c27a3af25f0ae87edfae1889332a4"
            api_link=requests.get(complete_api_link)
            api_data=api_link.json()
            if api_data['cod']=="404":
                print("invalid city:{},please check your city name".format(location))
            else:
                temp_city=((api_data['main']['temp'])-273.15)
                weather_desc=api_data['weather'][0]['description']
                hmdt=api_data['main']['humidity']
                wind_spd=api_data['wind']['speed']
                #date_time=datetime.now().strftime("%d %b %Y  %I:%M:%S %P")
                now=datetime.now()
                date_time=now.strftime("%m-%d-%Y %T:%M%p")
                
                
                print(".................")
                speak("weather stats for-{} || {}".format(location.upper(),date_time))
                speak("current temp is:{:.2f}deg C".format(temp_city))
                speak("current weather desc:"+weather_desc)
                speak("current humidity :{}".format(hmdt,'%'))
                speak("current wind speed:{}".format(wind_spd,'kmph'))
                
        elif 'reminder' in res:
           
                speak("what should i remind you sir:")
                words=myCommand()
                speak("after how much time i should remember you sir:")
                int 
                sec=int(myCommand())
                timer(words,sec)
            
        
        elif 'news'in res:
    
                    content=None
                    url=None
                    speak("which field do you want sir?")
                    field=myCommand()
                    for key,value in api_dict.items():
                        if key.lower() in field.lower():
                            url=value
                            print(url)
                            print("url found")
                            break
                        else:
                            url=True
                    if url is True:
                        print("url not found")
                        
                    lang_dict={"english":"en","hindi":"hi","telugu":"te"}
                    lang=None
                    speak("which language news do u want sir?")
                    lang_in=myCommand()
                    for key,value in lang_dict.items():
                        if key.lower() in lang_in.lower():
                            lang=value
                            print(lang)
                            print("lang found")
                            break
                        else:
                            lang=True
                    if lang is True:
                        print("lang not found")
                    
                    news=requests.get(url).text
                    
                    news=json.loads(news)
                    speak("hear is the first news:")
                    arts=news['articles']
                    for articles in arts:
                        article=articles ['title']
                        news_url=articles ['url']
                        if article is None:
                            continue
                        translation(article,lang)
                        print("for more info visit: (news_url)")
                    print("here the top news..thankyou!!!")
                    
        elif 'email' in res:
            speak('Who is the recipient? ')
            recipient = myCommand()

            if 'me' in recipient:
                try:
                    speak('What should I say? ')
                    content = myCommand()
       
                    server = smtplib.SMTP('smtp.gmail.com', 587)
                    server.ehlo()
                    server.starttls()
                    server.login("Your_Username", 'Your_Password')
                    server.sendmail('Your_Username', "Recipient_Username", content)
                    server.close()
                    speak('Email sent!')

                except:
                    speak('Sorry Sir! I am unable to send your message at this moment!')


        #elif 'nothing' in query1 or 'abort' in query1 or 'stop' in query1:
         #   speak('okay')
          #  speak('Bye Sir, have a good day.')
           # sys.exit()
          
                                   
           

       # else:
       #     query1 = query1
        #    speak('Searching...')
        #    try:
         #       try:
          #          res = client.query1(query1)
         #           results = next(res.results).text
         #           speak('WOLFRAM-ALPHA says - ')
         #           speak('Got it.')
         #           speak(results)
                   
         #       except:
         #           results = wikipedia.summary(query1, sentences=4)
         #           speak('Got it.')
          #          speak('WIKIPEDIA says - ')
         #           speak(results)
       #
        #    except:
         #       webbrowser.open('www.google.com')
         #       wikipedia.open('www.google.co.in')
                
        else:
           speak(res)
                
       
        speak('Next Command! Sir!')
        
        
        
