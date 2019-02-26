from PIL import Image
from PIL import ExifTags
import sys
import os
import re

# create empty lists
exifData = {}
list = {}
index = 0
count = 0

# scan folder for jpg
path = sys.argv[1]
files = os.listdir(path)
files = [ f for f in files if re.search('.jpg$', f, re.I)]

# open files and get exif data
for filename in files:
  try:
      print(">>>" , filename)
      img=Image.open(filename)
  except:
      print("'%s': Cannot open for reading.\n" % filename)
      continue
  
  # get exif raw data
  exifDataRaw = img._getexif()

  # close image
  img.close()

  for tag, value in exifDataRaw.items():
    try:
      decodedTag = ExifTags.TAGS.get(tag, tag)
      exifData[decodedTag] = value
    except:
      print("No exif Data for %s" , filename)
      continue

  date = exifData['DateTimeOriginal']
  key = str(date)
  list[key] = filename

# get number of files in list
count = len(list)

# corresponding to the list, set the leading zero fpr the index counter
if count > 100:
  count = 3
elif count > 10:
  count = 2
else:
  count = 1

datestamps = list.keys()
datestamps = sorted(datestamps)

# build new file name
for datestamp in datestamps:
  index = index + 1
  # Get the file extension
  file_ext = os.path.splitext(list[datestamp])[1]
  
  # delete time value
  aux_datestamp = str(datestamp[:-9])
  newName = [item.replace(':' , '') for item in aux_datestamp]
  newName = ''.join(str(e) for e in newName)
  
  # add leading zeros to index counter number
  index_string = str(index).zfill(count)
  newName = str(newName) + "_" + sys.argv[2] + "_" + "%s" % (index_string) + file_ext

  # rename file
  try:
    os.rename(list[datestamp], newName)
    print(list[datestamp] + ' -> ' + newName)
  except:
    print('%s: Could not rename' % list[datestamp])


