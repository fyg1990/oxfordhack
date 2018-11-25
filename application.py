from flask import Flask,jsonify
import api

app = Flask(__name__)

@app.route("/get-all-records")
def records():
    all_record = api.get_all_record()
    return jsonify(all_record)
