# Name: Arul Nigam
# Period 3
# Date: 26 May 2020

import PIL
from PIL import Image
import urllib.request
import io, sys

print(PIL.__version__)
URL = 'http://www.w3schools.com/css/trolltunga.jpg' # URL = sys.argv[1]
f = io.BytesIO(urllib.request.urlopen(URL).read())  # Read image into memory
img = Image.open(f)
img.show()
img = Image.open(f)
print(img.size)  # Gives (width, height)
pix = img.load()  # Sets up access to the pixels of the image
print(pix[2, 5])  # Pixels are tuples, mostly

def chrome(color):
    if color < (255 // 3):
        return 0
    elif color > (255 // 3 * 2):
        return 255
    else:
        return 127

for x in range(img.size[0]):
    for y in range(img.size[1]):
        r, g, b = pix[x, y]
        pix[x, y] = chrome(r), chrome(g), chrome(b)
img.show()
