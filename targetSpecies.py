# Use megaspecies.csv to get list of target species,
# use input data and filter out non-target species, then filter to megaDetector crop photos

from audioop import ulaw2lin
import os
import csv
import json
import numpy as np
import pandas as pd
from PIL import Image

# create list of target species 
df = pd.read_csv('/home/compbio/GDrive/UWIN_Test_Dataset/MegaSpecies.csv', dtype = str) 
df = df[df.target == 'Target']
targetSpecies = df.loc[:, ['commonName','target']]

# use MegaClassifier BigQuery to filter out rows with non-target species and numDetections != 1
df = pd.read_csv('/home/compbio/GDrive/UWIN_Test_Dataset/multicity-bigquery-export.csv', dtype = str) 
# df = pd.read_csv('~/Desktop/CompBio/Oxy-InceptionV3/2019_10_AST1.csv', dtype = str) 

# df = pd.read_csv('/home/compbio/GDrive/UWIN_Test_Dataset/multicity-bigquery-export.csv', dtype = str) 
df = pd.read_csv('/home/compbio/mayaDir/ast2.csv', dtype = str) 

df['numAnimalDetections'] = pd.to_numeric(df['numAnimalDetections'])

#UNCOMMENT BELOW when you switch files, we only want target species. only include if commonName is in mataData
# df= df[df.commonName.isin(targetSpecies.loc[:]['commonName'])]
MCTargetSpeciesDetections = df[df['numAnimalDetections'] == 1]

allBboxStr = MCTargetSpeciesDetections.loc[:]['jsonAnimalDetection']
width = df['imgWidth'] # width = 3840 
height = df['imgHeight'] # height = 2160


def convertToPixels (ann):
    ann = eval(ann)
    width = 3840 
    height = 2160

    ulx = ann['bbox'][0] * width 
    uly = ann['bbox'][1] * height 
    brx = ulx + ann['bbox'][2]*width 
    bry = uly + ann['bbox'][3]*height 

    ann['bbox'][0] = ann['bbox'][0] * width 
    ann['bbox'][1] = ann['bbox'][1] * height 
    ann['bbox'][2] = ulx + ann['bbox'][2]*width 
    ann['bbox'][3] = uly + ann['bbox'][3]*height 
    return ann
# apply convertToPixels to each bbox in 'jsonAnimalDetection' column
MCTargetSpeciesDetections.loc[:, 'jsonAnimalDetection']  = MCTargetSpeciesDetections['jsonAnimalDetection'].apply(convertToPixels)

# gather data from orig detections that we'll need
filename = []
MCTargetSpeciesDetections.reset_index()
imgName = MCTargetSpeciesDetections.loc[:]['photoDir']
coords = MCTargetSpeciesDetections.loc[:]['jsonAnimalDetection']

countImg=0
for image in imgName:
    im = Image.open(image)


# add new column to csv called croppedImage FIXME
filename = []

# for each row, crop the image
for row in MCTargetSpeciesDetections:
    imgName = MCTargetSpeciesDetections.loc[row, 'photoName']
    coords = MCTargetSpeciesDetections.loc[row, 'jsonAnimalDetection']

    # open image from photoUpload
    im = Image.open(imgName)
    # actually crop the image
    im = im.crop(coords[2], coords[3], coords[0], coords[1])
    # save image to folder destination
    image_path = '/home/compbio/GDrive/croppedOutput/' + imgName + '.jpg'
    im.save(image_path, 'JPEG')

    truewidth, trueheight = im.size
    # if (truewidth != width  and trueheight != height):
    #     continue

    bbox = coords.iloc[countImg]['bbox']
    crop_img = im.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
    
    # save cropped image to new dir 
    image_name = os.path.basename(image)
    image_path = '/home/compbio/GDrive/croppedOutput/' + image_name
    crop_img.save(image_path, 'JPEG')
    # add filename list as column in csv
    filename.append(image_path)
    countImg +=1
# FIXME ensure column is added correctly
MCTargetSpeciesDetections.loc[:][filename]



# Uncomment of using UWIN dataset. 
#   get path of photoUpload. Not necessary is photos are all in one dir/folder
    # if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/first_upload/'+ image):
    #     im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/first_upload/' + image)
    #     print('first_upload')
    # if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/second_upload'+ image):
    #     im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/second_upload/' + image)
    #     print('second_upload')
    # if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/third_upload'+ image):
    #     im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/third_upload/' + image)
    #     print('third_upload')
    # if os.path.exists('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/fourth_upload/' + image):
    #     im = Image.open('/home/compbio/GDrive/UWIN_Test_Dataset/Photo_Upload/fourth_upload/' + image)
    #     print('fourth_upload')