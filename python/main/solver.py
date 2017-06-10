import cv2
import numpy as np
import pickle


def clear_borders(X, size):
    for y in range(0, size):
        black = False
        for x in range(0, size):
            if not black:
                if X[x, y] == 0:
                    black = True
                else:
                    X[x, y] = 0

        black = False
        for x in range(size - 1, -1, -1):
            if not black:
                if X[x, y] == 0:
                    black = True
                else:
                    X[x, y] = 0
    return X


img = cv2.imread('sudoku.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.adaptiveThreshold(gray, 255, 1, 1, 11, 2)

_, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.imshow("dsd",img2)
max = None
max_area = 0
for i in contours:
    area = cv2.contourArea(i)
    if area > 100:
        peri = cv2.arcLength(i, True)
        poly_approx = cv2.approxPolyDP(i, 0.03 * peri, True)
        if area > max_area and len(poly_approx) == 4:
            max = poly_approx
            max_area = area
h = max.reshape((4, 2))
newH = np.zeros((4, 2), dtype=np.float32)
add = h.sum(1)
newH[0] = h[np.argmin(add)]
newH[2] = h[np.argmax(add)]
diff = np.diff(h, axis=1)
newH[1] = h[np.argmin(diff)]
newH[3] = h[np.argmax(diff)]
h = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)
retval = cv2.getPerspectiveTransform(newH, h)
img = cv2.warpPerspective(gray, retval, (450, 450))

clf = pickle.load(open("recognizer.pickle", "rb"))
img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 101, 1)
# img = cv2.blur(img, (1, 1))
height, width = img.shape[:2]
step_x = width / 9
step_y = height / 9

###########
result = []

for j in range(0, 9):
    part = []
    for i in range(0, 9):
        x1 = int(i * step_x)
        x2 = int(i * step_x + step_x)
        y1 = int(j * step_y)
        y2 = int(j * step_y + step_y)
        size = 36
        X = img[y1:y2, x1:x2]
        if X.size != 0:
            X = cv2.resize(X, (size, size))
            X = clear_borders(X, size)
            X = np.reshape(X, (1, -1))
            num = clf.predict(X)
            part.append(num[0])
            cv2.putText(img, str(num[0]), (x1 + int(step_x / 2), y1 + int(step_y / 2)),
                        cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (225, 0, 0), 2)
    result.append(part)
print(result)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
