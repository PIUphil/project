from pop import IMU, time, xnode

xnode.atcmd('NI', "IMU_Sender")
xnode.atcmd('CE', 0x00)             # 0번 - 라우터
xnode.atcmd('ID', 0x25)             # 코디네이터와 같은 번호. 유일해야 함
xnode.atcmd('JV', 0x01)             # Joint Variable
xnode.atcmd('WR')

imu = IMU()

while True:
    acc = imu.accel()
    gyro = imu.gyro()
    
    msg = "%.2f, %.2f, %.2f, "%(acc)        # 문자열 결합  // 뒤의 % 형식인자 결합연산자  // 소수점 2자리씩 잘라서 옮겨담음 - 파싱
    msg += "%.2f, %.2f, %.2f"%(gyro)
    
    xnode.transmit(xnode.ADDR_COORDINATOR, msg)     # 상대방의 주소(맥주소) # 0013A200 41AEF51D 
    time.sleep(.1)
