import os
from os.path import splitext, join, basename
from glob import glob

from PIL import Image

def create_resized(fname, target_fname, maxwidth=None, maxheight=None):
    """Resize an image up to the maximum width and height.
    Will only scale images down, not enlarge them.
    - fname: original file name
    - target_fname: name of the new file to create
    - maxwidth: maximum width of the new image
    - maxheight: maximum height of the new image
    """
    try:
        img = Image.open(fname)
        format = img.format
        resized_img = universal_resize(img, maxwidth, maxheight)
        resized_img.save(target_fname, format)
    except IOError:
        pass

def universal_resize(img, maxwidth, maxheight):
    """Given a target PIL image, returns a resized version up to the maximum width and height.
    Will only scale images down, not enlarge them.
    - img: original image
    - maxwidth: maximum width of the new image
    - maxheight: maximum height of the new image
    """
    width, height = img.size
    new_width, new_height = size_for(width, height, maxwidth, maxheight)
    resized_img = img.resize( (new_width, new_height), Image.ANTIALIAS )
    return resized_img

def create_cropped(fname, target_fname, target_width, target_height):
    """Crop an image to the specified target width/height.
    The new image is guaranteed to have the specified width/height.
    This algorithm will select a part out of the middle of the image.
    - fname: original file name
    - target_fname: name of the new file to create
    - maxwidth: target width of the new image
    - maxheight: target height of the new image
    """
    try:
        img = Image.open(fname)
        format = img.format
        cropped_img = universal_crop(img, target_width, target_height)
        cropped_img.save(target_fname, format)
    except IOError:
        pass

def universal_crop(img, target_width, target_height):
    """Given a target PIL image, returns a cropped version of the specified target width/height.
    Returned images are guaranteed to have the specified width/height.
    This algorithm will select a part out of the middle of the image.
    - img: original image
    - maxwidth: target width of the new image
    - maxheight: target height of the new image
    """
    width, height = img.size    
    if float(width) / target_width > float(height) / target_height:
        scale = float(target_height) / height
        new_width, new_height = int(width * scale), int(height * scale)
        target_img = img.resize( (new_width, new_height), Image.ANTIALIAS )
        dx = (new_width - target_width) / 2
        target_img = target_img.crop( (dx, 0, dx + target_width, target_height) )
    else:
        scale = float(target_width) / width
        new_width, new_height = int(width * scale), int(height * scale)
        target_img = img.resize( (new_width, new_height), Image.ANTIALIAS )
        dy = (new_height - target_height) / 2
        target_img = target_img.crop( (0, dy, target_width, dy + target_height) )
    return target_img
    
def size_for(width, height, maxwidth=None, maxheight=None):
    """Returns a new width and height pair that fall inside of the given maximum width/height.
    Note that if the given width and height are both smaller than maxwidth and maxheight,
    they are simply returned.
    """
    if maxheight is None or (maxwidth is not None and width > maxwidth and width > height):
        scale = float(maxwidth) / width
        return ( int(width * scale), int(height * scale) )
    elif maxwidth is None or (maxheight is not None and height > maxheight and height >= width):
        scale = float(maxheight) / height
        return ( int(width * scale), int(height * scale) )
    else:
        return width, height        

def check_size(fname, minwidth=None, minheight=None, maxwidth=None, maxheight=None):
    img = Image.open(fname)
    img_width, img_height = img.size
    if minwidth is not None and img_width < minwidth:
        return False
    if minheight is not None and img_height < minheight:
        return False
    if maxwidth is not None and img_width > maxwidth:
        return False
    if maxheight is not None and img_height > maxheight:
        return False
    return True
        
try:
    os.mkdir('thumbs')
except OSError:
    pass
fnames = glob('images/*')
for fname in fnames:
    target_fname = join('thumbs', basename(fname))
    print target_fname
    create_cropped(fname, target_fname, 500, 500)
