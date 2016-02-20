# asciieditor
Ascii-art editor with ansi colors in Pygcurse (Pygame)
Can export in ansi and in custom format
S to save, E to export (read with cat Mydrawing.txt as you can't change the name, make a backup before making another drawing)

Notes:
I modified pygcurse so that it doesn't raise an error when sent an unicode in putchar because I don't understand well how to use it.
It works in python2 because pygame...
