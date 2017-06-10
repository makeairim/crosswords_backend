import numpy as np
from sklearn.svm import LinearSVC
import os
import cv2
import pickle



TEST_PATH = "dataset\\test"
list_folder = os.listdir(TEST_PATH)
testset = []
test_label = []
for folder in list_folder:
    flist = os.listdir(os.path.join(TEST_PATH, folder))
    for f in flist:
        im = cv2.imread(os.path.join(TEST_PATH, folder, f))
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY )
        im = cv2.resize(im, (36,36))
        testset.append(im)
        test_label.append(int(folder))
testset = np.reshape(testset, (len(testset), -1))

TRAIN_PATH = "dataset\\train"
list_folder = os.listdir(TRAIN_PATH)
trainset = []
for folder in list_folder:
    flist = os.listdir(os.path.join(TRAIN_PATH, folder))
    for f in flist:
        im = cv2.imread(os.path.join(TRAIN_PATH, folder, f))
        im = cv2.cvtColor(im, cv2.COLOR_RGB2GRAY )
        im = cv2.resize(im, (36,36))
        trainset.append(im)
trainset = np.reshape(trainset, (5000, -1))

train_label = []
for i in range(0,10):
    temp = 500*[i]
    train_label.extend(temp)


clf = LinearSVC()
clf.fit(trainset, train_label)

# result = clf.predict(testset)
print("Test accuracy: " + str(clf.score(testset, test_label)))

pickle.dump( clf, open( "recognizer.pickle", "wb" ) )