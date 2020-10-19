# 마이크 세팅
import speech_recognition as sr

# 오디오 파일 / 마이크에서 음성을 추출하는 객체
recognizer = sr.Recognizer()

# 마이크를 다루는 객체
microphone = sr.Microphone(sample_rate=16000)

# 마이크 세팅 - 에너지 임계점 설정
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    print("소음 수치 반영하여 음성을 청취합니다. {}".format(recognizer.energy_threshold))
    
# 소음 수치 반영하여 음성을 청취합니다. 199.67706126141093
    
# 음성 입력
with microphone as source:
    audio_data = recognizer.listen(source)
audio = audio_data.get_raw_data()