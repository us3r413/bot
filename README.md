# Ollama ChatBot

使用 Llama3.2 LLM 模型來製作麥當勞點餐助理，並且支援語音輸入及輸出。

## 安裝 & 使用方式

1.  下載專案
    ```bash
    git clone https://github.com/YuanOwO/LLM_ChatBot.git
    cd LLM_ChatBot
    ```
2.  確認已安裝 Python 3.12 以上版本
3.  確認已安裝 [Ollama](https://ollama.com/)、[FFmpeg](https://ffmpeg.org/)。
4.  安裝相依套件
    ```bash
    pip install -r requirements.txt
    ```
5.  設定環境變數
    ```bash
    mv .env.example .env
    ```
    將 `.env.example` 重新命名為 `.env`，並修改成適合的設定。
    其內容請參考下方的[參數設定](#參數設定)。
6.  執行程式
    ```bash
    python main.py
    ```

## 參數設定

我們可以透過修改 `.env` 檔案來設定程式的參數。

-   `OLLAMA_HOST`: Ollama 伺服器位置 (預設為 `localhost`)
-   `OLLAMA_PORT`: Ollama 伺服器連接埠 (預設為 `11434`)
-   `OLLAMA_MODEL`: Ollama 使用的模型名稱 (預設為 `llama-3.2`)
-   `PROMPT_FILE`: 模型運練時的提示檔案位置 (預設為 `data/prompt.md`)
-   `LANGUAGE`: 語音辨識及合成的語言 (預設為 `zh-TW`)
    可選擇任一 [Google Text-to-Speech 支援的語言](https://cloud.google.com/text-to-speech/docs/voices)，
    如 `zh-TW` (中文) 、 `en-US` (英文) 、 `ja` (日文) 等。
-   `INPUT_TYPE`: 輸入模式 (預設為 `speech`)
    可選擇 `text` (文字輸入) 或 `speech` (語音輸入)。
-   `SPEACH_SPEED`: 語音合成的速度 (預設為 `1.2`)
    可以是任意浮點數，數值越大速度越快，`1.0` 為原始速度。
-   `RECOGNIZER_ENERGY_THRESHOLD`: 語音辨識的能量閾值 (預設為 `1000`)
    表示語音辨識判定為有效語音和背景噪音的臨界值，
    可以是任意整數，數值越大能量閾值越高，語音辨識的靈敏度越低。
    不過在之後會根據環境聲音的大小來自動調整。
