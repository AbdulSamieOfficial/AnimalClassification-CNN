# -*- coding: utf-8 -*-
"""Animal_Classification__Model.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/116wulOV6mtZ1z3ZD07VBUO61W7ztz49S
"""

import numpy as np
import cv2
import os
import random
import matplotlib.pyplot as plt
import tensorflow
from keras.models import Sequential
from keras.layers import Conv2D,MaxPooling2D,Dropout,Flatten,Dense,Activation,BatchNormalization
from sklearn.model_selection import train_test_split
from tensorflow.keras.preprocessing.image import img_to_array,ImageDataGenerator
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.applications.mobilenet_v2 import preprocess_input
from tensorflow.keras.models import Model

from zipfile import ZipFile
with ZipFile("animals.zip",'r') as zip:
  zip.extractall()
  print('Done')

file_cat=os.listdir("/animals/cats")
print('cat Data')
print(file_cat)
file_dog=os.listdir("/animals/dogs")
print('Dog Data')
print(file_dog)

file_panda=os.listdir("/animals/panda")
print('Panda Data')
print(file_panda)

for image in file_cat:
    img=os.path.join("/animals/cats",image)
    print(img)
    break

for image in file_cat:
    img=os.path.join("/animals/cats",image)
    img_a=cv2.imread(img)
    plt.imshow(img_a)
    break

for image in file_dog:
    img=os.path.join("/animals/dogs",image)
    img_a=cv2.imread(img)
    plt.imshow(img_a)
    break

value_train=[]
for image in file_cat:
    img=os.path.join("/animals/cats",image)
    
    pic=load_img(img,target_size=(100,100))
    pic=img_to_array(pic)
    pics=preprocess_input(pic)
    value_train.append([pics,0])

for image in file_dog:
    img=os.path.join("/animals/dogs",image)
    
    pic=load_img(img,target_size=(100,100))
    pic=img_to_array(pic)
    pics=preprocess_input(pic)
    value_train.append([pics,1])

for image in file_panda:
    img=os.path.join("/animals/panda",image)
    
    pic=load_img(img,target_size=(100,100))
    pic=img_to_array(pic)
    pics=preprocess_input(pic)
    value_train.append([pics,2])

random.shuffle(value_train)

X=[]
Y=[]
for i in range(len(value_train)):
  X.append(value_train[i][0])
  Y.append(value_train[i][1])

X=np.array(X,dtype="float32")
Y=np.array(Y)

model = Sequential()

model.add(Conv2D(64,(3,3),activation ='relu', input_shape = (100,100,3)))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D( 32,(3,3), activation ='relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(16,(3,3), activation ='relu'))
model.add(MaxPooling2D((2,2)))

model.add(Conv2D(8,(3,3), activation ='relu'))
model.add(MaxPooling2D((2,2)))



model.add(Flatten())
model.add(Dense(128, activation = "relu"))
model.add(Dense(64, activation = "relu"))
model.add(Dense(3, activation = "softmax"))

model.compile(loss = 'sparse_categorical_crossentropy', optimizer = 'adam',metrics=['accuracy'])

model.summary()

X_train_val, X_test, Y_train_val, Y_test = train_test_split(X, Y, test_size = 0.2)

X_train, X_val, Y_train, Y_val = train_test_split(X_train_val, Y_train_val, test_size = 0.3)

model.fit(X_train, Y_train,epochs =10, validation_data = (X_val, Y_val))

Y_pred = model.predict(X_test)
score = model.evaluate(X_test, Y_test)
print('Accuracy over the test set: \n ', round((score[1]*100), 2), '%')