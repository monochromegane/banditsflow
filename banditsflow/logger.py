import os
from contextlib import redirect_stdout


class Logger:
    def __init__(self, mute: bool = False) -> None:
        self.mute = mute

    def log(self, log: str) -> None:
        if self.mute:
            with redirect_stdout(open(os.devnull, "w")):
                print(log)
        else:
            print(log)
