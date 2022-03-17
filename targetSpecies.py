# Take megaspecies.csv to get list of target species, get list of target species to become labels (STEP 1- list of target species names)
# Filter out non-target species, then filter to mD crop photos
#   So now we have just 1 megadetector detection
#       Cropped images (using MD boxes)
#           80/20 train/test split
import csv
import json
import numpy as np
import pandas as pd
from PIL import Image
# create virtual Env to install np

df = pd.read_csv('/home/compbio/GDrive/UWIN_Test_Dataset/MegaSpecies.csv', dtype = str) 
df = df[df.target == 'Target']
targetSpecies = df.loc[:, ['commonName','target']]
# use MC BQ to filter out rows with non-target species and numDetections != 1
df = pd.read_csv('/home/compbio/GDrive/UWIN_Test_Dataset/multicity-bigquery-export.csv', dtype = str) 
df['numAnimalDetections'] = pd.to_numeric(df['numAnimalDetections'])
df= df[df.commonName.isin(targetSpecies.loc[:]['commonName'])]
MCTargetSpeciesDetections = df[df['numAnimalDetections'] == 1]
# print(MCTargetSpeciesDetections.loc[:]['jsonAnimalDetection'])
#print(MCTargetSpeciesDetections.loc[: , ['commonName', 'numAnimalDetections']])
MCTargetSpeciesDetections.to_csv('MCTargetSpecies.csv')


allBboxStr = MCTargetSpeciesDetections.loc[:]['jsonAnimalDetection']
width = 3840 
height = 2160
def convertToPixels (ann):
    ann = eval(ann)
    ann['bbox'][0] = ann['bbox'][0] * width
    ann['bbox'][1] = ann['bbox'][1] * height
    ann['bbox'][2] = ann['bbox'][2] * width
    ann['bbox'][3] = ann['bbox'][3] * height
    return ann
MCTargetSpeciesDetections.loc[:, 'jsonAnimalDetection']  = MCTargetSpeciesDetections['jsonAnimalDetection'].apply(convertToPixels)
# MCTargetSpeciesDetections.to_csv('finalOutput.csv')
print(MCTargetSpeciesDetections.loc[:, 'jsonAnimalDetection'])


# loop over each row, call crop method and save output(cropped image) to cropped folder. save cropped file name as new column (croppedFilename - val is img/croppedFiles)
# use coordinates for left, right, top, bottom

# df = pd.read_csv('finalOutput.csv')
# create new folder called croppedFilename

# add new column to csv called croppedImage
# for each row, crop image
filename = []
for row in MCTargetSpeciesDetections:
    imgName = MCTargetSpeciesDetections.loc[row, 'photoName']
    coords = MCTargetSpeciesDetections.loc[row, 'jsonAnimalDetection']
    # open image from photoUpload
    im = Image.open(imgName)
    im = im.crop(coords[0], coords[1], coords[2], coords[3])
    image_path = '/home/compbio/GDrive/croppedOutput/' + imgName + '.jpg'
    im.save(image_path, 'JPEG')

    filename.append(image_path)
# create filename
# pass filename value into new column



MCTargetSpeciesDetections['croppedFilename'] = filename

MCTargetSpeciesDetections