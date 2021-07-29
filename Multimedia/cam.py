import cv2
import sys

cam_cmd = lambda cam_with=1280, cam_height=720, win_with=1280, win_height=720, rate=60, flip=0 : ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width={0}, height={1}, '
            'format=NV12, framerate={2}/1 ! '
            'nvvidconv flip-method={3} ! '
            'video/x-raw, width={4}, height={5}, '
            'format=BGRx ! '
            'videoconvert ! appsink').format(cam_with, cam_height, rate, flip, win_with, win_height)

cam = cv2.VideoCapture(cam_cmd(), cv2.CAP_GSTREAMER)        # 엔비디아 - GSTREAMER / 다른제품은 카메라번호

if not cam.isOpened():
    print("can't open the CAM0")
    sys.exit()

while True:
    #ret, frame = cam.read()     # ret = True/False
    _, frame = cam.read()
    #if ret:
    cv2.imshow("preview", frame)
    if cv2.waitKey(10) >= 0:        # 10: 시간(milliSec)   # 종료
        break

cam.release()                   # 필수!! # 해제를 제대로 해야 다음에 다시 실행가능
cv2.destroyWindow('preview')    # 메모리 지움

# 종료할 때 화면누르고 아무키나 누름.. Ctrl+C 하지말고..
