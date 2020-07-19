import sys
# from PIL import Image
import numpy
# from numpy import asarray
import cv2
from math import sqrt


def reflection(img):
    h = img.shape[0]
    w = img.shape[1]
    #BGR
    for i in range(h):
        for j in range(int(w/2)):
            # img[i][j], img[i][w-1-j] = img[i][w-1-j], img[i][j] pointers are being copied.So, won't work
            val = img[i][j].copy()
            img[i][j] = img[i][w-1-j]
            img[i][w-1-j] = val
    return img


def grayscale(img):
    h = img.shape[0]
    w = img.shape[1]
    #BGR
    for i in range(h):
        for j in range(w):
            avg = round((img[i][j][0] / 3) + (img[i][j][1] / 3) + (img[i][j][2] / 3))
            for k in range(3):
                # 0 - Blue, 1 - Green, 2 - Red
                img[i][j][k] = avg
    return img

def cap(val):
    if val >= 255:
        return 255
    else:
        return val

def sepia(img):
    h = img.shape[0]
    w = img.shape[1]
    #BGR
    for i in range(h):
        for j in range(w):
            b, g, r = img[i][j][0], img[i][j][1], img[i][j][2]
            r1 = round(0.393 * r + 0.769 * g + 0.189 * b)
            g1 = round(0.349 * r + 0.686 * g + 0.168 * b)
            b1 = round(0.272 * r + 0.534 * g + 0.131 * b)
            img[i][j][0] = cap(b1)
            img[i][j][1] = cap(g1)
            img[i][j][2] = cap(r1)
    return img

def edges(img):
    h = img.shape[0]
    w = img.shape[1]
    outimg = numpy.empty(shape=img.shape)  #BGR
    Gx, Gy = [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], [[-1, -2, -1], [0, 0, 0], [1, 2, 1]]
    for i in range(h):
        for j in range(w):
            for k in range(3):
                valx, valy = 0, 0
                for di in [-1, 0, 1]:
                    for dj in [-1, 0, 1]:
                        if 0 <= i + di < h and 0 <= j + dj < w:
                            valx += (Gx[1 + di][1 + dj] * img[i + di][j + dj][k])
                            valy += (Gy[1 + di][1 + dj] * img[i + di][j + dj][k])
                val = round(sqrt(valx**2 + valy**2))
                outimg[i][j][k] = cap(val)
    return outimg

def blur(img):
    h = img.shape[0]
    w = img.shape[1]
    outimg = numpy.empty(shape=img.shape)  #BGR
    for i in range(h):
        for j in range(w):
            for k in range(3):
                count = 0
                val = 0
                for di in [-1,0,1]:
                    for dj in [-1,0,1]:
                        if 0 <= i + di < h and 0 <= j + dj < w:
                            val += img[i+di][j+dj][k]
                            count += 1
                outimg[i][j][k] = round(val / count)
    return outimg

def main():
    if len(sys.argv) != 4:
        sys.exit("Usage: python3 filter.py [flag] input_image output_image")

    if sys.argv[1] not in ['-r', '-g', '-s', '-e', '-b']:
        sys.exit("Usage: \nFlags are r, g, s, e, b")
    flag = sys.argv[1][1]
    
    try:
        img = cv2.imread(sys.argv[2])
    except:
        sys.exit(f"No file with name {sys.argv[2]}")
    
    flag_dict = {'r': reflection, 'g': grayscale, 's': sepia, 'e': edges, 'b': blur}
    
    output_img = flag_dict[flag](img)
    
    # writing to file
    cv2.imwrite(sys.argv[3], output_img)

    return 0


if __name__ == "__main__":
    main()