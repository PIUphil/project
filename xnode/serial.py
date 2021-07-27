from sys import stdin, stdout   # uPy에서 표준입출력   # 내부인식이 잘 안되서 밖에 놓음,,

class Serial:
    def __init__(self):
        pass
        
    def __del__(self):
        pass
    
    #def open(self):         # 호환이 되게끔 하기위해 비어있는(pass) 함수 만듦
    #    pass
        
    def read(self, size=-1):
        #return stdin.buffer.readline().decode() # bytearray -> uni-code /default:'utf-8'
        return stdin.buffer.read(size)      # size: -1 버퍼에 저장하지않고 바로 반환(1byte씩)
                                        
    def readline(self):
        data = b''              # bytearray
        while True:
            t = self.read()
            if t:
                if t==b'\n':
                    break
                else:
                    data += t
        return data                         
                                        
    def write(self, data):
        stdout.write(bytearray(data))           # data.encode()