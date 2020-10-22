import requests
import json


url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type" : "refresh_token",
    "client_id"  : "",
    "refresh_token" : ""
}
response = requests.post(url, data=data)

print(response.json())
