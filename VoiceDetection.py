import time
import speech_recognition as sr

class VoiceDetection():
    def __init__(self, socket):
        self.socket = socket

        self.init_rec = sr.Recognizer()
        self.wordList = ['경찰', '불러', '살려',
                    '무서워', '제발', '누구',
                    '그만', '어딜', '도망',
                    '뭐야', '놔', '놓으',
                    '뭐야', '죽을', '죽어',
                    '뒤질', '뒤지고', '맞을',
                    '따라와', '따라', '조용',
                    '닥쳐', '죽여', '살고',
                    '싫어', '하지마', '하지'
                    '아파', '때려', '때리']

        # protocol message
        self.message = protocolMsg(id=1, level=4, length=0)

        print("Let's speak!!")

    def parseVoice(self):
        try:
            with sr.Microphone() as source:
                print("Tell something")
                audio_data = self.init_rec.record(source, duration=5)
                print("Recognizing your text.............")
                text = self.init_rec.recognize_google(audio_data, language='ko-KR')

                # text에 경찰이라는 단어가 포함되면 위치를 출력(0 이상), 아니면 -1 출력
                sign = text.split(' ')  # 띄어쓰기 기준으로 파싱

                for word in sign:  # sign 리스트 인덱스 요소를 하나식 반환
                    wordDetection = list(filter(lambda x: word in x, self.wordList))
                    if wordDetection:
                        self.socket.send(self.message)
                        print(word)
                        break

        except Exception as e:
            print(e)
            pass

    def main(self):
        try:
            while True:
                self.parseVoice()
        except Exception as e:
            print(e)
