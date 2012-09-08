size(21*cm, 29.7*cm)
from glob import glob
from math import ceil

fnames = glob('thumbs/*')

ROW_HEIGHT = 10
TARGET_WIDTH = 100

rows = int(ceil(HEIGHT / ROW_HEIGHT )+ 1)
cols = int(ceil(WIDTH / TARGET_WIDTH) + 1)

background(0.1)

y=0
while y < HEIGHT:
    fname = choice(fnames)
    x=0
    while x < WIDTH:
        image(fname, x, y, width=TARGET_WIDTH, height=TARGET_WIDTH, alpha=1.0-(y/HEIGHT))
        x += TARGET_WIDTH
    y += TARGET_WIDTH
    TARGET_WIDTH = max(TARGET_WIDTH * 0.88, 5)
