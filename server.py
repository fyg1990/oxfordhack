from bottle import route, run
import api


@route('/get-all-records')
def hello():
    all_record = api.get_all_record()
    return all_record


run(host='localhost', port=8080, debug=True)