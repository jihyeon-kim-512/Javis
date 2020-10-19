import requests
import json
import speech_recognition as sr
import os
import time


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


import tkinter
from PIL import ImageTk, Image
import webbrowser




# 1-1. 구글 인증
# 클라이언트 ID 파일을 가져와서 새창으로 로그인을 통해 토큰을 생성합니다.
# 이미 토큰이 있다면 로그인 작업은 건너뜁니다.
def get_google_auth():
    # 구글 OAuth 클라이언트 ID Json 파일
    directory = 'auth'
    creds_filename = 'gcredentials.json'
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
access_token = "tMfrpQEBgfqKSRQAHU6_qnJWBz1a_AD7-IIseQorDR8AAAFzkwYcnw"
rest_key =  "f906f76f8956eb053a9a621a4d52b704"
kcreds = get_kakao_auth(access_token, rest_key)

# 카카오 서비스에 인증 키를 보낼 때 쓰는 headers
kheaders = {
    "Authorization": "Bearer " + kcreds.get('access_token')
}

# 1-3. 네이버 인증
# https://developers.naver.com/apps
# 해당 사이트에서 로그인 후 "Cliend ID"와 "Client Secret"을 얻어오세요
client_id = "mltgGJSIGvKq5Z_Eae5G"
client_secret = "BY5R3ftEWB"
ncreds = get_naver_auth(client_id, client_secret)

# 네이버 서비스에 인증키를 보낼 때 쓰는 headers
nheaders = {
    "X-Naver-Client-Id" : ncreds.get('client_id'),
    "X-Naver-Client-Secret" : ncreds.get('client_secret')
}





