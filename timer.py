from cterm2 import CTerm2
import time

cterm = CTerm2()


class Timer:
    _stats = {}

    def __init__(self, label, color="blue+ blue"):
        self.label = label
        self.color = color

    def __enter__(self):
        self.time_start = time.time()
        cterm(self.label, self.color)(-1)()
        cterm.add_start(cterm(" ", self.color)(-1)(" ").get_string())
        cterm()

    def __exit__(self, t, value, traceback):
        delta = time.time() - self.time_start

        if self.label not in Timer._stats:
            Timer._stats[self.label] = []

        Timer._stats[self.label].append(delta)

        cterm()

        cterm.pop_start()

        cterm("\xE2\x96\xB3t = " + str(delta), self.color)(-1)()

        cterm()

    @staticmethod
    def stats():
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
        Timer._stats = {}


if __name__ == "__main__":

    with Timer("first", "white+ blue"):
        time.sleep(3)

        with Timer("second", "white+ green+"):
            time.sleep(2)

            with Timer("third", "white+ red"):
                time.sleep(1)

    Timer.stats()
    Timer.clear_stats()
