# asciieditor
Ascii-art editor with ansi colors in 
Tkinter (Python base)
Pygcurse (Pygame)

Can export in ansi and in custom format
Pygame version:
Development halted for now until I understand Pygame better
S to save, E to export (read with cat Mydrawing.txt as you can't change the name, make a backup before making another drawing)
Tkinter version:
Currently working on it

Notes:
I modified pygcurse so that it doesn't raise an error when sent an unicode in putchar because I don't understand well how to use it.
It works in python2 because pygame...
Python3 using Tkinter
Once I have a better understanding of what I want to do, I should be able to have a font-end for both