# coding=utf-8
import sys
import re


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class CTerm2:
    """
    @p
    This class is a wrapper for using color ANSI codes in the terminal

    @p
    a color string has its values seperated by a single space:
    bold_red = colors["bold red"]

    @p
    to create bright colors add aplus to the end of a color:
    bright_green = colors[green+]

    @p
    Notes:
        this class is of metaclass 'Singleton', meaning that this class has only one instance,
        when trying to create an instance, while one is already exist, the existing one will be returned
    """

    __metaclass__ = Singleton

    __styles = {
        # style
        "bold": "\033[1m",
        "underline": "\033[4m",
        "rapid_blink": "\033[6m",
    }

    __colors = {
        # color
        "black": "%d0",
        "red": "%d1",
        "green": "%d2",
        "yellow": "%d3",
        "blue": "%d4",
        "magenta": "%d5",
        "cyan": "%d6",
        "white": "%d7"
    }

    __fg_mod = 3
    __bg_mod = 4
    __bright_mod = 6
    __reset = "\033[0m"

    def __init__(self):
        pass

    def get_string(self):
        ret = self.__current_text
        # self.clear_all()
        self.__color_stack = []
        self.__current_text = ""
        return ret

    def __get_color(self, string):
        if string == "reset":
            return self.__reset

        items = string.split(" ")

        fg = None
        bg = None
        advanced = False

        color_str = ""

        for i in items:

            bright_flag = False

            if i[-1] == "+":
                bright_flag = True
                i = i[:-1]

            if i in self.__colors:

                bright = self.__bright_mod if bright_flag else 0

                if not fg:
                    fg = self.__colors[i] % (self.__fg_mod + bright)
                else:
                    bg = self.__colors[i] % (self.__bg_mod + bright)
            elif i in self.__styles:
                color_str += self.__styles[i]
            else:
                advanced = True
                if not fg:
                    fg = i
                else:
                    bg = i

        return color_str + ((("\033[38;5;%sm\033[48;5;%sm" if advanced else "\033[%s;%sm") % (fg, bg)) if bg else ("\033[38;5;%sm" if advanced else "\033[%sm") % fg)

    def color(self, color_string):
        color = self.__get_color(color_string)
        self.__color_stack.append(color)
        self.__current_text += color
        return self

    def pop_color(self):
        self.__color_stack.pop()
        self.__current_text += self.__color_stack[-1] if self.__color_stack else self.__reset
        return self

    def clear_style(self):
        self.__color_stack = []
        self.__current_text += self.__reset
        return self

    def clear_all(self):
        self.__color_stack = []
        self.__current_text = ""
        self.__start_stack = []

    def printc(self, obj=None, flush=True, endline="\n"):
        if obj:
            self.__current_text += str(obj)
        sys.stdout.write(("".join(self.__start_stack)) + self.__current_text + endline)
        self.__current_text = ""
        if flush:
            sys.stdout.flush()
        return self

    __start_stack = []

    def add_start(self, text):
        self.__start_stack.append(text)

    def pop_start(self):
        self.__start_stack.pop()

    __color_stack = []
    __current_text = ""

    # def __getitem__(self, item):
    #     if type(item) == str:
    #         self.__current_text += item
    #     if type(item) == tuple:
    #         self.color(item[0])
    #         if len(item) > 1:
    #             self.__current_text += item[1]
    #             if len(item) > 2:
    #                 if item[2] == -1:
    #                     self.__color_stack.pop()
    #                     self.__current_text += self.__color_stack[-1] if self.__color_stack else self.__reset
    #                 elif item[2] == 0:
    #                     self.__color_stack = []
    #                     self.__current_text += self.__reset
    #     elif type(item) == int:
    #         if item == -1:
    #             self.__color_stack.pop()
    #             self.__current_text += self.__color_stack[-1] if self.__color_stack else self.__reset
    #         elif item == 0:
    #             self.__color_stack = []
    #             self.__current_text += self.__reset
    #
    #     return self

    __char_tl = "┏"
    __char_t = "━"
    __char_tr = "┓"
    __char_l = "┃"
    __char_r = "┃"
    __char_bl = "┗"
    __char_b = "━"
    __char_br = "┛"

    def __getitem__(self, text):
        """
        Args:
            text (Union[str, tuple]): the text to put inside a box

        Returns:
            cterm (Cterm2): returns the object __getitem__ was called from, for further calling of object
        """
        if type(text) == str:
            text_split = text.split("\n")

            max_len = 0

            for t in text_split:
                max_len = max(max_len, len(t))

            new_string = self.__char_tl + (self.__char_t * (max_len + 2)) + self.__char_tr + "\n"

            for t in text_split:
                new_string += self.__char_l + " " + t + (" " * (max_len - len(t) + 1)) + self.__char_r + "\n"

            new_string += self.__char_bl + (self.__char_b * (max_len + 2)) + self.__char_br

            self.__current_text += new_string
        elif type(text) == tuple:
            text_split = text[0].split("\n")

            label = text[1]

            max_len = 0

            for t in text_split:
                max_len = max(max_len, len(t))

            new_string = self.__char_tl + (self.__char_t * (max_len + 2)) + self.__char_tr + "\n"

            new_string = label + new_string[(len(label) * 3):]

            for t in text_split:
                new_string += self.__char_l + " " + t + (" " * (max_len - len(t) + 1)) + self.__char_r + "\n"

            new_string += self.__char_bl + (self.__char_b * (max_len + 2)) + self.__char_br

            self.__current_text += new_string

        return self

    def __call__(self, text=None, color=None, flush=True, endline="\n"):
        """

        Args:
            text (Union[str, int]): if str: the text to be added to cterm, if int: 0: clear style, -1: pop last color
            color (str): the string color to wrap the text with

        Returns:
            cterm (Cterm2): returns the object __call__ was called from, for further calling of object
        """
        if text is None and color is None:
            self.printc(flush=flush, endline=endline)
        else:

            if color:
                self.color(color)

            if text is not None:

                if type(text) == int:

                    if text == -1:
                        self.pop_color()
                    elif text == 0:
                        self.clear_style()

                else:
                    self.__current_text += str(text)

            return self


if __name__ == "__main__":

    cterm = CTerm2()

    cterm.printc("Yo Yo Yo")
    cterm("hello world!")()

    # Note: the + sign will cause a color to be of the bright variant
    # ie: 'blue' is blue, and 'blue+' is bright blue

    # Note: the first color specified is the foreground, the second color specified is the background
    # ie: 'red' is foreground red, 'red green' is foreground red background green

    # Note color can also be also a numeric value from this table: https://en.wikipedia.org/wiki/ANSI_escape_code#collapsibleTable0
    # ..but this will NOT render in the JetBrains terminal (pycharm, idea ...)

    cterm(color="green")
    cterm("hello world")
    cterm()
    cterm.color("red")("hello world")()
    cterm("hello world", "yellow+ underline")(0)()

    # you can draw a box with [<text>]
    cterm(color="bold blue+")["""\
this is a test my reddit bros
im inside a boxxe
hello woooooooooooooooooooorld!!"""](0)()

    # this is how you dont use rects
    cterm(color="red")["hello"](color="green")["world"](color="blue")["my"](color="208")["reddit"](color="206")["bro"](0)()
    # label square
    cterm(color="208")["hello world\nthis\nis\nnuttya", "red+"]()

    cterm("%03d" % 20)()
    cterm("%03d" % 300)()

    import datetime

    cterm[str(datetime.time(20, 30) > datetime.time(34, 30))]()



