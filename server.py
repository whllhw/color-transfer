#coding:utf-8
from flask import Flask,request,send_from_directory,flash,redirect,url_for,abort,jsonify,render_template,g
import os
from werkzeug.utils import secure_filename

from src.reinhard.main import work as reinhard
from src.welsh.main import work as welsh
import time
import sqlite3
from db import *

app = Flask(__name__,static_url_path='')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
UPLOAD_FILE_PATH = 'uploads/'

@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()
        
@app.route('/')
def index():
    return redirect('index.htm')

@app.route('/file/<path:filename>',methods=['DELETE'])
def delete(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FILE_PATH,filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
        return jsonify({'msg':'删除成功','code':0})
    else:
        return jsonify({'msg':'删除失败','code':1})

@app.route('/file/<types>',methods=['POST'])
def upload(types):
    if 'file' not in request.files:
        # flash('No file part')
        abort(400)
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        if types == 'src':
            filename = 'src_' + filename
        else:
            filename = 'ref_' + filename
        file.save(os.path.join(UPLOAD_FILE_PATH, filename))
        return jsonify({'hash':filename})
        # return redirect('/')
    else:
        abort(400)

@app.route('/file/<types>',methods=['GET'])
def get_list(types):
    files = next(os.walk(UPLOAD_FILE_PATH))[2]
    files = list(filter(lambda x:x.startswith(types),files))
    files.sort(key=lambda f:os.stat(os.path.join(UPLOAD_FILE_PATH,f)).st_mtime)
    return jsonify(files)

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FILE_PATH,filename, as_attachment=True)

@app.route('/work')
def work():
    ref_img_filename = os.path.join(UPLOAD_FILE_PATH,secure_filename(request.args.get('ref_img')))
    src_img_filename = os.path.join(UPLOAD_FILE_PATH,secure_filename(request.args.get('src_img')))
    al = request.args.get('alg','reinhard')
    if not os.path.isfile(ref_img_filename) or not os.path.isfile(src_img_filename):
        return jsonify({'msg':'file not exists','code':1}),400
    out_img = str(round(time.time() * 1000))+'.jpg'
    out_img_file = os.path.join(UPLOAD_FILE_PATH,out_img)
    if al == 'reinhard':
        reinhard(src_img_filename,ref_img_filename,out_img_file)
    elif al == 'welsh':
        welsh(src_img_filename,ref_img_filename,out_img_file)
    else:
        abort(400)
    insert_file(out_img.split('.')[0],src_img,ref_img,al)
    return jsonify({'msg':'done','code':0,'url':url_for('download',filename=out_img)})

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0',debug=True)
