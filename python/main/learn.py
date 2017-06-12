import numpy as np
import os
import cv2
import pickle
from sklearn.svm import LinearSVC


def get_image(path):
    img = cv2.imread(path)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    img = cv2.resize(img, (36, 36))
    return img


def generate_set_and_label(path):
    set = []
    label = []
    for folder in os.listdir(path):
        file_list = os.listdir(os.path.join(path, folder))
        for filename in file_list:
            img = get_image(os.path.join(path, folder, filename))
            set.append(img)
            label.append(int(folder))
    set = np.reshape(set, (len(set), -1))
    return set, label


test_set, test_label = generate_set_and_label("dataset\\test")
train_set, train_label = generate_set_and_label("dataset\\train")
clf = LinearSVC()
clf.fit(train_set, train_label)
# print("Test accuracy: " + str(clf.score(test_set, test_label)))
f=open("D:\MEGASync\Semestr6\studio\New folder\crosswords_backend\python\main\\recognizer.pickle", "wb")
pickle.dump(clf, f)
f.close()
