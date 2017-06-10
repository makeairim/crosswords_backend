import numpy as np
from sklearn.svm import LinearSVC
import os
import cv2
import pickle

def get_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY )
    img = cv2.resize(img, (36,36))
    return img

print("Learning...")
path_test_set = "dataset\\test"
testset = []
test_label = []
for folder in os.listdir(path_test_set):
    flist = os.listdir(os.path.join(path_test_set, folder))
    for f in flist:
        img = get_image(os.path.join(path_test_set, folder, f))
        testset.append(img)
        test_label.append(int(folder))
testset = np.reshape(testset, (len(testset), -1))
print("...")

path_train_set = "dataset\\train"
trainset = []
for folder in os.listdir(path_train_set):
    flist = os.listdir(os.path.join(path_train_set, folder))
    for f in flist:
        img = get_image(os.path.join(path_train_set, folder, f))
        trainset.append(img)
trainset = np.reshape(trainset, (5000, -1))

train_label = []
for i in range(0,10):
    temp = 500*[i]
    train_label.extend(temp)

print("...")

clf = LinearSVC()
clf.fit(trainset, train_label)

# result = clf.predict(testset)
print("Test accuracy: " + str(clf.score(testset, test_label)))

pickle.dump( clf, open( "recognizer.pickle", "wb" ) )