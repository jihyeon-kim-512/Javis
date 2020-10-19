import requests
import json
import urllib.request

# 네트워크 관련
import urllib

# 웹 문서 분석 관련
from bs4 import BeautifulSoup
import bs4.element

# 자연어 처리 관련
from gensim.summarization.summarizer import summarize

# 시간 관련
import datetime



import pickle
import os
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# 1-1. 구글 인증
# 클라이언트 ID 파일을 가져와서 새창으로 로그인을 통해 토큰을 생성합니다.
# 이미 토큰이 있다면 로그인 작업은 건너뜁니다.
def get_google_auth():
    # 구글 OAuth 클라이언트 ID Json 파일
    directory = 'auth'
    creds_filename = 'client_secret_422511621553-ner5kv45f8o7eec66cl527jf7l6h5j2k.apps.googleusercontent.com.json'
    token_filename = 'gtoken.pickle'
    
    # 캘린더에서 사용할 권한
    SCOPES = ['https://www.googleapis.com/auth/calendar']
    
    # 새로운 창에서 로그인 하시면 인증 정보를 얻게 됩니다.
    creds = None
    
    # 이미 생성한 인증 토큰이 존재하면 사용합니다.
    if os.path.exists(os.path.join(directory, token_filename)):
        with open(os.path.join(directory, token_filename), 'rb') as token:
            creds = pickle.load(token)
    
    # 이미 생성한 인증 토큰이 유효한지 체크합니다.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # 인증 토큰이 없을 경우 생성. 새 창에서 로그인 필요
            flow = InstalledAppFlow.from_client_secrets_file(
               os.path.join(directory, creds_filename) , SCOPES)
            creds = flow.run_local_server(port=0)
        # 토큰 저장
        with open(os.path.join(directory, token_filename), 'wb') as token:
            pickle.dump(creds, token)
    return creds

# 1-2. 카카오톡 인증
def get_kakao_auth(access_token, rest_key):
    return {
      "access_token" : access_token,
      "rest_key" : rest_key
    }

# 1-3. 네이버 인증
def get_naver_auth(client_id, client_secret):
    return {
      "client_id" : client_id,
      "client_secret" : client_secret
    }


# 1-1. 구글 인증
gcreds = get_google_auth()
# 구글 서비스를 사용하게 하는 객체
service = build('calendar', 'v3', credentials=gcreds)

# 1-2. 카카오 인증
# https://developers.kakao.com/docs/restapi/tool
# 해당 사이트에서 로그인 후 'Access token'을 얻어오세요
# 앱 페이지에서 REST API KEY 를 얻어오세요
access_token = "5HloZOo7Wp2IHj4o-uNOmyIUFyRUkpYQYjw3PgopcJ4AAAFzkwLcAw"
rest_key =  "dbbadbe804f295f7da88212ccff2f83f"
kcreds = get_kakao_auth(access_token, rest_key)

# 카카오 서비스에 인증 키를 보낼 때 쓰는 headers
kheaders = {
    "Authorization": "Bearer " + kcreds.get('access_token')
}

# 1-3. 네이버 인증
# https://developers.naver.com/apps
# 해당 사이트에서 로그인 후 "Cliend ID"와 "Client Secret"을 얻어오세요
client_id = "vH30MBZOOyXkZtIWlPkt"
client_secret = "H85Mc72H_R"
ncreds = get_naver_auth(client_id, client_secret)

# 네이버 서비스에 인증키를 보낼 때 쓰는 headers
nheaders = {
    "X-Naver-Client-Id" : ncreds.get('client_id'),
    "X-Naver-Client-Secret" : ncreds.get('client_secret')
}



       

