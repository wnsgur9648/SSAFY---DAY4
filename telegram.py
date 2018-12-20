import requests
import json
#환경변수에서 토큰 뽑아오기
import os
token=os.getenv("TELEGRAM_TOKEN")
#다른 사람이 나의 토큰을 보는 것을 방지하기 위해 토큰 값을 os 환경변수에 넣은 다음 불러서 사용


url = "https://api.hphk.io/telegram/bot{}/getUpdates".format(token)
response = json.loads(requests.get(url).text)
# 문자열로 날라온 response를 json 형식으로 만듬
print(response)

url = "https://api.hphk.io/telegram/bot{}/sendMessage".format(token)

chat_id = response["result"][-1]["message"]["from"]["id"]
msg = response["result"][-1]["message"]["text"]

requests.get(url, params = {"chat_id":chat_id, "text":msg})