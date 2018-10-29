#coding:utf-8
from flask import Flask,request,send_from_directory,flash,redirect,url_for,abort,jsonify,render_template
import os
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
UPLOAD_FILE_PATH = 'uploads/'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload',methods=['POST'])
def upload():
    if 'file' not in request.files:
        flash('No file part')
        abort(400)
        return redirect('/')
    file = request.files['file']
    if file:
        filename = secure_filename(file.filename)
        file.save(os.path.join(UPLOAD_FILE_PATH, filename))
        return redirect('/')
    else:
        abort(400)

@app.route('/list')
def get_list():
    return jsonify(list(i[2] for i in os.walk(UPLOAD_FILE_PATH)))

@app.route('/download/<path:filename>')
def download(filename):
    return send_from_directory(UPLOAD_FILE_PATH,filename, as_attachment=True)

if __name__ == '__main__':
    app.run(port=8080,host='0.0.0.0')
