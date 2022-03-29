from flask import Flask, render_template
app = Flask(__name__)

## HTML pages

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/welcome')
def welcome():
   return render_template('welcome.html')

@app.route('/login')
def login():
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

@app.route('/signIn')
def signIn():
   return render_template('signIn.html')



if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)