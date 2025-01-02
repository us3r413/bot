from itertools import cycle
from shutil import get_terminal_size
from threading import Thread
from time import sleep

"""
讓載入時有更有趣的效果

code from:
https://stackoverflow.com/questions/22029562
"""


class Loader:
    def __init__(self, desc="Loading...", end=None, prefix="", timeout=0.1):
        """
        A loader-like context manager

        Args:
            desc (str, optional): The loader's description. Defaults to "Loading...".
            end (str, optional): Final print. Defaults to "Done!".
            timeout (float, optional): Sleep time between prints. Defaults to 0.1.
        """
        self.desc = desc
        self.end = end
        self.prefix = prefix
        self.timeout = timeout

        self._thread = Thread(target=self._animate, daemon=True)
        self.steps = ["⢿", "⣻", "⣽", "⣾", "⣷", "⣯", "⣟", "⡿"]
        self.done = False

    def start(self):
        self._thread.start()
        return self

    def _animate(self):
        for i, c in cycle(enumerate(self.steps)):
            if self.done:
                break
            dots = "." * (i // 2 % 4)
            print(f"\r\033[0J{self.prefix}\033[32m{c}\033[0m {self.desc}{dots}", flush=True, end="")
            sleep(self.timeout)

    def __enter__(self):
        self.start()

    def stop(self):
        self.done = True
        if self.end == None:
            print(f"\r\033[0J{self.prefix}", flush=True, end="")
            # print(f"\r\033[0J{self.prefix}\033[32m⣿\033[0m {self.desc}...", flush=True)
            return
        cols = get_terminal_size((80, 20)).columns
        print("\r" + " " * cols, end="", flush=True)
        print(f"\r{self.end}", flush=True)

    def __exit__(self, exc_type, exc_value, tb):
        # handle exceptions with those variables ^
        self.stop()


if __name__ == "__main__":
    with Loader("Loading with context manager..."):
        for i in range(10):
            sleep(0.25)

    loader = Loader("Loading with object...", "That was fast!", 0.05).start()
    for i in range(10):
        sleep(0.25)
    loader.stop()