def do_news_project():
    #################################################
    # 1. 네이버 상위 뉴스 크롤링하기
    #################################################
    # sections :
    # {'eco' : '경제','soc' : '사회','lif' : '생활/문화','wor' : '세계','its' : 'IT/과학'}
    news_dic = get_naver_news_top3()

    # news_dic['eco'][0].keys()
    # dict_keys(['link', 'news_body', 'image_url'])
    # title : 뉴스 제목
    # views : 조회수
    # link : 뉴스 URL
    # news_body : 뉴스 내용
    # image_url : 이미지 URL
    
    #################################################
    # 2. 뉴스 요약하기
    #################################################
    
    # 마이크 세팅 - 에너지 임계점 설정
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        print("소음 수치 반영하여 음성을 청취합니다. {}".format(recognizer.energy_threshold))
        print("카테고리를 선택해주세요~~")
        
        
    with microphone as source:
        audio_data = recognizer.listen(source)
        audio = audio_data.get_raw_data()
    
    res = requests.post(kakao_speech_url, headers=headers, data=audio)
    
    print(res.text)
    
    result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    result = json.loads(result_json_string)
    
    print(result)
    print(result['value'])
    
    
    
    KEYWORD_ECO = '경제'
    KEYWORD_SOC = '사회'
    KEYWORD_LIF = '생활'
    KEYWORD_CUL = '문화'
    KEYWORD_WOR = '세계'
    KEYWORD_IT = '아이티'
    KEYWORD_SC = '과학'
    
    # 명령어
    command = result.get('value')
    
    print('입력한 명령 : ' + command)
    print('명령을 수행합니다.')
    
    if KEYWORD_ECO in command:
        my_section = 'eco'
    elif KEYWORD_SOC in command:
        my_section = 'soc'
    elif KEYWORD_LIF or KEYWORD_CUL in command:
        my_section = 'lif'
    elif KEYWORD_WOR in command:
        my_section = 'wor'
    elif KEYWORD_IT or KEYWORD_SC in command:
        my_section = 'its'
    else:
        print('명령을 알 수 없습니다.')
    
    # 2-1. 뉴스 목록 정하기
    
    news_list3 = news_dic[my_section]
    
    # 2-2. 뉴스 요약하기
    for news_info in news_list3:

        snews_body = summarize(news_info['news_body'], word_count=20)

        # 뉴스 본문이 10 문장 이하일 경우 결과가 반환되지 않음.
        # 이때는 요약하지 않고 본문에서 앞 3문장을 사용함.
        if not snews_body:
            news_sentences = news_info['news_body'].split('.')

            if len(news_sentences) > 3:
                snews_body = '.'.join(news_sentences[:1])
            else:
                snews_body = '.'.join(news_sentences)

        news_info['snews_body'] = snews_body
        
        print(" " + news_info['snews_body'] + "\n")
        
    #################################################
    # 3. 카카오톡 보내기
    #################################################
    # 카카오톡 API URL
    kakaotalk_template_url = "https://kapi.kakao.com/v2/api/talk/memo/default/send"
    
    # 3-1. 카카오톡 보내기 - 리스트 템플릿
    # 사용자가 선택한 카테고리를 제목에 넣기 위한 dictionary
    sections_ko = {'eco' : '경제', 'soc' : '사회',
                'lif' : '생활/문화', 'wor' : '세계',
                'its' : 'IT/과학'}

    # 네이버 뉴스 URL
    navernews_url = "https://news.naver.com/main/ranking/popularDay.nhn?mid=etc&sid1=111"

    # 각 리스트에 들어갈 내용(content) 만들기
    contents = []
    for news_info in news_list3:
        title = news_info.get('title')
        views = news_info.get('views')
        link = news_info.get('link')
        snews_body = news_info.get('snews_body')
        image_url = news_info.get('image_url')

        content = {
            "title" : title,
            "description" : "조회수 : " + views,
            "image_url" : image_url,
            "image_width" : 50, "image_height" : 50,
            "link": {
                "web_url": link,
                "mobile_web_url": link
            }
        }

        contents.append(content)

    # 리스트 템플릿 형식 만들기
    template = {
        "object_type" : "list",
        "header_title" : sections_ko[my_section] + " 분야 상위 뉴스 빅3",
        "header_link" : {
            "web_url": navernews_url,
            "mobile_web_url" : navernews_url
        },
        "contents" : contents,
        "button_title" : sections_ko[my_section] + " 분야 모두 보기"
    }

    # JSON 형식 -> 문자열 변환
    payload = {
        "template_object" : json.dumps(template)
    }

    # 카카오톡 보내기
    res = requests.post(kakaotalk_template_url, data=payload, headers=kheaders)

    if res.json().get('result_code') == 0:
        print('상위 3개의 뉴스를 성공적으로 보냈습니다.')
    else:
        print(f'상위 3개의 뉴스를 성공적으로 보내지 못했습니다. 오류메시지 : {str(res.json())}')
    
    
    
    # 3-2. 카카오톡 보내기 - 텍스트 템플릿
    # 3번에 걸쳐 각 뉴스의 요약 결과를 보냅니다.
    for idx, news_info in enumerate(news_list3):
        title = news_info.get('title')
        views = news_info.get('views')
        link = news_info.get('link')
        snews_body = news_info.get('snews_body')
        image_url = news_info.get('image_url')

        # 글 내용
        text = '# 제목 : ' + title + \
                '\n\n# 요약 : ' + snews_body

        # 텍스트 템플릿 형식 만들기
        template = {
          "object_type": "text",
          "text": text,
          "link": {
            "web_url": link,
            "mobile_web_url": link
          },
          "button_title": "자세히 보기"
        }

        # JSON 형식 -> 문자열 변환
        payload = {
        "template_object" : json.dumps(template)
        }

        # 카카오톡 보내기
        res = requests.post(kakaotalk_template_url, data=payload, headers=kheaders)

        if res.json().get('result_code') == 0:
            print(f'index {str(idx)} 뉴스를 성공적으로 보냈습니다.')
        else:
            print(f'index {str(idx)} 뉴스를 성공적으로 보내지 못했습니다. 오류메시지 : {str(res.json())}')


