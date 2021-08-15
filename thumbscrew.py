"""thumbscrew.py -- a fairly simple script that turns a json file into a series of thumnails for
youtube-related purposes.  Probably the best documentation is to view the example file."""

import json
from sys import argv
import sys
from PIL import Image, ImageDraw, ImageFont

def load_instructions(ufilename):
    """
    Expand this, maybe in the readme/docs because it's pretty much the heart and soul of the
    program.
    Loads a json file that describes the titlecard.  In general, it'll be pairings of json
    keys and values.  There are two keys that are handled specially; the 'background' key is
    drawn first and everything else is drawn on top of it with no specific order.  The two
    text-items will be for static text and ranges of information handled with a format string.

    if x or y is omitted from a caption, make it align center for that value"""

    return json.load(open(ufilename, 'r'))


def create_thumbnails(ujson):
    """Accepts a data structure created by json.load and turns it into a series of thumbnails
    based on the parameters."""

    # create the output image
    output = Image.new('RGB', tuple(ujson['dimensions']))

    # open the background image
    background = Image.open(ujson['background'])

    # resize the bg image to the output size
    resbg = background.resize(tuple(ujson['dimensions']))

    # paste the background into the original
    output.paste(resbg)

    # create a drawing context
    canvas = ImageDraw.Draw(output)

    # add captions
    for caption in ujson['captions']:
        # truetype also does opentype, so that's handy
        fnt = ImageFont.truetype(caption['font'], size=caption['size'])

        # if x or y is omitted, center the text along that axis
        if 'x' not in caption:
            p_x = (ujson['dimensions'][0] - fnt.getsize(caption['text'])[0]) / 2
        else:
            p_x = caption['x']

        if 'y' not in caption:
            p_y = (ujson['dimensions'][1] - fnt.getsize(caption['text'])[1]) / 2
        else:
            p_y = caption['y']

        canvas.text((p_x, p_y), caption['text'], tuple(caption['color']), fnt)

    # we mostly duplicate the caption function, but with a special attribute called text_list
    # which allows for a series of labels which will be used to create a series of files with
    # the label as the filename and the label writted to the file.
    # this is entirely for episode numbers :P
    if "labels" in ujson:
        for txt in ujson['labels']['text_list']:
            fnt = ImageFont.truetype(ujson['labels']['font'], size=ujson['labels']['size'])

            # the placing and drawing of labels should be in a loop that copies the already-drawn
            # picutre and writes to disk for each label
            if 'x' not in ujson['labels']:
                p_x = (ujson['dimensions'][0] - fnt.getsize(txt)[0]) / 2
            else:
                p_x = ujson['labels']['x']

            if 'y' not in ujson['labels']:
                p_y = (ujson['dimensions'][1] - fnt.getsize(txt)[1]) / 2
            else:
                p_y = ujson['labels']['y']

            # copy the image and create a drawing donctext
            card = output.copy()
            labelme = ImageDraw.Draw(card)

            # stamp it with the label
            labelme.text((p_x, p_y), txt, tuple(ujson['labels']['color']), fnt)

            # create a file and write it to disk
            # - note if you use illegal characters in text_list, bad things could happen
            card.save(open(txt + '.png', 'wb'))


if __name__ == '__main__':
    if len(argv) < 2:
        print('Usage: python %s file1 file2 file3' % argv[0])
        sys.exit(1)
    for project in argv[1:]:
        create_thumbnails(load_instructions(project))
