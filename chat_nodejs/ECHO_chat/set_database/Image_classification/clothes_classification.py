#!/usr/bin/env python
# coding: utf-8

# In[1]:

from webScrap import prd_img
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np

# In[5]:


train = ImageDataGenerator(rescale = 1/255)
validation = ImageDataGenerator(rescale = 1/255)


# In[6]:


train_dataset = train.flow_from_directory("/Users/yebin/Desktop/gr_project/img_ML/train/",
                                         target_size = (200, 200),
                                         batch_size = 3,
                                         class_mode = 'binary')

validation_dataset = train.flow_from_directory("/Users/yebin/Desktop/gr_project/img_ML/validation/",
                                         target_size = (200, 200),
                                         batch_size = 3,
                                         class_mode = 'binary')


# In[7]:


train_dataset.class_indices


# In[8]:


from tensorflow.keras.optimizers import RMSprop

model = tf.keras.models.Sequential([
    # Note the input shape is the desired size of the image 150x150 with 3 bytes color
    # This is the first convolution
    tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(200, 200, 3)),
    tf.keras.layers.MaxPooling2D(2, 2),
    # The second convolution
    tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The third convolution
    tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    tf.keras.layers.MaxPooling2D(2,2),
    # The fourth convolution
    #tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    #tf.keras.layers.MaxPooling2D(2,2),
    # The fifth convolution
    #tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
    #tf.keras.layers.MaxPooling2D(2,2),
    # Flatten the results to feed into a DNN
    tf.keras.layers.Flatten(),
    # 512 neuron hidden layer
    tf.keras.layers.Dense(512, activation='relu'),
    # Only 1 output neuron. It will contain a value from 0-1 where 0 for 1 class ('horses') and 1 for the other ('humans')
    tf.keras.layers.Dense(1, activation='sigmoid')
])

model.compile(loss='binary_crossentropy',
              optimizer=RMSprop(lr=0.001),
              metrics=['accuracy'])


# In[19]:


model_fit = model.fit(
      train_dataset,
      steps_per_epoch=3,  
      epochs=5, 
      validation_data = validation_dataset)


# In[22]:


from skimage import io
from skimage.transform import resize
im = io.imread(prd_img[0])
img = resize(im, (200,200))

plt.imshow(img)
plt.show()

X = image.img_to_array(img)
X = np.expand_dims(X, axis = 0)
images = np.vstack([X])

val = model.predict(images)
print(val)

if val == 1:
    print("동물 문양 프린팅 원피스")
elif val == 0:
    print("운동용 탱크 탑")
else:
    print("결과 없음")











# %%
