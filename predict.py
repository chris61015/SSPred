from keras.models import Sequential, Model,  load_model
from keras.layers import Dense,Activation,Bidirectional, LSTM, RepeatVector, Input, Masking, TimeDistributed,Embedding
from keras.utils import np_utils, generic_utils
import numpy as np
import os, sys


def fetchModel(isNew, trainX, trainY ,windowSize):

	dimension = 2 * windowSize + 1

	if isNew == True:

		model = Sequential()		#adding Neural Networks layers one after one 
		model.add(Dense(12, input_shape=(dimension,)))		#First layer with 12 neurons
		model.add(Dense(8))									#Second layer with 8 neurons
		model.add(Dense(3))									#Thrid layer with 3 neurons
		model.add(Activation('softmax'))					#Softmax will provide probabilities for three options
		model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])	#call tensorflow to compute
		model.fit(trainX, trainY, epochs=10,shuffle=True,validation_split=0.1)			#trainging start

		model.save('my_model.h5') 			#save model
	else:
		model = load_model('my_model.h5')	#load model
	return model

def main(argv):

	trainPath = os.path.join(os.getcwd(),"train")  	#get data from train folder
	windowSize = 5									#adjust window size to get different result

	trainX = []
	trainY = []
	for _, filename in enumerate(os.listdir(trainPath), start=0):			#loop through txt file in folder
		filePath = os.path.join(trainPath,filename)
		ar = np.loadtxt(filePath,delimiter=',')

		tempX = ar[:,0]	
		tempY = ar[:,1]
		for index, value in enumerate(tempX, start=windowSize):
			if index - windowSize >=0 and index + windowSize < len(tempX):
				#generate sliding window dataset
				tmp = []
				for slide in range(-windowSize,windowSize+1):
					tmp.append(tempX[index+slide])
				trainX.append(tmp)
				trainY.append(tempY[index])

	trainX = np.array(trainX)
	trainY = np.array(trainY)

	#if we want to use categorical_crossentropy as loss function, we should turn label into one-hot vectors
	categorical_labels = np_utils.to_categorical(trainY, num_classes=3)

	#To see whether we should retrain model, or just fetch it
	if argv != 0: 
		isNew = True
	else:
		isNew = False

	#get trained model
	model = fetchModel(isNew, trainX, categorical_labels, windowSize)

	accuracis = []
	path = os.path.join(os.getcwd(),"test")
	for filename in os.listdir(path):											#loop through txt file in folder
		filePath = os.path.join(path,filename)
		ar = np.loadtxt(filePath,delimiter=',')

		testX = []
		testY = []
		tempX = ar[:,0]	
		tempY = ar[:,1]
		for index, value in enumerate(tempX, start=windowSize):
			if index - windowSize >=0 and index + windowSize < len(tempX):
				#generate sliding window dataset
				tmp = []
				for slide in range(-windowSize,windowSize+1):
					tmp.append(tempX[index+slide])
				testX.append(tmp)
				testY.append(tempY[index])

		categorical_labels = np_utils.to_categorical(testY, num_classes=3)
		scores = model.evaluate(testX, categorical_labels, verbose=0)
		# print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

		accuracis.append(scores[1])

	print("Mean Of Accuracy: %f" % np.mean(accuracis))
	print("Variance Of Accuracy: %f" % np.std(accuracis))

if __name__ == '__main__':
	main(sys.argv[1])

# Ref: 
# Keras:https://keras.io/

