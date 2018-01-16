# cterm
Python Terminal Color Singleton Wrapper

## Usage:

### initialization
```py
from cterm.cterm2 import CTerm2

# this fetches a singleton instance, meaning that if one was already created, the existing one will be give
# and a new 'CTerm2' object will not be created.
cterm = CTerm2()
```

### appending
appending data to cterm is done through the `__call__` command:
```py
cterm.__call__(...)
# or most commonly:
cterm(...)
```
to print text, you must first append it to the `CTerm2` object, we can do so by calling `__call__` with the first positional parameter `text` as a string:
```py
cterm("hello world!")
# or incase of clashing:
cterm(text="hello world")
```

after appending text, we now have to print it, we can do so by calling `__call__` with empty `text` and `color` parameters:
```py
cterm()
```

or as a whole:
```py
cterm("hello world")
cterm()

->"hello world\n"
```

but writing cterm every time is annoying, and because of that `__call__` returns `self` after executing, meaning you can chain `__call__`s:
```py
# dont forget to __call__ with empty text and color params to print
cterm("hello world ")("this will appear after hello world")()
```

`__call__` has another parameter - color, you can give the color parameter as follows:
```py
cterm("text goes here", "red")()
cterm(color="red")("text")()
cterm(color="green")
cterm("hello green!")()
```

Note: using a color adds the color to the color stack, you can pop a color to use the color below the last color, or clear the stack entirely and clear terminal color and style:
```py
cterm("this is red", "red")()
cterm("this is also red")()
# __call__ with text as -1 of type int will pop a color from the stack
cterm(-1)
cterm("this is now in terminal default)()
cterm("hello is blue", "blue")(" world is green", "green")(-1)(" and im blue again!")()

# __call__ with text as 0 of type int will clear the color and style stack
cterm("A", "red")("B", "green")("C", "blue")(0)(" this text is in terminal default")()
```

### color
selecting color is done in the following string format:
```py
"item1 item2 item3"
```

when choosing a color the selector expects one or two color items, the first is the foreground, while the second is the background:
```py
"red green"
# red foreground, green background
```
the allowed colors are:
+ black
+ red
+ green
+ yellow
+ blue
+ magenta
+ cyan

and their 'bright' variant:
+ black+
+ red+
+ green+
+ yellow+
+ blue+
+ magenta+
+ cyan+

if you want to use more diverse colors, you can also give a value from 0 to 255, as seen here [https://en.wikipedia.org/wiki/ANSI_escape_code#mw-headline]

ie:
```py
"112 208"
```

### misc
you can also use the following to draw a box around text:
```py
cterm(color="red")["this is rendered inside a box!"]()
cterm(color="red")["this box is labeled!", "label"]()

# or for multiline
cterm["""\
Hello
World!!
"""]()
```
## Bracket
the `Bracket` class uses features given in `CTerm2` and wraps them nicely with the `__enter__` and `__exit__` magic methods

### usage
```py
with Bracket("label 1"):
  cterm("Hello world!")()
  
with Bracket("label 2", "red+ red", draw_line=False):
  cterm("Hello world!")()

  with Bracket("label 3", "green+", end_label="end label 3"):
    cterm("Hello world!")()
```

### Braqet
draws a bracket with equally sized ends
```py
with Braqet("label 1"):
  cterm("Hello world!")()
```

### Timer
draws a bracket, and prints the delta time it took between the `__enter__` and `__exit__` of the timer
```py
with Timer("label 1"):
  cterm("Hello world!")()
```
