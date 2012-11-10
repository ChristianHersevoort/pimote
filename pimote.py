from flask import Flask, jsonify, render_template, abort
from models import db, File

app = Flask(__name__)

@app.route('/')
@app.route('/browse/<hash>')
def browse(hash=None):
    current_file = File.query.filter_by(hash=hash).first()
    files = File.query.filter_by(root=hash).all()

    if len(files) <= 0:
        return abort(404)

    return render_template('browse.html', files=files, current=current_file)


@app.route('/file/<hash>')
def file(hash):
    file = File.query.filter_by(hash=hash).first_or_404()
    return render_template('file.html', file=file)

@app.route('/play_file/<hash>')
def play_file(hash):
    file = File.query.filter_by(hash=hash).first_or_404()

    #TODO: start a subprocess or something ;-)
    return browse()

@app.route('/json/')
@app.route('/json/browse/<hash>/')
def json_browse(hash=None):
    files = File.query.filter_by(root=hash)
    return jsonify(files=[i.serialize for i in files.all()])

if __name__ == '__main__':
    app.run(debug=True)
