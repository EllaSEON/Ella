import datetime
from flask_pymongo import PyMongo
# request: 사용자로부터 요청을 받을때 요청에 대한 정보를 갖고있는 변수
from flask import Flask, render_template, request, redirect
# redirect 이동시킨다. 페이지를 보여주는게 아니라 글을 쓰고나면 페이지를 다시보여줘야해.

app = Flask(__name__)
app.config['MONGO_URI'] = "mongodb://localhost:27017/local"  # 데이터베이스 연결
mongo = PyMongo(app)  # 데이터베이스에 저장하기 위한 조치


@app.route('/write', methods=["POST"])  # POST를 추가하면 요청한다는 뜻
def write():
    name = request.form.get('name')  # 이름이랑 내용을 받아서 몽고DB에 저장해야해
    content = request.form.get('content')

    mongo.db['wedding'].insert_one({
        "name": name,
        "content": content
    })
    return redirect('/')


@app.route('/')
def index():
    now = datetime.datetime.now()
    wedding = datetime.datetime(2022, 8, 13, 0, 0, 0)
    diff = (wedding-now).days
    guestbooks = mongo.db['wedding'].find()
    # = 을 사용하는 이유 : diff의 변수는 파이썬에서 사용되는건데
    return render_template('index.html', day=diff, guestbooks=guestbooks)
    # diff 변수가 html 에서 사용되려면 주머니=값 문법을 써야함


if __name__ == '__main__':
    app.run(port=5001, debug=True)
