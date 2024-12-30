import ollama
from os import remove
import gtts
import time
from pydub import AudioSegment
import pydub.effects as ef
from pygame import mixer
import speech_recognition as sr
client = ollama.Client(host= 'http://localhost:11434') #test for llm
prompt_file = open('prompt.txt')
price_tag = prompt_file.read()
prompt_file.close()
mixer.init()
while(1):
    user_input = input();
    out = client.chat('llama3.2',messages=[
        {'role': 'system', 'content': price_tag}, 
        {'role': 'user', 'content': user_input},
    ])
    price_tag += out.message.content
    tts = gtts.gTTS(text= out.message.content, lang='en')
    tts.save('r1.mp3')
    edit = AudioSegment.from_mp3("r1.mp3")
    edit = ef.speedup(edit,1.20) 
    AudioSegment.export(edit,'r1.mp3','mp3')
    f = open('r1.mp3')
    mixer.music.load(f)
    mixer.music.play()
    print(out.message.content)
    while(mixer.music.get_busy()):
        time.sleep(0.1)
    f.close()
    remove('r1.mp3')