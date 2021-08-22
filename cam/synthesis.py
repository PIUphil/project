import cv2

src = cv2.imread('pic.png')             # 원본사진
mask = cv2.imread('makeMask.png')       # 마스크이미지 - imgcut.py
dst = cv2.imread('tomb2.png')           # 배경1
dst2 = cv2.imread('crown.png')          # 배경2

# 사이즈 변경 
src = cv2.resize(src, (1024, 576))
mask = cv2.resize(mask, (1024, 576))
dst = cv2.resize(dst, (1024, 576))
dst2 = cv2.resize(dst2, (1024, 576))

# mask_hsv = cv2.cvtColor(mask, cv2.COLOR_BGR2HSV)        # 색채변환(hsv)
# maskg = cv2.cvtColor(mask_hsv, cv2.COLOR_BGR2GRAY)      # 흑백처리

# cv2.imwrite('makeMaskHsv_gray.png',maskg*1.5)           # 대비값 증가

# maskgg = cv2.imread('makeMaskHsv_gray.png', cv2.IMREAD_GRAYSCALE)

cv2.copyTo(src, mask, dst)

# cv2.imshow('src',src)
# cv2.imshow('mask', mask)
cv2.imshow('dst', dst)


cv2.waitKey()
cv2.destroyAllWindows()
