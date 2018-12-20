from flask import Flask, request
import requests
import json
import time
import os
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
TELEGRAM_URL = 'https://api.hphk.io/telegram'

@app.route('/{}'.format(TELEGRAM_TOKEN), methods=['POST']) 
# 주소를 복잡하는 이유 -> 다른 사람이 접근할 수 있기 때문에
# methods=['POST'] -> post 방식 사용
def telegram():
    #telegram으로부터 요청이 들어올 경우, 해당 요청을 처리하는 코드
    chat_id = request.get_json()["message"]["from"]["id"]
    msg = request.get_json()["message"]["text"]
    
    if(msg=="안녕"):
        msg="첫만남에는 존댓말을 써야죠!"
    elif(msg=="안녕하세요"):
        msg="인사 잘한다~~~~!"
    elif(msg=="환율"):
        conti=["#asiaBody", "#europeBody", "#mideastBody", "#africaBody"]
        ex={}
        cnt=0
    
        url = "http://m.exchange.daum.net/mobile/exchange/exchangeMain.daum"
        response = requests.get(url).text
        soup = bs(response, "html.parser")
        
        for i in range(len(conti)):
            document = soup.select(conti[i])[0]
            tbody = document.select("tbody")[0]
            name = tbody.select("td.name")
            idx = tbody.select("td.idx")
                
            for j in range(len(name)):
                ex[name[j].text]=idx[j].text
        
        msg="";
        for i in ex.keys():
            msg+="{} {}\n".format(i,ex[i])
        
    url = "https://api.hphk.io/telegram/bot{}/sendMessage".format(TELEGRAM_TOKEN)
    requests.get(url, params = {"chat_id":chat_id, "text":msg})
    print(request.get_json())
    return '', 200
    
@app.route('/set_webhook')
def set_webhook():
    url = TELEGRAM_URL + '/bot' + TELEGRAM_TOKEN + '/setWebhook'
    params = {
        'url' : 'https://ssafy-week2-wnsgur9648.c9users.io/{}'.format(TELEGRAM_TOKEN)
    }
    response = requests.get(url, params = params).text
    return response
