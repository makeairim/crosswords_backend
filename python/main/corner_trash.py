import cv2
import numpy as np

filename = 'test1.jpg'
img = cv2.imread(filename)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# find Harris corners
gray = np.float32(gray)
dst = cv2.cornerHarris(gray, 2, 3, 0.04)
dst = cv2.dilate(dst, None)
ret, dst = cv2.threshold(dst, 0.01 * dst.max(), 255, 0)
dst = np.uint8(dst)

# find centroids
ret, labels, stats, centroids = cv2.connectedComponentsWithStats(dst)
# print(centroids)
# define the criteria to stop and refine the corners
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 0.001)
corners = cv2.cornerSubPix(gray, np.float32(centroids), (5, 5), (-1, - 1), criteria)

def check_points(point_list):
    min_x = int(point_list[0][0])
    min_y = int(point_list[0][1])
    max_x = int(point_list[0][0])
    max_y = int(point_list[0][1])
    for point in point_list:
        point[0] = int(point[0])
        point[1] = int(point[0])
        if point[0] < min_x:
            min_x = point[0]
        if point[1] < min_y:
            min_y = point[1]
        if point[0] > max_x:
            max_x = point[0]
        if point[1] > max_y:
            max_y = point[1]
    step_x = int(max_x / 9)
    step_y = int(max_y / 9)
    #the acceptable distance for a point from the line
    distance_from_line=4
    # print (corners)
    i = 0
    for point in point_list:
        if (not (point[0] % step_x) < distance_from_line or not (point[1] % step_y) < distance_from_line)and i <len(point_list):
            point_list = np.delete(point_list, i, axis=0)
        i += 1
    return point_list

corners=check_points(corners)
centroids=check_points(centroids)
print(len(corners))
# unsatisfying
print(len(centroids))

# miejsce gdzie sie linie stykaja
print(corners)


#way to find numbers
# img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 101, 1)
for i in range(0,9):
    for j in range(0,9):
        y1=int(Points[j+i*10][1]+5)
        y2=int(Points[j+i*10+11][1]-5)
        x1=int(Points[j+i*10][0]+5)
        x2=int(Points[j+i*10+11][0]-5)
        # Saving extracted block for training, uncomment for saving digit blocks
        # cv2.imwrite(str((i+1)*(j+1))+".jpg", sudoku1[y1: y2,
        #                                            x1: x2])
        cv2.rectangle(img,(x1,y1),
                      (x2, y2),(0,255,0),2)


# res = np.hstack((centroids, corners))
# res = np.int0(res)
# img[res[:, 1],res[:, 0]]=[0, 0, 255]
# img[res[:, 3], res[:, 2]] = [0, 255, 0]
# cv2.imshow('subpixel5.png', img)
# cv2.waitKey(0)
# cv2.imwrite('subpixel5.png', img)
