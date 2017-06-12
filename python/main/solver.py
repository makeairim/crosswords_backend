import copy
import cv2
import numpy as np
import pickle
import sys

from backtrack import print_grid,solveSudoku

def clear_digit_borders(digit, size):
    for y in range(0, size):
        black = False
        for x in range(0, size):
            if not black:
                if digit[x, y] == 0:
                    black = True
                else:
                    digit[x, y] = 0

        black = False
        for x in range(size - 1, -1, -1):
            if not black:
                if digit[x, y] == 0:
                    black = True
                else:
                    digit[x, y] = 0
    return digit


def to_bw_cut_image(filepath):
    img = cv2.imread(filepath)
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
    new_h = np.zeros((4, 2), dtype=np.float32)
    add = h.sum(1)
    new_h[0] = h[np.argmin(add)]
    new_h[2] = h[np.argmax(add)]
    diff = np.diff(h, axis=1)
    new_h[1] = h[np.argmin(diff)]
    new_h[3] = h[np.argmax(diff)]
    h = np.array([[0, 0], [449, 0], [449, 449], [0, 449]], np.float32)
    val = cv2.getPerspectiveTransform(new_h, h)
    img = cv2.warpPerspective(gray, val, (450, 450))
    return img


def get_matrix(img):
    clf = pickle.load(open("recognizer.pickle", "rb"))
    img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 101, 1)
    height, width = img.shape[:2]
    step_x = width / 9
    step_y = height / 9
    result = []
    for j in range(0, 9):
        part = []
        for i in range(0, 9):
            x1 = int(i * step_x)
            x2 = int(i * step_x + step_x)
            y1 = int(j * step_y)
            y2 = int(j * step_y + step_y)
            size = 36
            digit = img[y1:y2, x1:x2]
            if digit.size != 0:
                digit = cv2.resize(digit, (size, size))
                digit = clear_digit_borders(digit, size)
                digit = np.reshape(digit, (1, -1))
                predicted_number = clf.predict(digit)
                part.append(predicted_number[0])
                # cv2.putText(img, str(predicted_number[0]), (x1 + int(step_x / 2), y1 + int(step_y / 2)),
                #             cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (225, 0, 0), 2)
        result.append(part)
    # print(result)
    # cv2.imshow('img', img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    return result


# get_matrix('sudoku.jpg')
def to_labeled_rgb_img(img, grid, matrix2):
    img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
    height, width = img.shape[:2]
    step_x = width / 9
    step_y = height / 9
    for j in range(0, 9):
        for i in range(0, 9):
            x = int(i * step_x)
            y = int(j * step_y)
            if matrix2[j][i] == 0:
                cv2.putText(img, str(grid[j][i]), (x + int(step_x / 2), y + int(step_y / 2)),
                            cv2.FONT_HERSHEY_SCRIPT_SIMPLEX, 1, (0, 255, 0), 2)
    return img


if __name__ == '__main__':
    try:
        img = to_bw_cut_image(sys.argv[1])
        matrix = get_matrix(img)
        print_grid(matrix)
        # matrix = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
        #           [5, 2, 0, 0, 0, 0, 0, 0, 0],
        #           [0, 8, 7, 0, 0, 0, 0, 3, 1],
        #           [0, 0, 3, 0, 1, 0, 0, 8, 0],
        #           [9, 0, 0, 8, 6, 3, 0, 0, 5],
        #           [0, 5, 0, 0, 9, 0, 6, 0, 0],
        #           [1, 3, 0, 0, 0, 0, 2, 5, 0],
        #           [0, 0, 0, 0, 0, 0, 0, 7, 4],
        #           [0, 0, 5, 2, 0, 6, 3, 0, 0]]
        # matrix = [[0, 0, 7, 5, 0, 1, 4, 3, 0],
        #           [0, 1, 0, 7, 0, 0, 2, 0, 5],
        #           [0, 0, 0, 9, 0, 6, 0, 7, 1],
        #           [0, 8, 2, 0, 0, 0, 5, 6, 0],
        #           [0, 0, 0, 2, 0, 5, 0, 0, 0],
        #           [0, 3, 5, 0, 0, 0, 1, 4, 0],
        #           [1, 5, 0, 4, 0, 3, 0, 0, 0],
        #           [7, 0, 9, 0, 0, 2, 0, 1, 0],
        #           [0, 6, 3, 1, 0, 8, 7, 0, 0]]

        # (res, grid) = solveSudoku(matrix)
        (res, grid, orig) = solve(matrix)
        img = to_labeled_rgb_img(img, grid, orig)
        cv2.imshow('img', img)
        cv2.imwrite('solution.jpg', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        if (res == True):
            print_grid(grid)
    except:
        raise

def solve(path):
    try:
        print(path)
        img = to_bw_cut_image(path)
        matrix = get_matrix(img)
        print_grid(matrix)
        # (res, grid) = solveSudoku(matrix)
        (res, grid, orig) = solveSudoku(matrix)
        img = to_labeled_rgb_img(img, grid, orig)
        # f = open(path, 'wb')
        # f.write(img)
        # f.close()
        cv2.imwrite(path, img)
    except:
        raise
    return True