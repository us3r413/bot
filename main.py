from dotenv import load_dotenv

load_dotenv()  # 從 .env 讀取環境變數

import os
import time
from os import environ

import ollama
import speech_recognition as sr
from gtts import gTTS
from pydub import AudioSegment, effects
from pygame import mixer
from speech_recognition.exceptions import UnknownValueError

from loader import Loader

####################################################################################################


# 初始化

HOST = f"http://{environ['OLLAMA_HOST']}:{environ['OLLAMA_PORT']}"
MODEL = environ.get("MODEL", "llama3.2")
PROMPT_FILENAME = environ.get("PROMPT_FILE", "prompt.txt")
LANG = environ.get("LANGUAGE", "zh-TW")
SPEECH_SPEED = float(environ.get("SPEECH_SPEED", 1.25))
RECOGNIZER_ENERGY_THRESHOLD = float(environ.get("RECOGNIZER_ENERGY_THRESHOLD", 1000))

input_type = environ.get("INPUT_TYPE", "speech")
if input_type in ["speech", "voice", "audio", "mic"]:
    VOICE_INPUT = True
elif input_type in ["text", "keyboard", "typing"]:
    VOICE_INPUT = False
else:
    raise ValueError(f"未知的輸入類型: {input_type}")
del input_type


client = ollama.Client(host=HOST)  # 連接 Ollama (預設為本地端的，不需要網路)

history = []  # 對話紀錄

# 讀取 prompt
with open(PROMPT_FILENAME, "r", encoding="utf-8") as f:
    history.append({"role": "system", "content": f.read()})

# recognizer 初始化
recognizer = sr.Recognizer()
recognizer.energy_threshold = RECOGNIZER_ENERGY_THRESHOLD  # 設定識別音量的閾值
recognizer.dynamic_energy_threshold = True  # 自動調整閾值

# mixer 初始化
mixer.init()

# 快取資料夾
os.makedirs(".cache", exist_ok=True)


####################################################################################################


def play_audio(file: str) -> None:
    """
    播放音檔，並等待播放完畢，按下 Ctrl+C 可中斷播放。

    Args:
        file (str): 音檔路徑

    Raises:
        FileNotFoundError: 找不到音檔
    """
    if not os.path.exists(file) or not os.path.isfile(file):
        raise FileNotFoundError(f"找不到音檔: {file}")

    mixer.music.load(file)
    mixer.music.play()

    try:
        # 阻塞直到播放完畢
        while mixer.music.get_busy():
            time.sleep(0.1)
    except KeyboardInterrupt:
        # 中斷播放
        mixer.music.stop()

    mixer.music.unload()


def text_to_speech(text: str, lang: str = "zh-TW") -> None:
    """
    文字轉語音 (Text-to-Speech)

    Args:
        text (str): 要轉換的文字
        lang (str): 語言代碼 (預設為 zh-TW)
    """
    file = ".cache/tts.mp3"

    # 儲存語音檔
    tts = gTTS(text=text, lang=lang)
    tts.save(file)

    # 加速語音檔
    edit = AudioSegment.from_mp3(file)
    edit = effects.speedup(edit, SPEECH_SPEED)
    AudioSegment.export(edit, file, "mp3")

    play_audio(file)


def raw_stt(lang: str) -> str:
    """
    錄音轉文字 (Speech-to-Text)

    Args:
        lang (str): 語言代碼

    Returns:
        str: 轉換後的文字

    Raises:
        UnknownValueError: 無法辨識語音
    """
    with sr.Microphone() as mic:
        recognizer.adjust_for_ambient_noise(mic, duration=1)  # 自動調整噪音水平
        with Loader("聆聽中", prefix=">> ") as loader:
            audio = recognizer.listen(mic)

            with open(".cache/input.wav", "wb") as f:
                f.write(audio.get_wav_data())

            # needs internet to access google's service
            content = recognizer.recognize_google(audio, language=lang)

    return content


def speech_to_text(lang: str = "zh-TW", retry: bool = True) -> str:
    """
    錄音轉文字 (Speech-to-Text)

    Args:
        lang (str): 語言代碼 (預設為 zh-TW)
        retry (bool): 若無法辨識語音時，是否重試 (預設為 True)

    Returns:
        str: 轉換後的文字

    Raises:
        UnknownValueError: 無法辨識語音 (若 retry 為 False)
    """
    if retry:
        while True:
            try:
                content = raw_stt(lang)
                break
            except UnknownValueError:
                print("無法辨識，請您再說一次。", end="\r")
                play_audio("data/unknown.mp3")
    else:
        content = raw_stt(lang)
    return content


def chat(user_input: str, model: str = MODEL) -> str:
    """
    跟 Ollama 對話

    Args:
        user_input (str): 使用者輸入的文字
        model (str): 使用的模型 (預設為 llama3.2)

    Returns:
        str: Ollama 回應的文字
    """

    with Loader("Ollama 思考中") as loader:
        history.append({"role": "user", "content": user_input})

        # 生成回應
        response = client.chat(model, messages=history)

        history.append(response.message)

    return response.message.content


####################################################################################################


if __name__ == "__main__":
    print("請開始對話，按 Ctrl+C 結束對話")
    print("使用語言:", LANG)
    # play_audio("data/welcome.mp3")
    # text_to_speech(LANG, "zh-TW")
    print("-" * 40)

    while True:
        try:
            if VOICE_INPUT:  # 使用語音輸入
                text = speech_to_text(LANG)
                print(text)
            else:  # 使用文字輸入
                text = input(">> ")

            # Ollama 回應
            response = chat(text)
            print(response)
            text_to_speech(response, LANG)

        except KeyboardInterrupt:
            print("[結束對話]")
            play_audio("data/goodbye.mp3")
            break
