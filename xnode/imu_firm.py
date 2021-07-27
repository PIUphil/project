from pop import IMU, time
from serial import Serial


#imu = IMU()
ser = Serial()       # 객체를 만들면 self에 적용이 됨. 'this->' / 인터프리터가 넣어줌

while True:
    ret = ser.read()
    if ret:
        if ret == b'a':
            ser.write("Accel\n")
        elif ret == b'x':
            ser.write("Xyro\n")
        elif ret == b'q':
            ser.write("Quart\n")
        else:
            ser.write(ret)
    
    time.sleep(0.1)
            
    #ret = ser.readline()        
    #ser.write(ret)              # echo-test

ser.write("hi")

"""while True:
    ac = imu.accel()        # 전부 리스트로 넘어옴, (x,y,z)
    gy = imu.gyro()
    ma = imu.magnetic()
    qu = imu.quat()         # 절대위치 알려줌. 값4개 반환
    msg = ""

    for data in ac, gy, ma:
        msg += ("%.2f, " * 3)%(data)

    msg += (("%.2f " * 4)%(qu)) #+ "\n"

    #uart.write(msg)
    print(msg)

    time.sleep(0.1)"""