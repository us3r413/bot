import shutil
import subprocess

from PIL import Image, ImageDraw, ImageFont

PLAY = True
COLOR_MODE = "256fgbg"

"""
生成 gif 檔案，並播放在終端機上
依賴於 [gif-for-cli](https://github.com/google/gif-for-cli) 套件
"""

font_path = ".fonts/Cubic-11-1.430/fonts/ttf/Cubic_11.ttf"
# font_path = ".fonts/Noto_Sans_TC/static/NotoSansTC-Regular.ttf"

w, h = 320, 180

font = ImageFont.truetype(font_path, 48, encoding="utf-8")

imgs = [Image.new("RGB", (w, h), color="black") for _ in range(4)]

for i, img in enumerate(imgs):
    draw = ImageDraw.Draw(img)
    draw.text((w // 2, h // 2), "聆聽中" + "." * i + " " * (4 - i), font=font, fill="white", anchor="mm")

imgs[0].save("test.gif", save_all=True, append_images=imgs[1:], duration=200, loop=0)


##################################################


col, row = shutil.get_terminal_size()
args = [
    "gif-for-cli",
    f"--display-mode={COLOR_MODE}",
    "--rows",
    str(row - 1),
    "--cols",
    str(col - 1),
    "-l",
    "0",
    "test.gif",
]

if PLAY:
    try:
        subprocess.run(args)
    except KeyboardInterrupt:
        print("\033[2J\033[1;1H")


# from gif_for_cli.execute import execute

# if __name__ == "__main__":
#     execute(os.environ, args[1:], sys.stdout)
