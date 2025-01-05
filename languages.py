from enum import Enum

"""
Language code for different languages.
Please refer to the following link for more information:
https://cloud.google.com/text-to-speech/docs/voices
"""


class Language(Enum):
    raise NotImplementedError("Please use the language code directly.")

    chinese = "zh-TW"  # 中文
    english = "en-US"  # 英文
    japanese = "ja"  # 日文
    korean = "ko"  # 韓文
    french = "fr-FR"  # 法文
    german = "de-DE"  # 德文
    italian = "it-IT"  # 義大利文
    spanish = "es-ES"  # 西班牙文
    portuguese = "pt-PT"  # 葡萄牙文
    russian = "ru"  # 俄文
    arabic = "ar-AE"  # 阿拉伯文
    dutch = "nl-NL"  # 荷蘭文
