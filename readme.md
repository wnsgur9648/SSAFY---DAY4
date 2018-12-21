# 181220 - Day3 (Parameter란?, 아파트 매매 내역 시스템 크롤링, Telegram 사용)



# 1. parameter란?

- Parameter를 전달하는 방식은 GET, POST 방식이 있다.
  - GET방식은 URL 뒤에 ?parameter명=~~~로 사용 가능
  - POST방식은 비밀스러운 데이터(비밀번호,ID...)를 보낼 때 사용



- GET 방식으로 Parameter 전달

*index.html*

```html
...
        <a href="/toon?type=naver"><button>네이버웹툰</button></a> 
        <!--?parameter=~~~ get방식으로 parameter를 넘겨준다.-->
        <a href="/toon?type=daum"><button>다음웹툰</button></a>
...
```



*app.py*

```python
from flask import Flask,render_template, request
#url에서 원하는 parameter 얻기위해 request를 import 해야함
import requests
import time
from bs4 import BeautifulSoup as bs

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/toon")
def toon():
    cat = request.args.get("type") #URL에서 Parameter값을 뽑아냄
    if(cat == "naver"):
        today = time.strftime("%a").lower()
        url = "https://comic.naver.com/webtoon/weekdayList.nhn?week={}".format(today)
        response = requests.get(url).text
        soup = bs(response, 'html.parser')

        toons = []
        li = soup.select('.img_list li')
    	
        for item in li:
    	    toon = { 
    	        "title" : item.select('dt a')[0].text, #==item.select_one('dt a').text
    	        "url" : "https://comic.naver.com/"+item.select('dt a')[0]["href"], 
    	        "img_url" : item.select('.thumb img')[0]["src"]
    	    }
    	    toons.append(toon)
    	    
    elif(cat == "daum"):
        today=time.strftime("%a").lower()
        url = "http://webtoon.daum.net/data/pc/webtoon/list_serialized/{}?timeStamp=1545116996132".format(today)

        data = requests.get(url).json()
        toons = []
        for i in range(len(data["data"])):
            toon = { 
                "title" : data["data"][i]["title"], 
                "url" : "http://webtoon.daum.net/webtoon/view/"+data["data"][i]["nickname"], 
                "img_url" : data["data"][i]["pcThumbnailImage"]["url"]          
            }
            toons.append(toon)
            
    return render_template("toon.html", cat = cat, t = toons)
    
@app.route("/lotto")
def lotto():
    return render_template("lotto.html")
```



*toon.html*

```html
<!DOCTYPE html>
<html>
    <head>
        <title>Webtoon 모아보기</title>
    </head>
    <body>
        <h2>너님 지금 {{cat}} 웹툰을 찾은거 맞음?</h2>
        <table>
            <thead>
                <tr>
                    <th>썸네일</th>
                    <th>웹툰 제목</th>
                    <th>웹툰 링크</th>
                </tr>
            </thead>
            {%for i in t:%}
            <tbody>
                <tr>
                    <td><img src="{{i["img_url"]}}"></img></td>
                    <td>{{i["title"]}}</td>
                    <td><a href="{{i["url"]}}">클릭</a></td>
                </tr>
            </tbody>
            {% endfor %}        
        </table>
    </body>
</html>
```





# 2. 아파트 매매 내역 시스템 크롤링

-> URL로만은 자신이 원하는 데이터를 받을 수가 없다. 그래서 request header에서 host와 referer를 수정해주어야 아파트 매매 내역 시스템에서 정보를 요청한 것처럼 만들어 줘야한다.



*index.html*

```html
...
	<a href="/apart"><button>아파트 실거래가</button></a>
...
```



*app.py*

```python
from flask import Flask,render_template, request #url에서 원하는 parameter 얻기위해 request를 import 해야함
import requests
import time
from bs4 import BeautifulSoup as bs
import json

...
    
@app.route("/apart")
def apart():
    # 1. 내가 원하는 정보를 얻을 수 있는 url을 url 변수에 저장한다.
    url = "http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=20333305&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode="
    # 1-1. request header에 추가할 정보를 dictionary 형태로 저장한다.
    headers = {
        "Host": "rt.molit.go.kr",
        "Referer": "http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND"
    }
    # 2. requests의 get 기능을 이용하여 해당 url에 header와 함께 요청을 보낸다.
    response = requests.get(url, headers = headers).text
    # 3. 응답으로 온 코드의 형태를 살펴본다. (json/xml/html)
    document = json.loads(response)
    
    for d in document["result"]:
        print(d["BLDG_NM"])
    
    return render_template("apart.html")
```





# 3. Telegram 사용



