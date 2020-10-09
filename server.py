# coding:utf-8
from flask import Flask, request, send_from_directory, flash, redirect, url_for, abort, jsonify, render_template, g
import os
from werkzeug.utils import secure_filename
from flask import helpers

import color_transfer
import db
from logger import get_log

os.environ['LD_LIBRARY_PATH'] = '/'.join(__file__.split('/')[:-1]) + '/lib'

app = Flask(__name__, static_url_path='')
app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

executor = color_transfer.Executor()
fs = color_transfer.FileStore()


@app.before_request
def before_request():
    g.db = db.SqliteDB()


@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()


@app.route('/')
def index():
    return send_from_directory('static', 'index.htm')


@app.route('/file/<path:filename>', methods=['DELETE'])
def delete(filename):
    # TODO
    # filename = secure_filename(filename)
    # filepath = os.path.join(UPLOAD_FILE_PATH, filename)
    # if os.path.isfile(filepath):
    #     os.remove(filepath)
    #     return jsonify({'msg': '删除成功', 'code': 0})
    # else:
    return jsonify({'msg': '删除失败', 'code': 1})


@app.route('/file/<types>', methods=['POST'])
def upload(types):
    if 'file' not in request.files:
        abort(400)
    file = request.files['file']
    if not file:
        abort(400)
    filename = secure_filename(file.filename)
    if types == 'src':
        filename = 'src_' + filename
    elif types == 'ref':
        filename = 'ref_' + filename
    else:
        abort(400)
    return jsonify({'hash': fs.upload(file, filename)})


@app.route('/file/<types>', methods=['GET'])
def get_list(types):
    # files = next(os.walk(UPLOAD_FILE_PATH))[2]
    # files = list(filter(lambda x: x.startswith(types), files))
    # files.sort(key=lambda f: os.stat(os.path.join(UPLOAD_FILE_PATH, f)).st_mtime, reverse=True)
    return jsonify(fs.list(types))


@app.route('/download/<path:filename>')
def download(filename):
    file_path = fs.download(filename)
    if not file_path:
        abort(404)
    if not os.path.exists(file_path):
        abort(404)
    return helpers.send_file(file_path, cache_timeout=24 * 3600)


@app.route('/work')
def work():
    ref_img = request.args.get('ref_img')
    src_img = request.args.get('src_img')
    al = request.args.get('alg', 'reinhard')
    if al not in ['reinhard', 'welsh']:
        abort(400)
    r_id = g.db.insert_file(src_img, ref_img, al)
    executor.add_task(r_id, src_img, ref_img, al)
    return jsonify({'redirect': 'show'})


@app.route('/show')
def show():
    return send_from_directory('static', 'submission.html')


@app.route('/submission')
def submission():
    return jsonify(g.db.query_db('select * from result order by id desc'))


@app.route('/submission/del/<int:id>')
def submission_del(id):
    # TODO
    # row = g.db.query_db('select * from result where id = ?', (id,), one=True)
    # filenames = [row['src_img'], row['res_img'], row['ref_img']]
    # for row_name in row:
    #     if row[row_name] not in filenames:
    #         continue
    #     size = g.db.query_db('select count(1) from result where {} = ?1'.format(row_name), (row[row_name],), one=True)
    #     if 1 < int(size['count(1)']):
    #         filenames.remove(row[row_name])
    #
    # for i in filenames:
    #     try:
    #         os.remove(os.path.join(UPLOAD_FILE_PATH, i))
    #     except IOError:
    #         pass
    # g.db.del_file(id)
    return redirect(url_for('show', _external=True))


if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=8080)
