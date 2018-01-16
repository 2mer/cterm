# coding=utf-8
from cterm2 import CTerm2
import time

cterm = CTerm2()


class Bracket:
    """
    @p Creates a bracket around cterm prints within its __enter__ to __exit__
    """

    def __init__(self, label, color="blue+ blue", end_label="", draw_line=True):
        self.label = label
        self.color = color
        self.end_label = end_label
        self.draw_line = draw_line

    def __enter__(self):
        self.time_start = time.time()
        cterm(("┏━" if self.draw_line else "  ") + self.label, self.color)(-1)()
        cterm.add_start(cterm("┃" if self.draw_line else " ", self.color)(-1)(" ").get_string())
        cterm()

    def __exit__(self, t, value, traceback):
        cterm()

        cterm.pop_start()

        cterm(("┗━" if self.draw_line else "  ") + self.end_label, self.color)(-1)()


class Braqet(Bracket):

    def __init__(self, label, color="blue+ blue", draw_line=True):
        Bracket.__init__(self, label, color, ("━" if draw_line else " ") * len(label), draw_line)


class Timer(Bracket):
    """
    @p A bracket that prints the delta time between its __enter__ and __exit__
    """
    _stats = {}

    def __enter__(self):
        self.time_start = time.time()

        Bracket.__enter__(self)

    def __exit__(self, t, value, traceback):
        delta = time.time() - self.time_start

        if self.label not in Timer._stats:
            Timer._stats[self.label] = []

        Timer._stats[self.label].append(delta)

        self.end_label += "\xE2\x96\xB3t = " + str(delta)

        Bracket.__exit__(self, t, value, traceback)

    @staticmethod
    def stats():
        """
        @p Prints averages of labeled timings
        """
        stats_string = ""

        for k, v in Timer._stats.items():
            stats_string += "---" + k + "---\n"

            avg_delta = 0

            for i in v:
                avg_delta += i

            avg_delta = avg_delta / len(v)

            stats_string += "avg: " + str(avg_delta) + "\n\n"

        cterm(color="bold blue+")[stats_string[:-2], "stats"](-1)()

    @staticmethod
    def clear_stats():
        """
        @p Clears the stats
        """
        Timer._stats = {}


if __name__ == "__main__":

    with Braqet("Braqet 1"):

        with Bracket("Test 1"):
            cterm("hello world!")()

        with Timer("Time 1", "green+", draw_line=True, end_label="woowoo waawaa "):

            with Bracket("Test 2"):
                cterm("hello world!")()

                with Bracket("Test 3"):
                    cterm("hello world!")()
