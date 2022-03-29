from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)

client = MongoClient('localhost', 27017)
db = client.dbsparta  

@app.route('/')
def home():
    return render_template('index.html')

# 메모 조회
@app.route('/memo', methods=['GET'])
def read_articles():
    result = list(db.articles.find({}, {'_id': False}))

    return jsonify({'result': 'success', 'articles': result})

# 메모 생성
@app.route('/memo', methods=['POST'])
def create_article():
    title_receive = request.form['title_give'] 
    content_receive = request.form['content_give'] 

    article = {'title': title_receive, 'content': content_receive}

    db.articles.insert_one(article)

    return jsonify({'result': 'success'})

# 메모 수정
@app.route('/update', methods=['POST'])
def update_article():
    card_title = request.form['card_title']  
    card_text = request.form['card_text']  

    new_title = request.form['new_title']
    new_text = request.form['new_text']

    db.articles.update_one({'title':card_title, 'content':card_text}, {'$set':{'title':new_title, 'content':new_text}})

    return jsonify({'result': 'success'})

# 메모 삭제
@app.route('/delete', methods=['POST'])
def delete_article():
    card_title = request.form['card_title'] 
    card_text = request.form['card_text']  

    db.articles.delete_one({'title':card_title, 'content':card_text})

    return jsonify({'result': 'success'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)