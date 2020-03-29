from flask import Flask
from flask import request
from flask_cors import CORS
import sqlite3
from sqlite3 import Error
import json
import os.path
from flask import g
app = Flask(__name__)
cors =CORS(app)


global conf

@app.route('/set_toran',methods=['POST'])
def set_toran():
    data = (json.loads(request.data))
    toran_name=data["label"]
    toran_date = data["value"]
    values = [toran_name,toran_date]
    try:
        for row in g.db.cursor().execute(conf["SQL"]["SQL_Search_if_Exist"].format(conf["DB"]["Table"],toran_date)):
            print(row)
            print("updated")
            g.db.cursor().execute(conf["SQL"]["SQL_Update_Query"].format(conf["DB"]["Table"], toran_name, toran_date))
            g.db.commit()
            break
        else:
            print("inserted")
            g.db.cursor().execute(conf["SQL"]["SQL_Insert_Query"].format(conf["DB"]["Table"], toran_name, toran_date))
            g.db.commit()
    except Exception as e:
        raise(e)
    return 'ff'

@app.route("/get_toranim",methods=['GET'])
def get_toranim():
    dates = (request.args.get("dates").split(','))
    print(conf["SQL"]["SQL_GetToranim_Query"].format(conf["DB"]["Table"], dates))
    toranim_this_week = g.db.cursor().execute(conf["SQL"]["SQL_GetToranim_Query"].format(conf["DB"]["Table"], tuple(dates)))
    g.db.commit()
    print(toranim_this_week)
    return "App is Running"


@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    if hasattr(g, 'db'):
        g.db.close()

def connect_db():
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(conf["DB"]["Database"],check_same_thread=False)
    except Error as e:
        print(e)
    return conn
#
# def insert_toran_to_db(conn,values):
#     try:
#         sql = """INSERT INTO {0} (toran, date) values {1}""".format(conf["DB"]["Table"],values)
#         print(sql)
#         cursor.execute("""INSERT INTO {0} values {1}""".format(conf["DB"]["Table"],tuple(values)))
#         conn.commit()
#     except Exception as e:
#         raise(e)
#


def pull_conf():
    with open(os.path.dirname(__file__) + '/conf.json') as json_file:
        data = json.load(json_file)
    return data


def create_table():
    try:
        conn = sqlite3.connect(conf["DB"]["Database"], check_same_thread=False)
        cursor = conn.cursor()

        cursor.execute("""CREATE TABLE if not exists '{}' (toran text, date text)""".format(conf["DB"]["Table"]))
        conn.commit()
        print("success!")
    except Exception as e:
        print("bla" + str(e))
    finally:
        if (conn):
            conn.close()


if __name__ == '__main__':
    conf = pull_conf()
    create_table()
    app.run()