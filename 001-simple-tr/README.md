001 - Simple Tr
===============

This program came about for a real reason, I use a website builder tool and
I have to manually take a space-separated string and put dashes
between the spaces to convert the title of a page to a valid file
name.

I figured that I may as well make the string separation and string
joining characters parameterised. So we have the following
specification:

# Program Spec

Create a program which accepts:
* a string of 255 characters
* a separation regular expression to detect (default: \s+)
* a joining character to replace the separation with (default: -)

Upon hitting the submit button, the program provides a version of the
string with any detected separations replaced with the joined
character.
