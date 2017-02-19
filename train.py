import cv2
import numpy as np
import cPickle
from os import path
from os import listdir
from keras.datasets import cifar10
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.layers import Flatten
from keras.constraints import maxnorm
from keras.optimizers import SGD
from keras.layers.convolutional import Convolution2D
from keras.layers.convolutional import MaxPooling2D
from keras.models import load_model
from keras.utils import np_utils
from keras import backend as K


##shallow model
#'''model = Sequential()
#model.add(Convolution2D(32, 3, 3, input_shape=(32, 32, 3), border_mode='same', activation='relu', W_constraint=maxnorm(3)))
#model.add(Dropout(0.2))
#model.add(Convolution2D(32, 3, 3, activation='relu', border_mode='same', W_constraint=maxnorm(3)))
#model.add(MaxPooling2D(pool_size=(2, 2)))
#model.add(Flatten())
#model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
#model.add(Dropout(0.5))
#model.add(Dense(num_classes, activation='softmax'))'''
#'''#deeper model
#model = Sequential()
#model.add(Convolution2D(32, 3, 3, input_shape=(32, 32, 3), activation='relu', border_mode='same'))
#model.add(Dropout(0.2))
#model.add(Convolution2D(32, 3, 3, activation='relu', border_mode='same'))
#model.add(MaxPooling2D(pool_size=(2, 1)))
#model.add(Convolution2D(64, 3, 3, activation='relu', border_mode='same'))
#model.add(Dropout(0.2))
#model.add(Convolution2D(64, 3, 3, activation='relu', border_mode='same'))
#model.add(MaxPooling2D(pool_size=(2, 1)))
#model.add(Convolution2D(128, 3, 3, activation='relu', border_mode='same'))
#model.add(Dropout(0.2))
#model.add(Convolution2D(128, 3, 3, activation='relu', border_mode='same'))
#model.add(MaxPooling2D(pool_size=(2, 1)))
#model.add(Flatten())
#model.add(Dropout(0.2))
#model.add(Dense(1024, activation='relu', W_constraint=maxnorm(3)))
#model.add(Dropout(0.2))
#model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
#model.add(Dropout(0.2))
#model.add(Dense(num_classes, activation='softmax'))'''


K.set_image_dim_ordering('th')

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# Load training data
data = cPickle.load(open("rawdata.dat", "rb"))
#print data[2][0]
shape = (len(data), 6, 4, 1)
max = 10000
#for i in range(len(data)):
#	for j in range(6):
#		if data[i][0][j][0][0] < max and data[i][0][j][0][0] != 0 :
#			max = data[i][0][j][0][0]
#			
#print max
#print data[50:100]
num_classes = 127
xtrain = np.zeros(shape)
ytrainNote = np.ndarray((shape[0]))
ytrainLength = np.ndarray((shape[0]))

weight = np.zeros((127))
weightDict = dict()
for i in range(1,60):
	weight[60 + i] = 1 + (50 - i) / 50
	weight[60 - i] = 1 + (50 - i) / 50
for i in range(127):
	weightDict[i] = weight[i]

for i in range(shape[0]):
	xtrain[i] = data[i][0]
	ytrainNote[i] = data[i][1].note
	ytrainLength[i] = data[i][1].length
	
#print xtrain[50:100]

# normalize inputs from 0-255 to 0.0-1.0
xtrain = xtrain.astype('float32')
xtrain = xtrain / max

#print xtrain
print ytrainNote.shape

# one hot encode outputs
ytrainNote = ytrainNote.reshape((-1, 1))
ytrainLength = ytrainLength.reshape((-1, 1))
#ytrain = np_utils.to_categorical(ytrain)

## Create the model

model = Sequential()
model.add(Convolution2D(32, 2, 2, input_shape=(6, 4, 1), activation='relu', border_mode='same'))
model.add(Dropout(0.2))
model.add(Convolution2D(32, 2, 2, activation='relu', border_mode='same'))
model.add(MaxPooling2D(pool_size=(2, 1)))
#model.add(Convolution2D(64, 2, 2, activation='relu', border_mode='same'))
#model.add(Dropout(0.2))
#model.add(Convolution2D(64, 2, 2, activation='relu', border_mode='same'))
#model.add(MaxPooling2D(pool_size=(2, 1)))
#model.add(Convolution2D(128, 2, 2, activation='relu', border_mode='same'))
#model.add(Dropout(0.2))
#model.add(Convolution2D(128, 2, 2, activation='relu', border_mode='same'))
#model.add(MaxPooling2D(pool_size=(2, 1)))
model.add(Flatten())
model.add(Dropout(0.2))
model.add(Dense(1024, activation='relu', W_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Dense(512, activation='relu', W_constraint=maxnorm(3)))
model.add(Dropout(0.2))
model.add(Dense(num_classes, activation='softmax'))


# Compile model
epochs = 5
lrate = 0.01
decay = lrate/epochs
sgd = SGD(lr=lrate, momentum=0.9, decay=decay, nesterov=False)
model.compile(loss='sparse_categorical_crossentropy', optimizer=sgd, metrics=['accuracy'])
print(model.summary())

model = load_model('model1.dat')

# Fit the model
model.fit(np.array(xtrain[:]), np.array(ytrainNote[:]), validation_data=None, batch_size=512, nb_epoch=epochs, verbose=1, callbacks=[], validation_split=0.1, shuffle=True, class_weight=None, sample_weight=None)
#model.fit(xtrain, ytrain, validation_data=(xtrain, ytrain), nb_epoch=epochs, batch_size=32)
model.save('model1.dat')

print model.predict_classes(xtrain[50:65], batch_size=32, verbose=1)
print ytrainNote[50:65]
"""
# Final evaluation of the model
scores = model.evaluate(X_test, y_test, verbose=0)
print("Accuracy: %.2f%%" % (scores[1]*100))
"""
