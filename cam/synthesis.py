import cv2
from PIL import Image
import numpy as np

src = cv2.imread('pic.png')
mask = cv2.imread('makeMask.png')#, cv2.IMREAD_COLOR)
# maskg = cv2.imread('makeMask.png', cv2.IMREAD_GRAYSCALE)
dst = cv2.imread('tomb2.png')

# # img = Image.open('makeMask.png')
# maskGray = mask.convert('L')
# maskGray.save('makeMask_gray.png')

# cv2.imwrite('makeMask_gray.png',mask)
# maskgray = cv2.imread('makeMask_gray.png', cv2.IMREAD_GRAYSCALE)


mask_hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)

maskg = cv2.cvtColor(mask_hsv, cv2.COLOR_BGR2GRAY)


cv2.imwrite('makeMaskHsv_gray.png',maskg*1.2)

maskgg = cv2.imread('makeMaskHsv_gray.png', cv2.IMREAD_GRAYSCALE)

cv2.copyTo(src, maskgg, dst)

# cv2.imshow('mask_blue', mask_blue)
cv2.imshow('src',src)
# cv2.imshow('mask',mask)
cv2.imshow('dst', dst)
cv2.imshow('maskgg', maskgg)
# cv2.imshow('hsv', hsv)
# cv2.imshow('src', src)


cv2.waitKey()
cv2.destroyAllWindows()