# 최신 뉴스 가져오기 코드

# '경제', '사회', '생활/문화', '세계', 'IT/과학'
# 각 분야의 상위 3개 뉴스들을 가져옵니다. (5분야 * 3개 = 15개)
def get_naver_news_top3():
    # 뉴스를 가져올 링크 주소 지정
    base_url = "https://news.naver.com"
    today = datetime.datetime.today().strftime('%Y%m%d')
    news_params = "/main/ranking/popularDay.nhn?rankingType=popular_day&date=" + today + "&sectionId="
    
    # 뉴스 결과를 담아낼 dictionary
    news_dic = dict()
    
    # sections : '경제', '사회', '생활/문화', '세계', 'IT/과학'
    # section_ids :  URL에 사용될 뉴스  각 부문 ID
    sections = ["eco","soc","lif","wor","its"]
    section_ids = ["101","102","103","104","105"]
    for sec, sid in zip(sections, section_ids):
        # 해당 분야 상위 뉴스 목록 주소
        news_link = base_url + news_params + sid
        
        # 해당 분야 상위 뉴스 HTML 가져오기
        res = requests.get(news_link)
        soup = BeautifulSoup(res.text,'lxml')
        
        # 해당 분야 상위 뉴스 3개 가져오기
        lis3 = soup.find_all('li', class_='ranking_item', limit=3)
        
        # 가져온 뉴스 데이터 정제하기
        news_list3 = []
        default_img = "https://search.naver.com/search.naver?where=image&sm=tab_jum&query=naver#"
        for li in lis3:
            news_link = base_url + li.a.attrs.get('href')
            
            res = requests.get(news_link)
            soup = BeautifulSoup(res.text,'lxml')
            body = soup.find('div', class_="_article_body_contents")
            
            # 뉴스 본문 가져오기
            news_body = ''
            for content in body:
                if type(content) is bs4.element.NavigableString and len(content) > 50:
                    news_body += content.strip() + ' '
                    # news_body += content.strip()
                    # 뉴스 요약할 때, '.' 마침표 뒤에 한칸 띄워주지 않으면 문장을 구분 못하는 경우가 있음
                        
            # title : 뉴스 제목
            # views : 조회수
            # link : 뉴스 URL
            # news_body : 뉴스 내용
            # image_url : 이미지 URL
            news_info = {
                "title" : li.a.attrs.get('title'),
                "views" : li.find('div', class_="ranking_view").text,
                "link" : news_link,
                "news_body" : news_body,
                "image_url" : li.img.attrs.get('src') if li.img else default_img
            }
            
            news_list3.append(news_info)

        news_dic[sec] = news_list3
    
    return news_dic
        

kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

rest_api_key = 'dbbadbe804f295f7da88212ccff2f83f'

headers = {
    "Content-Type": "application/octet-stream",
    "X-DSS-Service": "DICTATION",
    "Authorization": "KakaoAK " + "dbbadbe804f295f7da88212ccff2f83f",
}

#with open('heykakao.wav', 'rb') as fp:
#    audio = fp.read()

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
    
    
with microphone as source:
    audio_data = recognizer.listen(source)
    audio = audio_data.get_raw_data()

res = requests.post(kakao_speech_url, headers=headers, data=audio)

print(res.text)

result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
result = json.loads(result_json_string)

print(result)
print(result['value'])



KEYWORD_CALENDAR = '일정'
KEYWORD_NEWS = '뉴스'

# 명령어
command = result.get('value')

print('입력한 명령 : ' + command)
print('명령을 수행합니다.')

if KEYWORD_CALENDAR in command:
    print('일정을 파악하여 맛집을 추천합니다.')
    do_calendar_project()
elif KEYWORD_NEWS in command:
    print('최신 뉴스를 요약합니다.')
    do_news_project()
    
else:
    print('명령을 알 수 없습니다.')
    

#사용할 라이브러리 불러오기
    
    






    


