# Take megaspecies.csv to get list of target species, get list of target species to become labels (STEP 1- list of target species names)
# Filter out non-target species, then filter to mD crop photos
#   So now we have just 1 megadetector detection
#       Cropped images (using MD boxes)
#           80/20 train/test split
from audioop import ulaw2lin
import os
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
height = 2880
# height = 2160
# width, height = im.size
# print(width, height)
def convertToPixels (ann):
    ann = eval(ann)
    width = 3840 
    height = 2880

    ann['bbox'][0] = ann['bbox'][0] * width
    ann['bbox'][1] = ann['bbox'][1] * height
    ann['bbox'][2] = ann['bbox'][2] * width
    ann['bbox'][3] = ann['bbox'][3] * height
    return ann
MCTargetSpeciesDetections.loc[:, 'jsonAnimalDetection']  = MCTargetSpeciesDetections['jsonAnimalDetection'].apply(convertToPixels)


filename = []
MCTargetSpeciesDetections.reset_index()
imgName = MCTargetSpeciesDetections.loc[:]['photoName']
coords = MCTargetSpeciesDetections.loc[:]['jsonAnimalDetection']


im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/first_upload/VID626-00000.jpg')
countImg=0
for image in imgName:
    if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/first_upload/'+ image):
        im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/first_upload/' + image)
    if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/second_upload'+ image):
        im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/second_upload/' + image)
    if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/third_upload'+ image):
        im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/third_upload/' + image)
    if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/fourth_upload/' + image):
        im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/fourth_upload/' + image)
    
    truewidth, trueheight = im.size
    if (truewidth != width  and trueheight != height):
        continue

    ulx = coords.iloc[countImg]['bbox'][0]
    uly = coords.iloc[countImg]['bbox'][1]
    pwidth = coords.iloc[countImg]['bbox'][2]
    pheight = coords.iloc[countImg]['bbox'][3]

    crop_img = im.crop((ulx, uly, ulx+pwidth, uly+pheight))
    image_path = '/home/compbio/GDrive/croppedOutput/' + image
    crop_img.save(image_path, 'JPEG')
    print('saved image path = ', image_path, '\ncoords', ulx, uly, pwidth, pheight)

    filename.append(image_path)
    countImg +=1

