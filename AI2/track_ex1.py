from pop import Pilot 
import cv2

cam_cmd = lambda cam_width=224, cam_height=224, win_width=224, win_height=224, rate=60, flip=0 : ('nvarguscamerasrc ! '
            'video/x-raw(memory:NVMM), '
            'width={0}, height={1}, '
            'format=NV12, framerate={2}/1 ! '
            'nvvidconv flip-method={3} ! '
            'video/x-raw, width={4}, height={5}, '
            'format=BGRx ! '
            'videoconvert ! appsink').format(cam_width, cam_height, rate, flip, win_width, win_height)

cam = cv2.VideoCapture(cam_cmd(), cv2.CAP_GSTREAMER)

bot = Pilot.SerBot() 

of = Pilot.Object_Follow2(cam)
of.load_model()

print(">>>", "Successful model...")

while True:
    try:
        h, _ = of.detect(index='person')
        print('###', h)
        
        if h is not None: 
            steer = h['x'] * 4 
            if steer > 1:
                steer = 1
            elif steer < -1:
                steer = -1
            
            bot.steering = steer

            if h['size_rate'] < 0.2:
                bot.forward(50)
            else:
                bot.stop()
        else:
            bot.stop()
        
    except:
        break
    
bot.stop()
cam.release()
