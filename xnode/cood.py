from pop import xnode
from pop import time

xnode.atcmd('NI', "IMU_Receiver")         # 네트워크 식별이름 - 길게쓰지말기
xnode.atcmd('CE', 0x01)                   # 01번 - Coordinator Enable
xnode.atcmd('ID', 0x25)             # 라우터가 어디에 붙을지 모름 -> 수동으로 설정(25번)  # 기억해두기
xnode.atcmd('WR')                         # 세팅 저장

while True:
    msg = xnode.receive()
    if msg:
        print(msg['payload'].decode('utf-8'))           # 2byte -> 파이썬 스트링문자로 변환
    else:
        time.sleep(0.1)
