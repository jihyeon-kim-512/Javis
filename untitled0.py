from bs4 import BeautifulSoup

import urllib.request
import urllib.parse

with open("example.html") as fp:
    soup = BeautifulSoup(fp, 'html.parser')

web_url = 'https://www.google.com/search?rlz=1C1CAFC_enKR903KR903&ei=ueMzX-a0HdT6-QbLzpOYCA&q=s%2Fs+%ED%8C%A8%EC%85%98+%ED%8A%B8%EB%A0%8C%EB%93%9C&oq=s%2Fs+%ED%8C%A8%EC%85%98+%ED%8A%B8%EB%A0%8C%EB%93%9C&gs_lcp=CgZwc3ktYWIQAzIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeMgYIABAHEB4yBggAEAcQHjIGCAAQBxAeOgIIADoICAAQCBAHEB46BAgAEA1Q-05Y9llgi1xoAHAAeACAAZIBiAG_B5IBAzAuN5gBAKABAaoBB2d3cy13aXrAAQE&sclient=psy-ab&ved=0ahUKEwim9bOs2JXrAhVUfd4KHUvnBIMQ4dUDCAw&uact=5%27'
# web_url에 원하는 웹의 URL을 넣어주시면 됩니다.
with urllib.request.urlopen(web_url) as response:
    html = response.read()
    soup = BeautifulSoup(html, 'html.parser')
    
    first_div = soup.find("div")
    print(first_div)
    