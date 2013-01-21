import sys

from PIL import Image
from random import shuffle

def unshred(shreds):
  image = Image.open('sample.png')
  shredded = Image.new('RGBA', image.size)
  width, height = image.size
  shred_width = width / shreds
  sequence = range(0, shreds)
  shuffle(sequence)

  for i, shred_index in enumerate(sequence):
    shred_x1, shred_y1 = shred_width * shred_index, 0
    shred_x2, shred_y2 = shred_x1 + shred_width, height
    region =image.crop((shred_x1, shred_y1, shred_x2, shred_y2))
    shredded.paste(region, (shred_width * i, 0))

    shredded.save('sample_shredded.png')

if __name__ == '__main__':
  shreds = 10
  try:
    shreds = int(sys.argv[1])
  except:
    # Ignore
    pass
  unshred(shreds)
