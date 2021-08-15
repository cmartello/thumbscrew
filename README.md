# Thumbscrew

This is a fairly simple script that allows you to define a thumbnail (or series thereof) using a 
fairly easy to understand JSON file.  It exists entirely because I got tired of doing the same
series of inputs in GIMP (or God forbid, Krita) and let's face it, repetitive is work is for the
machines.  So I made a solution and generalized it. 

## Usage

`python thumbscrew.py file1.json file2.json ...`

## Installation

There isn't, to speak of, it's just a script.  It depends on PIL and only runs on Python 3.

## JSON files

The included example file should pretty well explain how the program makes its decisions -- and
since the code is barely 100 lines long even with comments/docstrings, so it should be fairly 
easy to understand.  Even so...

The top-level of the JSON file is expected to be a dictionary with four keys: background,
dimensions, captions, and labels.

The background key must have a string that points to an image file.  Note that currently,
the program doesn't do any checks to make sure that you specified the directory correctly for your
operating system.  The specified background is what all of your text is going to be splatted onto.

'dimensions' must be a two-element array containing the width and then the height of the planned
output image.  The image specified in the background value will be scaled to this size.

'captions' is a list of labels that will be applied to each output image.  Each item in the list
is a dictionary with the following keys: "font", "text", "size", "x", "y", and a list of colors
(red, green, blue.)  Font and text are both strings, where font points to a specific font file
(like background, probably needs to be in the same directory) and text is the actual text written
to the output file.  X and Y are the upper-left position of the text, and if either X or Y is
omitted, the text will be centered on that axis.  Omit both to center the text on the screen.

The 'labels' key is a special case; instead of a text field, it uses a 'text_list' field, which
contains a list of labels for each file.  This is where episode numbers effectively go.  Note that
filenames will be generated from these strings, and the program will have a problem if you attempt
to use a prohibited character in a filename.  Otherwise, 'labels' functions almost exactly the 
same as 'captions.'