def do_calendar_project():
    service = build("calendar", "v3", credentials = gcreds)
    calendar_id = "primary"
    today = datetime.date.today().isoformat()
    time_min = today + "T00:00:00+09:00"
    time_max = today + "T23:59:59+09:00"
    max_results = 1
    is_single_events = True
    orderby = "startTime"
    
    events_result = service.events().list(calendarId = calendar_id,
                                   timeMin = time_min,
                                   timeMax = time_max,
                                   maxResults = max_results,
                                   singleEvents = is_single_events,
                                   orderBy = orderby).execute()

    items = events_result.get("items")
    print(today, "일정 목록입니다.")
    for idx, item in enumerate(items) :
        print('=' * 10, idx + 1, '번째 일정', '=' * 10)
        print('일정 제목 :',item['summary'])
    
    item = items[0]

    # 일정 제목
    gsummary = item.get('summary')

    gcategory, glocation = gsummary[gsummary.index('[')+1 : gsummary.index(']')].split('-')

    # 해당 구글 캘린더 일정 연결 링크
    gevent_url = item.get('htmlLink')

    gaddress = item.get('location')
    
    if ',' in gaddress:
        gaddress = gaddress.split(',')[1].strip()
        
    enc_location = urllib.parse.quote(glocation + "맛집")
    
    nparams = "sort=comment&query=" + enc_location

    # 네이버 지역 검색 주소 및 검색할 정보
    naver_local_url = "https://openapi.naver.com/v1/search/local.json?" + nparams

    # 네이버에 일정 장소 주변 맛집을 검색합니다.
    res = requests.get(naver_local_url, headers=nheaders)

    if res.status_code != 200:
        print('네이버 인증에 실패하였습니다.')
        return None
    
    # 검색 결과로 받아온 10개의 결과
    places = res.json().get('items')
    
    if len(places) < 1:
        print('맛집 검색 결과가 잘못되었습니다.')
        print(res.text)
        return None
    #print(res.text)
    
    win = tkinter.Tk()
    win.title('**일정관리**')
    win.geometry('900x600')    
    wall = ImageTk.PhotoImage(file = "schedule.gif") 
    wall_label = tkinter.Label(image = wall) 
    wall_label.place(x = -2,y = -2) 
    
    contents = []
    for place in places[:3]:
        ntitle = place.get('title')  # 장소 이름
        ncategory = place.get('category')  # 장소 카테고리
        ntelephone = place.get('telephone')  # 장소 전화번호
        nlocation = place.get('address')  # 장소 지번 주소

        # 각 장소를 클릭할 때 네이버 검색으로 연결해주기 위해 작성된 코드
        enc_location = urllib.parse.quote(nlocation + ' ' + ntitle)
        query = "query=" + enc_location

        # 장소 카테고리가 카페이면 카페 이미지
        # 이외에는 음식 이미지
        
        # 전화번호가 있다면 제목과 함께 넣어줍니다.
        if ntelephone:
            ntitle = ntitle + "\ntel) " + ntelephone
        
        
    enc_gaddress = urllib.parse.quote(gaddress)
    query = "query=" + enc_gaddress
    gaddr_url = "https://search.naver.com/search.naver?" + query
    template = {
        "header_title" : "%s" % gsummary,
        "header_purpose" : "맛집 추천",
        "header_link" : {
            "web_url": gevent_url
        }
    }
    print(template)
    lbl = tkinter.Label(win, text = item['summary'], borderwidth = 1,bg = "white",font=("맑은 고딕", 10), width=20, height=1, anchor='n', justify='left', wraplength=200)
    lb2 = tkinter.Label(win, text = places[0]['title'],bg="white", font=("맑은 고딕", 10), width=30, height=2, anchor='n', justify='left', wraplength=200)
    lb3 = tkinter.Label(win, text = places[0]['category'],bg="white", font=("맑은 고딕", 10), width=30, height = 2, anchor='n', justify='left', wraplength=200)
    lb4 = tkinter.Label(win, text = places[0]['address'],bg="white", font=("맑은 고딕", 10), width=30, height=2, anchor='n', justify='left', wraplength=200)
    link1 = tkinter.Label(win, text = places[0]['link'],  fg = "blue",bg="white", font=("맑은 고딕", 8), cursor="hand2", width=35, height=2, anchor='n', justify='left', wraplength=200)
    
    lbl.pack()
    lb2.pack()
    lb3.pack()
    lb4.pack()
    link1.pack()
    
    def link1_btn(event) :
        webbrowser.open_new("\""+places[0]['link'] +"\"")
       
    link1.bind("<Button>", link1_btn)
    
    lbl.place(x=155, y=215)    
    lb2.place(x=380, y=350)
    lb3.place(x=380, y=375)
    lb4.place(x=380, y=400)
    link1.place(x=380, y=450)
    
    
    win.mainloop()




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
        print("==============================================================")
        print("카테고리를 선택해주세요 (경제/사회/생활/문화/세계/IT/과학)")
        print("==============================================================")
        print("소음 수치 반영하여 음성을 청취합니다. {}".format(recognizer.energy_threshold))
        
        
        
    with microphone as source:
        audio_data = recognizer.listen(source)
        audio = audio_data.get_raw_data()
    
    res = requests.post(kakao_speech_url, headers=headers, data=audio)
    
#    print(res.text)
    
    result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
    result = json.loads(result_json_string)
    
