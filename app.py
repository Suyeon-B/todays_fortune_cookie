import os
from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import *
# from flask_wtf.csrf import CSRFProtect
from pymongo import MongoClient
import datetime
# from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('localhost', 27017)
# client = MongoClient('mongodb://suyeon:tndus7988@3.36.39.129',27017)
db = client.dbFortune

## HTML pages
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/welcome')
def welcome():
   return render_template('welcome.html')

@app.route('/login_btn')
def login_btn():
   return render_template('login.html')

@app.route('/logined')
def logined():
   return render_template('logined.html')

@app.route('/main')
def main():
   return render_template('main.html')

@app.route('/myPage')
def myPage():
   return render_template('myPage.html')

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
            userinfo = {'user_id': userid, 'user_name': username, 'user_pwd': password }
            db.users.insert_one(userinfo)
            return jsonify({'result' : "success"})


# 로그인
@app.route('/login', methods=['POST'])
def login():

   userid = request.form['userid']
   password = request.form['password']

   user = db.users.find_one({'user_id': userid}, {'user_pwd': password})
   if user is None:
      return jsonify({'result' : 'fail'})
   else:
      return jsonify({'result' : "success", 'user_id': userid})


# 로그아웃
@app.route('/logout', methods=['POST'])
def logout():
    return render_template('home.html')

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)