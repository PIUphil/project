import time
from pop.Pilot import SerBot

bot = SerBot()            # Pilot모듈 안의 SerBot클래스

if False:
    bot.move(90, 40)        # 정면보고 오른쪽이동 / 속도40
    time.sleep(2)
    bot.move(0, 99)         # 직진 / 속도99
    time.sleep(2)
    bot.stop()

if False:
    bot.forward(90)
    bot.steering = -1       # 좌회전
    time.sleep(2)
    bot.steering = 1        # 우회전
    time.sleep(2)
    bot.stop()

from pop.CAN import OmniWheel           # CAN통신

omni = OmniWheel()
omni.forward([50,50,50])   # 모터를 앞쪽으로 회전 (3개모터 모두 앞으로 회전하면 제자리 회전하게됨)
time.sleep(3)
omni.backward([90,90,90])
time.sleep(3)
omni.stop()