#    print(result)
#    print(result['value'])
    
    
    
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
    elif KEYWORD_LIF in command:
        my_section = 'lif'
    elif KEYWORD_CUL in command:
        my_section = 'lif'
    elif KEYWORD_WOR in command:
        my_section = 'wor'
    elif KEYWORD_IT in command:
        my_section = 'its'
    elif KEYWORD_SC in command:
        my_section = 'its'
    else:
        print('명령을 알 수 없습니다.')
    
    # 2-1. 뉴스 목록 정하기
    news_list3 = news_dic[my_section]
    
    #print(news_list3)
    
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
        
        print("**" + news_info['title'])
        print(" " + news_info['snews_body'])
        print(" {" + news_info['image_url'] + "} ")
            
        
    win = tkinter.Tk()
    win.title('**뉴스요약**')
    win.geometry('1000x525')    
    wall = ImageTk.PhotoImage(file = my_section + ".gif") 
    wall_label = tkinter.Label(image = wall) 
    wall_label.place(x = -2,y = -2) 
    


    contents = []
    for news_info in news_list3:
        title = news_info.get('title')
        link = news_info.get('link')
        snews_body = news_info.get('snews_body')

        content = {
            "title" : title,
            "snews_body" : snews_body,
            "link": {
                "web_url": link,
                "mobile_web_url": link
            }
        }

        contents.append(content)
    
    def link1_btn(event) :
        webbrowser.open_new("\""+contents[0]['link']['web_url'] +"\"")
        
    def link2_btn(event) :
        webbrowser.open_new("\""+contents[1]['link']['web_url'] +"\"")
        
    def link3_btn(event) :
        webbrowser.open_new("\""+contents[2]['link']['web_url'] +"\"")
        
    #print(contents)      
    lbl = tkinter.Label(win, text = contents[0]['title'], bg = "white", font=("맑은 고딕", 10, 'bold'), width=26, height=2, anchor='n', justify='left', wraplength=200)
    lb2 = tkinter.Label(win, text = contents[0]['snews_body'],bg="white", font=("맑은 고딕", 10), width=30, height=10, anchor='n', justify='left', wraplength=200)
    link1 = tkinter.Label(win, text = contents[0]['link']['web_url'],  fg = "blue",bg="white", font=("맑은 고딕", 8), cursor="hand2", width=35, height=5, anchor='n', justify='left', wraplength=200)
    
    lb3 = tkinter.Label(win, text = contents[1]['title'], bg = "white", font=("맑은 고딕", 10, 'bold'), width=26, height=2, anchor='n', justify='left', wraplength=200)
    lb4 = tkinter.Label(win, text = contents[1]['snews_body'],bg="white", font=("맑은 고딕", 10), width=30, height=10, anchor='n', justify='left', wraplength=200)
    link2 = tkinter.Label(win, text = contents[1]['link']['web_url'],  fg = "blue",bg="white", font=("맑은 고딕", 8), cursor="hand2", width=35, height=5, anchor='n', justify='left', wraplength=200)
    
    lb5 = tkinter.Label(win, text = contents[2]['title'], bg = "white", font=("맑은 고딕", 10, 'bold'), width=26, height=2, anchor='n', justify='left', wraplength=200)
    lb6 = tkinter.Label(win, text = contents[2]['snews_body'],bg="white", font=("맑은 고딕", 10), width=30, height=10, anchor='n', justify='left', wraplength=200)
    link3 = tkinter.Label(win, text = contents[2]['link']['web_url'], fg = "blue", bg="white", font=("맑은 고딕", 8), cursor="hand2", width=35, height=5, anchor='n', justify='left', wraplength=200)
    
    
    lbl.pack()
    lb2.pack()
    lb3.pack()
    lb4.pack()
    lb5.pack()
    lb6.pack()
    link1.pack()
    link2.pack()
    link3.pack()
    
    link1.bind("<Button>", link1_btn)
    link2.bind("<Button>", link2_btn)
    link3.bind("<Button>", link3_btn)
    print(contents[0]['snews_body'])
    
    lbl.place(x=181, y=175)    
    lb2.place(x=181, y=250)
    lb3.place(x=442, y=175)
    lb4.place(x=442, y=250)
    lb5.place(x=703, y=175)
    lb6.place(x=703, y=250)
    link1.place(x=181, y=390)
    link2.place(x=442, y=390)
    link3.place(x=703, y=390)
    
    win.mainloop()

                    



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



# 마이크 세팅

# 오디오 파일 / 마이크에서 음성을 추출하는 객체
recognizer = sr.Recognizer()

# 마이크를 다루는 객체
microphone = sr.Microphone(sample_rate=16000)

# 마이크 세팅 - 에너지 임계점 설정
with microphone as source:
    recognizer.adjust_for_ambient_noise(source)
    print("=========================")
    print("무엇을 도와드릴까요? :)")
    print("=========================")
    print("소음 수치 반영하여 음성을 청취합니다. {}".format(recognizer.energy_threshold))
    
# 소음 수치 반영하여 음성을 청취합니다. 199.67706126141093
    
    
with microphone as source:
    audio_data = recognizer.listen(source)
    audio = audio_data.get_raw_data()

res = requests.post(kakao_speech_url, headers=headers, data=audio)

#print(res.text)

result_json_string = res.text[res.text.index('{"type":"finalResult"'):res.text.rindex('}')+1]
result = json.loads(result_json_string)

#print(result)
#print(result['value'])



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