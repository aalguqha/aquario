import cv2
from matplotlib import pyplot as plt
import numpy as np


def scl(image, s=2):
    return cv2.resize(image, (0, 0), fx=s, fy=s)


def process_image(fname):
    img = cv2.imread(fname, cv2.IMREAD_COLOR)
    # cv2.imshow('img', img)
    # cv2.waitKey()
    count = 1

    #crop the image
    img = img[110:430, 180:440]
    cv2.imshow('img', scl(img))
    cv2.imwrite('step_{}.jpg'.format(count), img)
    count += 1
    cv2.waitKey()

    # plt.imshow(img)
    # plt.show()

    # apply mask to isolate ROI
    roi = np.zeros(img.shape, np.uint8)
    roi[155:220, :] = img[155:220, :]
    
    cv2.imshow('img', scl(roi))
    cv2.imwrite('step_{}.jpg'.format(count), roi)
    count += 1

    cv2.waitKey()

    grayRoi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(grayRoi, 250, 255, cv2.THRESH_BINARY)
    
    cv2.imshow('img', scl(thresh))
    cv2.imwrite('step_{}.jpg'.format(count), thresh)
    count += 1 
    cv2.waitKey()

    #find the largest contour in the mask
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(contours, key=cv2.contourArea)  
    
    # compute the center of the contour
    M = cv2.moments(c)
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])

    cv2.circle(img, (cX, cY), 10, (0, 255, 0), 1)
    font = cv2.FONT_HERSHEY_SIMPLEX

    bottomLeftCornerOfText = (cX+10, cY-10)
    fontScale = 0.5
    fontColor = (0, 255, 0)
    lineType = 2

    cv2.putText(img, str((cX, cY)),
            bottomLeftCornerOfText,
            font,
            fontScale,
            fontColor,
            1)

    cv2.imshow('img', scl(img))
    cv2.imwrite('step_{}.jpg'.format(count), img)
    count += 1
    cv2.waitKey()
    cv2.destroyAllWindows()
    return (cX, cY) # return center of LED

def main():
    process_image('misc/led_mount.png')


if __name__ == '__main__':
    main()
