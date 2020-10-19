import requests
import json

#url = "https://kauth.kakao.com/oauth/token"
#
#data = {
#        "grant_type" : "authorization_code",
#        "client_id" : "dbbadbe804f295f7da88212ccff2f83f",
#        "redirect_uri" : "https://localhost.com",
#        "code" : "qTG-tufJi8CA6hgRqwhQkNGDYihLNy4Wzd2OjXz-KoTCC8i1sHS0rglzifdpkqeYbyytAAopdSkAAAFzjhYhFg"
#        }
#
#response = requests.post(url, data = data)
#
#tokens = response.json()
#
#with open("kakao_token.json", "w") as fp :
#    json.dump(tokens,fp)
#    
#print(response.json())
#

url = "https://kauth.kakao.com/oauth/token"
data = {
    "grant_type" : "refresh_token",
    "client_id"  : "dbbadbe804f295f7da88212ccff2f83f",
    "refresh_token" : "dhdwVQt-aI0Dv4ZYXRIrwyrDG2XKegXa0OwyKwo9dJkAAAFzjheEmw"
}
response = requests.post(url, data=data)

print(response.json())