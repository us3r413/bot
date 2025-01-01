import ollama
from os import remove,environ
environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import gtts
import time
from pydub import AudioSegment
import pydub.effects as ef
from pygame import mixer
import speech_recognition as sr


client = ollama.Client(host= 'http://localhost:11434') #local host, no need for internet
prompt_file = open('prompt.txt') #prompt read in
price_tag = prompt_file.read()
prompt_file.close()
recognizer = sr.Recognizer() #recognizer setup
mixer.init() #mixer setup


while(1):
    print("Recording...")
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic,duration=0.5) #speech to text
        audio = recognizer.listen(mic)
        user_input = recognizer.recognize_google(audio) #needs internet to access google's service
        print(user_input)
        price_tag+= "user:"+ user_input + '\n'
        
        
    out = client.chat('llama3.2',messages=[          #generate response
        {'role': 'system', 'content': price_tag}, 
        {'role': 'user', 'content': user_input},
    ])
    price_tag += "Bot:"+ out.message.content + '\n'
    tts = gtts.gTTS(text= out.message.content, lang='en')
    tts.save('r1.mp3')
    
    
    edit = AudioSegment.from_mp3("r1.mp3")          #speedup audio file
    edit = ef.speedup(edit,1.20) 
    AudioSegment.export(edit,'r1.mp3','mp3')
    
    
    f = open('r1.mp3')          #play audio file
    mixer.music.load(f)
    mixer.music.play()
    
    
    print(out.message.content)      #print out
    while(mixer.music.get_busy()):
        time.sleep(0.1)
    f.close()
    remove('r1.mp3')