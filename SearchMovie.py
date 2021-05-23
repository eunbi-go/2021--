import os
import sys
import urllib.request
client_id = "tvo5aUWG9rwBq1YRMqyJ"
client_secret = "40VkT1fuAS"
encText = urllib.parse.quote("어벤져스")
url = "https://openapi.naver.com/v1/search/movie?query=" + encText # json 결과
# url = "https://openapi.naver.com/v1/search/blog.xml?query=" + encText # xml 결과
request = urllib.request.Request(url)
request.add_header("X-Naver-Client-Id",client_id)
request.add_header("X-Naver-Client-Secret",client_secret)
response = urllib.request.urlopen(request)
rescode = response.getcode()
if(rescode==200):
    response_body = response.read()
    print(response_body.decode('utf-8'))
else:
    print("Error Code:" + rescode)