import keras
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D
from keras.layers import Dense, Dropout, Flatten
from keras.datasets import mnist
from keras.utils import to_categorical
from keras import backend as K

def precision(y_true, y_pred):
	true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
	predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
	precision = true_positives / (predicted_positives + K.epsilon())
	return precision
def recall(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall
def fbeta_score(y_true, y_pred, beta=1):
    if beta < 0:
        raise ValueError('The lowest choosable beta is zero (only precision).')
    else:
    	return ((1+beta**2)*(precision(y_true,y_pred)*recall(y_true,y_pred)))/((beta**2)*precision(y_true,y_pred)+recall(y_true,y_pred))    
    if K.sum(K.round(K.clip(y_true, 0, 1))) == 0:
        return 0
rows,cols=28,28
batch=128
classes=10
epochs=15
(Xtrain,Ytrain),(Xtest,Ytest) = mnist.load_data()
if K.image_data_format() == 'channels_last':
	Xtrain = Xtrain.reshape(Xtrain.shape[0],rows,cols,1).astype('float32')
	Xtest = Xtest.reshape(Xtest.shape[0],rows,cols,1).astype('float32')
	dims = (rows,cols,1)
else:
	Xtrain = Xtrain.reshape(1,Xtrain.shape[0],rows,cols).astype('float32')
	Xtest = Xtest.reshape(1,Xtest.shape[0],rows,cols).astype('float32')
	dims = (1,rows,cols)
Xtrain /= 255
Xtest /= 255
Ytrain = to_categorical(Ytrain, classes)
Ytest = to_categorical(Ytest, classes)
model = Sequential()
model.add(Conv2D(32,kernel_size=(3,3),activation='relu',input_shape=dims))
model.add(Conv2D(64,kernel_size=(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Dropout(0.25))
model.add(Conv2D(128,kernel_size=(3,3),activation='relu'))
model.add(MaxPooling2D(pool_size=(2,2)))
model.add(Flatten())
model.add(Dense(classes,activation='softmax'))
model.compile(loss='categorical_crossentropy',optimizer='sgd',metrics=['accuracy',precision,recall,fbeta_score])
model.fit(Xtrain,Ytrain,batch_size=batch,epochs=epochs,verbose=1,validation_split=0.2)
score = model.evaluate(Xtest, Ytest, verbose=1)
print('Test loss:', score[0])
print('Test accuracy:', score[1])
print('Precision:', score[2])
print('Recall:', score[3])
print('F-measure:', score[4])