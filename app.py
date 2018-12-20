from flask import Flask,render_template, request #url에서 원하는 parameter 얻기위해 request를 import 해야함
import requests
import time
from bs4 import BeautifulSoup as bs
import json

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")
    
@app.route("/toon")
def toon():
    cat = request.args.get("type")
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
    
@app.route("/apart")
def apart():
    # 1. 내가 원하는 정보를 얻을 수 있는 url을 url 변수에 저장한다.
    url = "http://rt.molit.go.kr/new/gis/getDanjiInfoDetail.do?menuGubun=A&p_apt_code=1304&p_house_cd=1&p_acc_year=2018&areaCode=&priceCode="
    # 1-1. request header에 추가할 정보를 dictionary 형태로 저장한다.
    headers = {
        "Host": "rt.molit.go.kr",
        "Referer": "http://rt.molit.go.kr/new/gis/srh.do?menuGubun=A&gubunCode=LAND"
    }
    # 2. requests의 get 기능을 이용하여 해당 url에 header와 함께 요청을 보낸다.
    response = requests.get(url, headers = headers).text
    # 3. 응답으로 온 코드의 형태를 살펴본다. (json/xml/html)
    document = json.loads(response)
    
    print(document)
    
    #for d in document["result"]:
     #   print(d["BLDG_NM"])
    
    return render_template("apart.html")
    
@app.route("/exchange")
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