1. 스마트폰에서 Telegram App을 받고 자신의 번호로 로그인
2. 컴퓨터에서 Telegram Web을 검색해서 자신의 번호로 로그인 -> 스마트폰으로 인증번호를 받고 인증
3. @botfather 검색 들어가서 start
4. /newbot -> 새로운 봇만들기
5. Apartment Price Bot(봇 이름)
6. twice_dec_bot(봇 유저 이름) -> token이 나온다.
7. Cloud9 배쉬에서 `$ vi  ~/.bashrc` -> export TELEGRAM_TOKEN = token값 추가
8. `$ source ~/.bashrc` -> 설정한 환경변수가 적용된다.
9. `$ echo $TELEGRAM_TOKEN `
10. workspace에서 telegram.py를 만든다.
11. telegram에서 twice_dec_bot 을 검색해서 채팅을 쓰고 telegram.py를 실행



*telegram.py*

```python
#telegram.py
import requests
import json
#환경변수에서 토큰 뽑아오기
import os
token=os.getenv("TELEGRAM_TOKEN")
#다른 사람이 나의 토큰을 보는 것을 방지하기 위해 토큰 값을 os 환경변수에 넣은 다음 불러서 사용


url = "https://api.hphk.io/telegram/bot{}/getUpdates".format(token)
#원래는 Cloud9에서 바로  Telegram으로 request를 보낼 수 있었지만 지금은 안되므로 우회를 해서 보내도록 한다.
response = requests.get(url).text
print(response)
```



*Cloud9 Bash*

```
wnsgur9648:~/workspace/day4 $ python telegram.py 
{"ok":true,"result":[{"update_id":884401307,
"message":{"message_id":1,"from":{"id":772997280,"is_bot":false,"first_name":"\uc900\ud601","last_name":"\uc7a5"},"chat":{"id":772997280,"first_name":"\uc900\ud601","last_name":"\uc7a5","type":"private"},"date":1545281664,"text":"/start","entities":[{"offset":0,"length":6,"type":"bot_command"}]}},{"update_id":884401308,
"message":{"message_id":2,"from":{"id":772997280,"is_bot":false,"first_name":"\uc900\ud601","last_name":"\uc7a5","language_code":"ko"},"chat":{"id":772997280,"first_name":"\uc900\ud601","last_name":"\uc7a5","type":"private"},"date":1545281668,"text":"\u314e\u3147\u314e\u3147"}},{"update_id":884401309,
"message":{"message_id":3,"from":{"id":772997280,"is_bot":false,"first_name":"\uc900\ud601","last_name":"\uc7a5","language_code":"ko"},"chat":{"id":772997280,"first_name":"\uc900\ud601","last_name":"\uc7a5","type":"private"},"date":1545281969,"text":"hello"}}]}
```



- telegram에서 보낸 메세지 echo 하기

  -> telegram에서 메세지를 하나 적고 telegram.py 실행 -> telegram 채팅창에 똑같은 메세지가 날라옴


*telegram.py*

```python
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
```



*app.py* -> 지정된 메세지에 대한 응답

```python
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
    #telegram으로 응답보내기
    requests.get(url, params = {"chat_id":chat_id, "text":msg})
    print(request.get_json())
    return '', 200
    
@app.route('/set_webhook')
# webhook이 한번 걸리면 telegram 서버에 봇으로 오는 메세지가 가는 장소가 지정이 되고 이 webhook을 삭제하려면 del_webhook을 이용하여 없애야한다.
def set_webhook():
    url = TELEGRAM_URL + '/bot' + TELEGRAM_TOKEN + '/setWebhook'
    params = {
        'url' : 'https://ssafy-week2-wnsgur9648.c9users.io/{}'.format(TELEGRAM_TOKEN)
        #이 url과 위에 있는 @app.route('/{}'.format(TELEGRAM_TOKEN), methods=['POST'])가 같다
    }
    response = requests.get(url, params = params).text
    return response

```



- Webhook  (요청이 왔는지 확인하는 것)

**App**  ---- 메세지 전송 ----> **Telegram Server** ---- 메세지 왔다! ----> **자신의 컴퓨터** ---- 원하는 응답 ----> **Telegram Server bot**



# 4. 환율 크롤링

*app.py*

```python
def exchange():
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
            cnt+=1
    
    print("총 개수 : {}개".format(cnt))
    
    return render_template("exchange.html",ex=ex)
```



*exchange.html*

```html
<!DOCTYPE html>
<html>
    <head>
        <title>환율</title>
    </head>
    <body>
        <h2>환율</h2>
        <table>
            <thead>
                <tr>
                    <th>국가</th>
                    <th>환율</th>
                </tr>
            </thead>
            {%for i in ex.keys():%}
            <tbody>
                <tr>
                    <td>{{i}}</td>
                    <td>{{ex[i]}}</td>
                </tr>
            </tbody>
            {% endfor %}
            
        </table>
    </body>
</html>
```

