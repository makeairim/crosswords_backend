import cv2
import numpy as np
import joblib

font = cv2.FONT_HERSHEY_SIMPLEX
ratio2 = 3
kernel_size = 3
lowThreshold = 30

clf = joblib.load('classifier.pkl')

is_print = True

img = cv2.imread('test1.jpg')
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img = cv2.blur(img, (1, 1))
height, width = img.shape[:2]
step_x = width / 9
step_y = height / 9
# todo
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 101, 1)
for i in range(0, 9):
    for j in range(0, 9):
        x1 = int(i * step_x)
        x2 = int(i * step_x + step_x)
        y1 = int(j * step_y)
        y2 = int(j * step_y + step_y)

        X = img[y1:y2, x1:x2]
        if X.size != 0:
            X = cv2.resize(X, (36, 36))
            ##################
            # cleaning borders
            for y in range(0, 36):
                black = False
                for x in range(0, 36):
                    if not black:
                        if X[x, y] == 0:
                            black = True
                        else:
                            X[x, y] = 0

                black = False
                for x in range(35, -1, -1):
                    if not black:
                        if X[x, y] == 0:
                            black = True
                        else:
                            X[x, y] = 0

            ##########3
            # cv2.imshow('a', X)
            # cv2.waitKey(0)
            #################
            # # change input
            # for y in range(0,36):
            #     for x in range(0,36):
            #         if X[x,y] > 200:
            #             X[x,y]=1
            #         else:
            #             X[x,y]=0
            #
            #
            # kernel = np.ones((3,3),np.uint8)
            # X = cv2.erode(X,kernel,iterations = 1)
            # X = cv2.dilate(X,kernel,iterations = 1)
            #
            # for y in range(0,36):
            #     for x in range(0,36):
            #         if X[x,y] ==1:
            #             X[x,y]=255

            ###############
            # cv2.imshow('b', X)
            # cv2.waitKey(0)
            X = np.reshape(X, (1, -1))
            num = clf.predict(X)
            cv2.putText(img, str(num[0]), (x1 + int(step_x / 2), y1 + int(step_y / 2)), font, 1, (225, 0, 0), 2)


print("ready")
# Now draw them
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
