import cv2
import time

class RecordVideo():
    def __init__(self, saveTime=30):
        self.saveTime = saveTime

        self.prevLock = True
        self.cap = cv2.VideoCapture(0)

        if not self.cap.isOpened():
            print("Camera open failed!")
            exit()

        # fourcc 값 받아오기, *는 문자를 풀어쓰는 방식, *'mp4v' == 'm', 'p', '4', 'v'
        self.fourcc = cv2.VideoWriter_fourcc(*'mp4v')

        # self.main()

    def recordCam(self, state):
        if state == 'prev':
            self.prevLock = True
        else:
            self.prevLock = False

        try:
            videoName = state + 'Cam.mp4'
            recorder = cv2.VideoWriter(videoName, self.fourcc, 30, (640, 480))

            if not recorder.isOpened():
                print(state + 'video File open failed!')
                self.cap.release()
                exit()

            stime = time.time()
            while True:
                if (time.time() - stime) > self.saveTime:
                    break

                ret, frame = self.cap.read()  # 카메라의 ret, frame 값 받아오기
                if not ret:
                    break

                recorder.write(frame)
                cv2.imshow(state, frame)
                if cv2.waitKey(1) & 0xFF == 27:  # esc를 누르면 강제 종료
                    break
            recorder.release()
            cv2.destroyAllWindows()

            if state == 'prev':
                self.prevLock = False
            else:
                self.prevLock = True

        except Exception as e:
            print(e)
            pass

    def main(self):
        try:
            while True:  # 무한 루프
                if self.prevLock:
                    self.recordCam('prev')
                elif not self.prevLock:
                    self.recordCam('cur')
        except Exception as e:
            self.cap.release()
            print(e)

if __name__ == '__main__':
    startRecord = RecordVideo(saveTime=3)
    startRecord.main()
