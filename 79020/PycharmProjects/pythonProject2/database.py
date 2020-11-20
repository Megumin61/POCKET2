#database.py
from flask import Flask,jsonify,request,session
from mysql.connector import connect
from werkzeug.security import generate_password_hash,check_password_hash
from util import *

def get_connection():
    conn=connect(user='root',password='',database='bbt2')
    cursor=conn.cursor()
    return conn,cursor

def check_number(number):
    conn, cursor = get_connection()
    cursor.execute('select count(*) from `students` where `number`=%s', (number,))
    count1 = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    return count1
def check_name(number,name):
    conn, cursor = get_connection()
    cursor.execute('select name from `students` where `number`=%s', (number,))
    test_name = cursor.fetchone()[0]
    cursor.close()
    conn.close()
    if name == test_name:
        count2 = 0
    elif name != test_name:
        count2 = 1
    return count2
def check_info_complete():
    data = request.get_json(force=True)
    if data.get('name') is None and data.get('num') is not None:
        raise HttpError(409,'缺少参数name')
    elif data.get('num') is None and data.get('name') is not None:
        raise HttpError(409,'缺少参数num')
    elif data.get('num') is None and data.get('name') is None:
        raise HttpError(409,'缺少参数num,name')
    else:
        return True
def check_and_save(name,number):
    count1=check_number(number)
    count2=check_name(number,name)
    if count1 >=1 and count2 == 0:
        raise HttpError(409,'已经有该用户！')
    elif count1 >=1 and count2 == 1:
        raise HttpError(409,'姓名不正确！')
    elif count1 <1 :
        conn,cursor=get_connection()
        cursor.execute('insert into `students`(`name`,`number`) values (%s,%s)',
                       (name,number))
        conn.commit()
        conn.close()
        cursor.close()
        return ('添加成功！')

