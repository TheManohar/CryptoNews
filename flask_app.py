
# A very simple Flask Hello World app for you to get started with...

from flask import Flask, jsonify, abort, redirect
import mysql.connector
from CN_config import mysql_u, mysql_p


app = Flask(__name__)
#app.config["DEBUG"] = True

@app.route('/')
def hello_world():
    return redirect('/api/v1.0/articles')

@app.route('/api/v1.0/articles', methods=['GET'])
def get_source():
    sources = []
    mydb = mysql.connector.connect(user=mysql_u,
                                    passwd=mysql_p,
                                    host='msitapati.mysql.pythonanywhere-services.com')
    qry = 'SELECT * FROM articles;'
    mycursor = mydb.cursor()
    mycursor.execute('USE msitapati$crypto_news')
    mycursor.execute(qry)
    rows = mycursor.fetchall()
    for row in rows:
        sources.append(row)
    mycursor.close()
    if len(row) == 0:
        abort(404)
    return jsonify({'articles': sources})