#coding:utf-8
from flask import Flask,request,send_from_directory,flash,redirect,url_for,abort,jsonify,render_template
import os
from werkzeug.utils import secure_filename

from src.reinhard.main import work as reinhard
import time

app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
UPLOAD_FILE_PATH = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/file/<path:filename>',methods=['DELETE'])
def delete(filename):
    filename = secure_filename(filename)
    filepath = os.path.join(UPLOAD_FILE_PATH,filename)
    if os.path.isfile(filepath):
        os.remove(filepath)
        return jsonify({'msg':'删除成功','code':0})
    else:
        return jsonify({'msg':'删除失败','code':1})

@app.route('/file',methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        abort(400)
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FILE_PATH, filename))
        return redirect('/')
    else:
        abort(400)

@app.route('/file',methods=['GET'])
def get_list():
    return jsonify(list(i[2] for i in os.walk(UPLOAD_FILE_PATH)))

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FILE_PATH,filename, as_attachment=True)

@app.route('/work')
def work():
    ref_img_filename = os.path.join(UPLOAD_FILE_PATH,secure_filename(request.args.get('ref_img')))
    src_img_filename = os.path.join(UPLOAD_FILE_PATH,secure_filename(request.args.get('src_img')))
    if not os.path.isfile(ref_img_filename) or not os.path.isfile(src_img_filename):
        return jsonify({'msg':'file not exists','code':1})
    out_img = str(round(time.time() * 1000))+'.jpg'
    out_img_file = os.path.join(UPLOAD_FILE_PATH,out_img)
    reinhard(src_img_filename,ref_img_filename,out_img_file)
    return jsonify({'msg':'done','code':0,'url':url_for('download',filename=out_img)})

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0',debug=True)
