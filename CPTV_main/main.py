import threading
from socket import *
import time
import CPTV

# socket
HOST = '192.168.0.42'
PORT = 22042
ADDR = (HOST, PORT)

if __name__ == '__main__':
    try:
        clientSocket = socket(AF_INET, SOCK_STREAM)     # 서버에 접속하기 위한 소켓을 생성한다.
        clientSocket.connect(ADDR)  # 서버에 접속을 시도한다.
        print('Socket connect')

        # 모듈 객체 생성
        p1 = CPTV.WatchingStranger(clientSocket)
        p2 = CPTV.VoiceDetection(clientSocket)

        # Threading
        t1 = threading.Thread(target=p1.main, args=(1,))
        t2 = threading.Thread(target=p2.main, args=(2,))
        t1.daemon = True
        t2.daemon = True

        t1.start()
        t2.start()

        while True:
            time.sleep(1)  # thread 간의 우선순위 관계 없이 다른 thread에게 cpu를 넘겨줌(1 일때)
            pass  # sleep(0)은 cpu 선점권을 풀지 않음

    except Exception as e:
        # 소켓 종료
        clientSocket.send(str(e).encode())  # 서버에 메시지 전달
        clientSocket.close()
