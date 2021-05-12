from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.preprocessing import image
from tensorflow.keras.optimizers import RMSprop
import tensorflow as tf
import matplotlib.pyplot as plt
import cv2
import os
import numpy as np


train = ImageDataGenerator(rescale = 1/255)
validation = ImageDataGenerator(rescale = 1/255)


# In[6]:


train_generator = train.flow_from_directory("/Users/yebin/Desktop/gr_project/img_ML/train/",
                                         target_size = (200, 200),
                                         batch_size = 3,
                                         class_mode = 'categorical')

validation_generator = train.flow_from_directory("/Users/yebin/Desktop/gr_project/img_ML/validation/",
                                         target_size = (200, 200),
                                         batch_size = 3,
                                         class_mode = 'categorical')

from tensorflow.keras.optimizers import RMSprop

model = tf.keras.models.Sequential([
  # Note the input shape is the desired size of the image 150x150 with 3 bytes color
  # This is the first convolution
  tf.keras.layers.Conv2D(16, (3,3), activation='relu', input_shape=(200, 200, 3), data_format='channels_last'),
  tf.keras.layers.MaxPooling2D(2, 2),
  # The second convolution
  tf.keras.layers.Conv2D(32, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  # The third convolution
  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  # The fourth convolution
  tf.keras.layers.Conv2D(64, (3,3), activation='relu'),
  tf.keras.layers.MaxPooling2D(2,2),
  # Flatten the results to feed into a DNN
  tf.keras.layers.Flatten(),
  tf.keras.layers.Dropout(0.5),
  # 512 neuron hidden layer
  tf.keras.layers.Dense(512, activation='relu'),
  tf.keras.layers.Dense(3, activation='softmax')
])


model.summary()

model.compile(loss = 'categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

history = model.fit(train_generator, epochs=10, validation_data = validation_generator)
model.save("rps.h5")
##
from skimage import io
from skimage.transform import resize
#im = io.imread('https://static-breeze.nike.co.kr/kr/ko_kr/cmsstatic/product/CU3105-895/3ec0ccf4-87a0-4bfb-9cf5-633ae806e92d_primary.jpg?gallery')
#img = resize(im, (200,200))
#print(train_generator.class_indices)
'''
img = image.load_img('/Users/yebin/Desktop/gr_project/img_ML/train/sporty/S_00000347.jpg', target_size=(200,200))
plt.imshow(img)
plt.show()

X = image.img_to_array(img)
X = np.expand_dims(X, axis = 2)
images = np.vstack([X])
val = model.predict(images)
print(val)

if val == 0:
    print("클래식")
elif val == 1:
    print("로맨틱")
elif val == 2:
    print("스포티")
'''