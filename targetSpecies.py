# Take megaspecies.csv to get list of target species,
# take input data (csv) and filter out non-target species, then filter to mD crop photos

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
# use MC BQ to filter out rows with non-target species and numDetections != 1
<<<<<<< HEAD
df = pd.read_csv('/home/compbio/GDrive/UWIN_Test_Dataset/multicity-bigquery-export.csv', dtype = str) 
# df = pd.read_csv('~/Desktop/CompBio/Oxy-InceptionV3/2019_10_AST1.csv', dtype = str) 
=======

# df = pd.read_csv('/home/compbio/GDrive/UWIN_Test_Dataset/multicity-bigquery-export.csv', dtype = str) 
df = pd.read_csv('/home/compbio/mayaDir/ast2.csv', dtype = str) 
>>>>>>> a03324aa0a206c25a9974897f1c40197086e81f8
df['numAnimalDetections'] = pd.to_numeric(df['numAnimalDetections'])
#UNCOMMENT BELOW when you switch files, we only want target species. only include if commonName is in mataData
# df= df[df.commonName.isin(targetSpecies.loc[:]['commonName'])]
MCTargetSpeciesDetections = df[df['numAnimalDetections'] == 1]

allBboxStr = MCTargetSpeciesDetections.loc[:]['jsonAnimalDetection']
width = df['imgWidth']
height = df['imgHeight']
# width = 3840 
# height = 2160

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
MCTargetSpeciesDetections.loc[:, 'jsonAnimalDetection']  = MCTargetSpeciesDetections['jsonAnimalDetection'].apply(convertToPixels)


filename = []
MCTargetSpeciesDetections.reset_index()
imgName = MCTargetSpeciesDetections.loc[:]['photoDir']
coords = MCTargetSpeciesDetections.loc[:]['jsonAnimalDetection']

countImg=0
for image in imgName:
    im = Image.open(image)

<<<<<<< HEAD
# add new column to csv called croppedImage
# for each row, crop image
filename = []
for row in MCTargetSpeciesDetections:
    imgName = MCTargetSpeciesDetections.loc[row, 'photoName']
    coords = MCTargetSpeciesDetections.loc[row, 'jsonAnimalDetection']
    # open image from photoUpload
    im = Image.open(imgName)
    im = im.crop(coords[2], coords[3], coords[0], coords[1])
    # im = im.crop(coords[0], coords[1], coords[2], coords[3])
    image_path = '/home/compbio/GDrive/croppedOutput/' + imgName + '.jpg'
    im.save(image_path, 'JPEG')
=======
    truewidth, trueheight = im.size
    # if (truewidth != width  and trueheight != height):
    #     continue
>>>>>>> a03324aa0a206c25a9974897f1c40197086e81f8

    bbox = coords.iloc[countImg]['bbox']
    crop_img = im.crop((bbox[0], bbox[1], bbox[2], bbox[3]))
    
    # save cropped image to new dir 
    image_name = os.path.basename(image)
    image_path = '/home/compbio/GDrive/croppedOutput/' + image_name
    crop_img.save(image_path, 'JPEG')
    # FIXME add filename list as column in csv
    filename.append(image_path)
    countImg +=1



    # get path of photoUpload, uncomment of using UWIN dataset. Not necessary is photos are all in one dir/folder
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
    





    # ymin = ann['bbox'][1]
    # ymax = ymin + ann['bbox'][3]
    # xmin = ann['bbox'][0]
    # xmax = xmin + ann['bbox'][2]

#     ymax = ann['bbox'][1]
#     ymin = ymax + ann['bbox'][3]
#     xmax = ann['bbox'][0]
#     xmin = xmax + ann['bbox'][2]
#     print(ann)
#     print(ymin, ymax, xmin, xmax)
# # 608, 1213, 897, 1833
#     ann['bbox'][3] = ymin * height 
#     ann['bbox'][1] = ymax * height 
#     ann['bbox'][0] = xmin * width 
#     ann['bbox'][2] = xmax * width

    # ulx = coords.iloc[countImg]['bbox'][0]
    # uly = coords.iloc[countImg]['bbox'][1]
    # pwidth = coords.iloc[countImg]['bbox'][2]
    # pheight = coords.iloc[countImg]['bbox'][3]
    # crop_img = im.crop((ulx, uly, ulx+pwidth, uly+pheight))