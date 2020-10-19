#pip install SpeechRecognition

import speech_recognition as sr

# 음성파일을 통한 음성인식
#AUDIO_FILE = "hello.wav"
#
## audio file을 audio source로 사용합니다
#r = sr.Recognizer()
#with sr.AudioFile(AUDIO_FILE) as source:
#    audio = r.record(source)  # 전체 audio file 읽기
#
## 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
#try:
#    print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
#except sr.UnknownValueError:
#    print("Google Speech Recognition could not understand audio")
#except sr.RequestError as e:
#    print("Could not request results from Google Speech Recognition service; {0}".format(e))
#    
## 결과
## Google Speech Recognition thinks you said : 안녕하세요 오늘도 멋진 하루 되세요




# microphone에서 auido source를 생성합니다
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# 구글 웹 음성 API로 인식하기 (하루에 제한 50회)
try:
    print("Google Speech Recognition thinks you said : " + r.recognize_google(audio, language='ko'))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))
    
# 결과
# Google Speech Recognition thinks you said : 안녕하세요
    
    
# write audio to a WAV file
with open("microphone-results.wav", "wb") as f:
    f.write(audio.get_wav_data())