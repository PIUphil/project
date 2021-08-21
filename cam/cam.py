from pop import Camera
import cv2

cam = Camera(width=1024,height=576)
cv2.imwrite("pic.png", cam.value)
