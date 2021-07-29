from popAssist import create_conversation_stream
from popAssist import GAssistant

def onAction(text):         # 핸들러 함수 (콜백함수)
    print(text)
    return True             # True: 오디오 응답 안함 
    
def onStart():
    print(">>> Start recording...")


stream = create_conversation_stream()
ga = GAssistant(stream, local_device_handler=onAction)

while True:
    try:
        ga.assist(onStart)

    except KeyboardInterrupt:
        break

stream.close()
