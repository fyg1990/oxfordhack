from flask import Flask,jsonify, send_from_directory
import api

app = Flask(__name__,static_url_path='')

@app.route('/')
def root():
    return send_from_directory("",'index.html')

@app.route("/get-all-records")
def records():
    all_record = api.get_all_record()
    return jsonify(all_record)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('js', path)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('css', path)


