#!/usr/bin/python3.7

import mysql.connector
from transform import read_data, parse_data
from CN_config import mysql_u, mysql_p

def connect_base(user, passwd):
    mydb = mysql.connector.connect(user=user,
                                    passwd=passwd,
                                    host='msitapati.mysql.pythonanywhere-services.com')
    print(f'Successfully connected to MySQL')
    return mydb

def insert_data(mydb, data):
    for i,v in enumerate(data):
        sql = 'INSERT IGNORE INTO articles VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
        mycursor = mydb.cursor()
        mycursor.execute('USE msitapati$crypto_news')
        mycursor.execute(sql, v)
        mydb.commit()

if __name__ == "__main__":
    mydb = connect_base(mysql_u, mysql_p)
    json = read_data()
    data = parse_data(json)
    insert_data(mydb, data)
    print('Success! Data inserted into MySQL')
    print(f'Newest Article: {data[0]}')