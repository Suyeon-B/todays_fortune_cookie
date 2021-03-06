from flask import Flask, render_template, request, session, jsonify, redirect, url_for
from bson.objectid import ObjectId
import hashlib
import jwt
from pymongo import MongoClient
import datetime
# import urllib.request
# import json

app = Flask(__name__)
# client = MongoClient('localhost', 27017)
client = MongoClient('mongodb://suyeon:tndus7988@3.36.39.129',27017)
db = client.dbFortune

## HTML pages
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/welcome')
def welcome():
   # 상호쓰 갖다 붙임
   token_receive = request.cookies.get('myToken')
   if token_receive is not None:
      return redirect(url_for('logined'))

   return render_template('welcome.html')

SECRET_KEY = 'apple'
app.config['SECRET_KEY'] = 'galhg2ilh6safbkj'

@app.route('/login_btn')
def login_btn():
   return render_template('login.html')

# by 상호
@app.route('/login', methods = ['POST', 'GET'])
def login():
   if request.method == 'POST':
      user_id = request.form['id_input']
      user_pw = request.form['pw_input']

      session['userid'] = user_id

      user_pw_hash = hashlib.sha256(user_pw.encode("utf-8")).hexdigest()
      result = db.users.find_one({'user_id' : user_id, 'user_pwd' : user_pw_hash})

      if result is not None:
         payload = {
            'id': user_id,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes = 60 * 60 * 24)
         }
         token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
         return jsonify({'success': True, 'token': token})
      else:
         return jsonify({'success': False, 'msg': '아이디,비밀번호가 일치하지 않습니다'})
   else:
      return render_template('login.html')


@app.route('/logined')
def logined():
   token_receive = request.cookies.get('myToken')
   payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
   user_id = payload['id']

   name = db.users.find_one({'user_id': user_id})
   userName = name['user_name']
   return render_template('logined.html', userName = userName)
   # return render_template('logined.html')

@app.route('/main')
def main():
   return render_template('main.html')

@app.route('/myPage')
def myPage():
   token_receive = request.cookies.get('myToken')
   payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
   user_id = payload['id']
   fortuneList = list(db.saveFortune.find({'user_id' : user_id}))
   
   my_fortune = []

   for fortuneLists in fortuneList:
      my_fortune.append(fortuneLists)
      
   print(my_fortune)

   return render_template('myPage.html', my_fortune = my_fortune)

@app.route('/signIn_btn')
def signIn_btn():
   return render_template('signIn.html')


# 회원가입
@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
   # 회원가입 버튼을 누르면
   if request.method == 'GET':
      return render_template("signIn.html")

   # 회원가입완료 버튼을 누르면
   else:
      # 회원정보 생성
      username = request.form['username']
      userid = request.form['userid']
      password = request.form['password']
      re_password = request.form['re_password']

      is_already_exist = db.users.find_one({'user_id' : userid})

      if is_already_exist is not None:
         return jsonify({'result' : 'fail' , 'msg' : 'alreay exist'})
      elif not (userid and username and password and re_password):
         print(userid, username, password, re_password)
         return jsonify({'result' : 'fail' , 'msg' : 'fill error'})
      elif password != re_password:
         return jsonify({'result' : 'fail', 'msg' : "pw error"})
      else:  # 모두 입력이 정상적으로 되었다면 밑에명령실행(DB에 입력됨)
         # pw_hash = bcrypt.generate_password_hash('password')
         pw_hash = hashlib.sha256(password.encode("utf-8")).hexdigest()
         userinfo = {'user_id': userid, 'user_name': username, 'user_pwd': pw_hash }
         db.users.insert_one(userinfo)
         return jsonify({'result' : "success"})

# 메인페이지에서 포춘쿠키 저장하기
@app.route('/save', methods=['POST'])
def save():
   fortune = request.form['fortune']
   myToken = request.form['myToken']
   payload = jwt.decode(myToken, SECRET_KEY, algorithms=['HS256'])['id']
   
   today = datetime.datetime.now()
   print(today)
   end_date = datetime.datetime(2022, 8, 11)
   print(end_date)
   d_day = end_date - today
  
   fortuneInfo = {'user_id' : payload, 'fortune' : fortune, 'd_day' : d_day.days}
   db.saveFortune.insert_one(fortuneInfo)
   return jsonify({'result' : "success"})


# @app.route('/translate', methods=['POST'])
# def translate():
#    fortune_eng = request.form["fortune_eng"]
#    fortune_eng = "hi nice to meet you"
#    client_id = "dbXYNxcslKrY4UlMw7h8"    # ■■ ID 설정 ■■
#    client_secret = "WjxS3mgM8h"   # ■■ PW 설정 ■■
#    encText = urllib.parse.quote(fortune_eng)
#    data = "source=en&target=ko&text=" + encText
#    url = "https://openapi.naver.com/v1/papago/n2mt"
#    request = urllib.request.Request(url)
#    request.add_header("X-Naver-Client-Id",client_id)
#    request.add_header("X-Naver-Client-Secret",client_secret)
#    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
#    rescode = response.getcode()
#    if(rescode==200):
#       response_body = response.read()
#       translated_result = response_body.decode("utf-8")
#       temp = json.loads(translated_result)
#       translated_text = temp['message']['result']['translatedText']
#       return jsonify({"result" : "success", "translated_text" :translated_text})
#    else:
#       Error_Code = rescode
#       # print(“Error Code:” + rescode)
#       # fortuneInfo = {‘fortune’ : fortune}
#       # db.saveFortune.insert_one(fortuneInfo)
#       return jsonify({"result" : "fail", "Error_Code": Error_Code})


#디데이 계산
@app.route('/d_day')
def d_day():
   # today = datetime.date(2022, 6, 2)
   #오늘
   today = datetime.date.today()
   #시작일
   start_date = datetime.date(2022, 3, 28)
   #종료일
   end_date = datetime.date(2022, 8, 11)
   #디데이
   d_day = end_date - today
   #총 일수
   all_day = end_date - start_date
   return jsonify({'d_day' : d_day.days, 'all_day' : all_day.days})

@app.route('/detail')
def detail():
   postid_receive = request.args.get('postId_give')
   fortune = db.saveFortune.find_one({'_id': ObjectId(postid_receive)})
   print(fortune)
   return render_template('detail.html', fortune = fortune)

@app.route('/fortune_check', methods=['GET'])
def fortune_check():
   #로그인 아이디
   token_receive = request.cookies.get('myToken')
   payload = jwt.decode(token_receive, SECRET_KEY, algorithms=['HS256'])
   userid = payload['id']
   #오늘 날짜 YYYY-MM-DD 형식
   today = datetime.date.today().isoformat()
   openinfo = {'user_id' : userid, 'open_date' : today}
   #오늘 오픈했는지 체크
   result = db.openinfo.find_one(openinfo)
   
   if result is not None:
      #오늘 오픈 했으면
      return jsonify({'result' : 'fail', 'msg' : '너는 오늘 이미 포춘쿠키를 열었따'})
   
   else:
      #오늘 오픈 안했으면
      #오픈 날짜 저장
      db.openinfo.insert_one(openinfo)
      return jsonify({'result' : 'success'})

      

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)