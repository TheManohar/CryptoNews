#!/usr/bin/python3.7

from flask import Flask, jsonify, redirect
import mysql.connector
from CN_config import mysql_u, mysql_p


app = Flask(__name__)
#app.config["DEBUG"] = True

@app.route('/')
def hello_world():
    return redirect('/api/v1.0/articles')

@app.route('/api/v1.0/articles', methods=['GET'])
def get_source():
    #sources = []
    mydb = mysql.connector.connect(user=mysql_u,
                                    passwd=mysql_p,
                                    host='msitapati.mysql.pythonanywhere-services.com')
    qry = 'SELECT * FROM articles ORDER BY publishedAt DESC;'
    mycursor = mydb.cursor()
    mycursor.execute('USE msitapati$crypto_news')
    mycursor.execute(qry)
    rows = mycursor.fetchall()
    parsed_data = []
    for row in rows:
        publishedAt = row[0]
        source = row[1]
        source_id = row[2]
        author = row[3]
        title = row[4]
        description = row[5]
        content = row[6]
        url = row[7]
        fields = {'publishedAt' : publishedAt,
                  'source' : source,
                  'source_id' : source_id,
                  'author' : author,
                  'title' : title,
                  'description' : description,
                  'content' : content,
                  'url' : url}
        parsed_data.append(fields)
    return jsonify({'articles': parsed_data})