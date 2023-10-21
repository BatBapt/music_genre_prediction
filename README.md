# Introduction

This repository is about Music Genre Prediction.
Given an album cover and 30 seconds of music, can the model predict the genre ?

# Files

## dl_music.py
This file contains all of the functions used to collect data from Deezer API.
You cant use to download music data for many genre (I used 5 in my case).
You just need to update the dictionary in the "dl_all()" function with the format:
'genre': list of playlist you want to download

## best_model.h5
This is my best model created for this task. Load it using Tensorflow

## fusion.ipynb
Notebook used to develop the model. You can improve it by updating data processing, such as image size, mfcc size, increase number 
of examples....

# prod.ipynb
Notebook used to test new data in a fast way. Just use the function "get_album" in the dl_music.py file then run your notebook