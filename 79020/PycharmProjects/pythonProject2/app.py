from flask import Flask,jsonify,request,session
from mysql.connector import connect
from util import *
from database import *
import json
app = Flask(__name__)
app.config['SECRET_KEY'] = '123456'

@app.route('/')
def hello_world():
    return 'Hello,World!!'

@app.route('/add',methods=['POST'])
def add_users():
    data = request.get_json(force=True)
    name = data.get('name')
    number = data.get('num')
    if check_info_complete():
        return check_and_save(name,number)

@app.route('/users',methods=['GET'])
def get_info():
    conn, cursor = get_connection()
    cursor.execute('select `name` from `students`')
    content = cursor.fetchall()
    cursor.close()
    conn.close()
    list = []
    users={}
    for i in content:
        list.insert(2,i)
    users['users']=list
    return json.dumps(users,ensure_ascii=False)


@app.errorhandler(HttpError)
def handle_http_error(error):
    response=jsonify(error.to_dict())
    response.status_code=error.status_code
    return response


if __name__ =='__main__':
    app.run()