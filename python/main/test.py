from sklearn import datasets
from sklearn import svm
import numpy as np
import cv2


img =  cv2.imread('4.jpg')
X = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
for x in range(0,36):
    for y in range(0,36):
        X[x,y]=X[x,y]/255*16
X = cv2.resize(X, (8, 8))
X = np.reshape(X, (1, -1))
digits=datasets.load_digits()
clf=svm.SVC(gamma=0.001, C=100.)
clf.fit(digits.data[:-1], digits.target[:-1])
num=clf.predict(X)
# num2=clf2.predict(digits.data[-1:])
print("num2")
print(num[0])