import sys

from PIL import Image
from random import shuffle

def unshred(shred_count):

  image = Image.open('sample_shredded.png')
  data = image.getdata() # This gets pixel data

  # Access an arbitrary pixel. Data is stored as a 2d array where rows are
  # sequential. Each element in the array is a RGBA tuple (red, green, blue,
  # alpha).

  width, height = image.size
  left_match = range(shred_count) # Index of best mach for strip's left hand side
  right_match = range(shred_count) # Index of best mach for strip's right hand side

  # Create a new image of the same size as the original
  # and copy a region into the new image
  unshredded = Image.new('RGBA', image.size)
  shred_width = unshredded.size[0] / shred_count

  def pixel_value(x, y):
    data = image.getdata() # This gets pixel data
    pixel = data[y * width + x]
    return pixel

  def pixel_in_shred(x, y, shred):
    x1, y1 = x + (shred * shred_width), 0
    x2, y2 = x1 + shred_width, height
    column = Image.new('RGBA', (shred_width, height))
    column = image.crop((x1, y1, x2, y2))
    data = column.getdata()
    pixel = data[y * shred_width + x]
    return pixel

  def avg(int1, int2):
    return (int1 + int2) / 2
  # Are two pixel columns similar?
  end = shred_width - 1
  def difference(left_strip, right_strip): # Shred indices
    deltaR = 0
    deltaG = 0
    deltaB = 0
    differentness = sys.maxint - 1
    if left_strip and right_strip:
      for i in range(height):
        r1, g1, b1, a1 = pixel_in_shred(end, i, left_strip)
        r2, g2, b2, a2 = pixel_in_shred(0, i, right_strip)
        r1a, g1a, b1a, a1a = pixel_in_shred(end - 1, i, left_strip)
        r2a, g2a, b2a, a2a = pixel_in_shred(1, i, right_strip)
        deltaR += abs(avg(r1, r1a) - avg(r2, r2a))
        deltaR += abs(avg(g1, g1a) - avg(g2, g2a))
        deltaR += abs(avg(b1, b1a) - avg(b2, b2a))
      differentness = deltaR + deltaG + deltaB
    print differentness
    return differentness

  for i in range(shred_count):
    left_match[i] = (i - 1) % shred_count
    right_match[i] = (i + 1) % shred_count
    #print 'Created empty lefts and rights for shred %s' % i

  for i in range(shred_count):
    for j in range(shred_count):
      if i != j:
        if difference(j, i) < difference(left_match[i], i):
          left_match[i] = j
        if difference(i, j) < difference(i, right_match[i]):
          right_match[i] = j
      print 'Compared shred %s with shred %s' % (i, j)

  # Create shreds as their own images
  original_shreds = []
  for i in range(shred_count):
    x1, y1 = shred_width * i, 0
    x2, y2 = x1 + shred_width, height
    source_region = Image.new('RGBA', (shred_width, height))
    source_region = image.crop((x1, y1, x2, y2))
    original_shreds.append(source_region)

  # Order the shreds by alignment
  out_shreds = []
  inserted = [False for x in range(shred_count)]
  for i in range(shred_count):
    if not inserted[left_match[i]]:
      out_shreds.append(original_shreds[left_match[i]])
      inserted[left_match[i]] = True
    if not inserted[i]:
      out_shreds.append(original_shreds[i])
      inserted[i] = True
    if not inserted[right_match[i]]:
      out_shreds.append(original_shreds[right_match[i]])
      inserted[right_match[i]] = True

  # Paste the shreds into an output image
  for i in range(shred_count):
    source_region = out_shreds[i]
    destination_point = (shred_width * i, 0)
    unshredded.paste(source_region, destination_point)

  # Output the new image
  unshredded.save('sample_unshredded.png')
  print 'Done'


if __name__ == '__main__':
  shred_count = 10
  try:
    shred_count = int(sys.argv[1])
  except:
    # Ignore
    pass
  unshred(shred_count)
