from keras.models import Sequential, Model,  load_model
from keras.layers import Dense,Activation,Bidirectional, LSTM, RepeatVector, Input 
from keras.utils import np_utils, generic_utils
import numpy as np
import os, sys

def equal_float(a, b):
    #return abs(a - b) <= sys.float_info.epsilon
    return abs(a - b) <= 1E-3 #see edit below for more info

def fetchModel(isNew, trainX, trainY):
	if isNew == True:
		#feature extraction
		# this is the size of our encoded representations
		encoding_dim = 10  # 32 floats -> compression of factor 24.5, assuming the input is 784 floats
		# this is our input placeholder
		input_seq = Input(shape=(20,))
		# "encoded" is the encoded representation of the input
		encoded = Dense(encoding_dim, activation='relu')(input_seq)
		# "decoded" is the lossy reconstruction of the input
		decoded = Dense(20, activation='sigmoid')(encoded)

		# this model maps an input to its reconstruction
		autoencoder = Model(input=input_seq, output=decoded)

		autoencoder.compile(optimizer='adadelta', loss='binary_crossentropy')
		autoencoder.fit(trainX,trainX,epochs=1,shuffle=True)

		feTrainX = autoencoder.predict(trainX)

		model = Sequential()
		model.add(Dense(12, input_dim=20))
		model.add(Dense(8))
		model.add(Dense(3))
		model.add(Activation('softmax'))
		model.compile(loss='categorical_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
		model.fit(feTrainX, trainY, epochs=10,shuffle=True,validation_split=0.1)
		model.save('my_model.h5') 
	else:
		model = load_model('my_model.h5')
	return model

def main(argv):
	ar = np.loadtxt('trainingSet.txt',delimiter=',')

	tempX = ar[:,0]	
	trainX = np.zeros((len(tempX),20), dtype=np.int)

	print(len(tempX))
	for i in range(0,len(tempX)):
		trainX[i][tempX[i]] = 1

	trainY = ar[:,1]
	categorical_labels = np_utils.to_categorical(trainY, num_classes=3)


	if argv != 0: 
		isNew = True
	else:
		isNew = False

	model = fetchModel(isNew, trainX, categorical_labels)



	accuracis = []
	path = os.path.join(os.getcwd(),"test")
	for filename in os.listdir(path):
		filePath = os.path.join(path,filename)
		ar = np.loadtxt(filePath,delimiter=',')

		tempX = ar[:,0]	
		testX = np.zeros((len(tempX),20), dtype=np.int)

		for i in range(0,len(tempX)):
			trainX[i][tempX[i]] = 1

		testY = ar[:,1]
		categorical_labels = np_utils.to_categorical(testY, num_classes=3)
		scores = model.evaluate(testX, categorical_labels, verbose=0)
		# print("%s: %.2f%%" % (model.metrics_names[1], scores[1]*100))

		accuracis.append(scores[1])


	print("Mean Of Accuracy: %f" % np.mean(accuracis))
	print("Variance Of Accuracy: %f" % np.std(accuracis))



	#bidirectional LSTM
	# Expected input batch shape: (batch_size, timesteps, data_dim)
	# model = Sequential()
	# model.add(LSTM(10, return_sequences=True, input_shape=(20,1)))
	# model.add(LSTM(10))
	# model.add(Dense(3))
	# model.add(Activation('softmax'))
	# model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

	# model.fit(trainX, categorical_labels, epochs=1,shuffle=True,validation_split=0.1)

if __name__ == '__main__':
	main(sys.argv[1])


# from sklearn.multiclass import OneVsOneClassifier
# from sklearn.svm import LinearSVC
# import numpy as np

# def equal_float(a, b):
#     #return abs(a - b) <= sys.float_info.epsilon
#     return abs(a - b) <= 1E-3 #see edit below for more info

# def main():
# 	ar = np.loadtxt('output.txt',delimiter=',')
# 	trainX = ar[:,0:2]
# 	trainy = ar[:,2]

# 	predX = trainX
# 	predY = OneVsOneClassifier(LinearSVC(random_state=0)).fit(trainX, trainy).predict(predX)
	
# 	seq = ""
# 	for i in predY:
# 		if  equal_float(1,i):
# 			seq+="a"
# 		elif equal_float(2,i):
# 			seq+="b"
# 		else:
# 			seq+="-"
# 	print(seq)

# if __name__ == '__main__':
# 	main()