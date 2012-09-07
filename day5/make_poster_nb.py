size(21*cm, 29.7*cm)
from glob import glob
from math import ceil

fnames = glob('thumbs/*.jpg')

CELL_SIZE = 10
IMAGE_SIZE = CELL_SIZE * 10
IMAGE_OFFSET = -25

ROW_HEIGHT = 5

rows = 200
cols = int(ceil(HEIGHT / CELL_SIZE) + 1)

def shuffled(l):
    from random import shuffle
    new_list = list(l)
    shuffle(new_list)
    return new_list

for y in range(rows):
    fname = choice(fnames)
    for x in range(cols):
        image(fname, x * CELL_SIZE, y*ROW_HEIGHT, width=IMAGE_SIZE, height=IMAGE_SIZE)