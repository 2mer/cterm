from cterm2 import CTerm2
from bracket import Braqet

cterm = CTerm2()


class Loader:

    def __init__(self, width=10, color_enabled="cyan+ cyan", color_disabled="blue blue+", color_bracket="208 4", char_enabled=".", char_disabled="."):
        self.progress = 0
        self.width = width
        self.color_enabled = color_enabled
        self.color_disabled = color_disabled
        self.color_bracket = color_bracket
        self.char_enabled = char_enabled
        self.char_disabled = char_disabled

    def set_progress(self, float_progress):
        self.progress = float_progress
        return self

    def __call__(self, status="", color=""):

        cterm.remember()

        amt_enabled = int(self.width * self.progress)
        amt_disabled = int(self.width - amt_enabled)

        cterm("[", self.color_bracket)(self.char_enabled * amt_enabled, self.color_enabled)(self.char_disabled * amt_disabled, self.color_disabled)("]", self.color_bracket)

        if status:
            cterm(0)(status, color or "bold blue+")

        cterm(0)(endline="")

        cterm.jump()


if __name__ == "__main__":
    pass
    loader = Loader(20)
    loader2 = Loader(30, char_enabled="#", char_disabled="/")

    import time

    with Braqet("egg"):
        for i in range(0, 10):
            time.sleep(0.5)
            loader.set_progress(float(i + 1) / 10)(" hello world, i is [%d/10]" % (i + 1))
        cterm()

        with Braqet("egg"):
            for i in range(0, 10):
                time.sleep(0.5)
                loader2.set_progress(float(i + 1) / 10)(" hello world, i is [%d/10]" % (i + 1))
            cterm()
