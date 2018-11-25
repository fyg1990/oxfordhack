from flask import Flask
import api

app = Flask(__name__)

@app.route("/get-all-records")
def records():
    all_record = api.get_all_record()
    return all_record
