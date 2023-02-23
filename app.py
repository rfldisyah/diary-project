import os
from os.path import join, dirname
from dotenv import load_dotenv
from datetime import datetime
from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME = os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)

db = client[DB_NAME]

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    today = datetime.now()
    mytime = today.strftime('%Y-%m-%d-%H-%M-%S')

    today = today.strftime('%Y.%m.%d')

    
    # gambar 1
    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{mytime}.{extension}'
    file.save(filename)


    # profile
    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{mytime}.{extension}'
    profile.save(profilename)

    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    doc = {
        'file': filename,
        'profile': profilename,
        'title':title_receive,
        'content':content_receive,
        'today':today,
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Data berhasil ditambahkan'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)