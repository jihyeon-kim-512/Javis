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
access_token = "zciXxo9pgWpjvtY4ZfJS6RGTeLntRdnesJK5HgopyWAAAAFzjpAfkA"
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