#!/usr/bin/python3.7

import datetime
import mysql.connector
from load import connect_base
from CN_config import mysql_u, mysql_p

def show_tables(mydb):
    import mysql.connector
    mycursor = mydb.cursor()
    mycursor.execute("SHOW TABLES")
    print('Tables in current DB:')
    for x in mycursor:
        print(x)
    return mycursor

def select_data(mydb):
    mycursor = mydb.cursor()
    mycursor.execute('SELECT * FROM articles')
    myresult = mycursor.fetchall()
    return pd.DataFrame(myresult, columns=['publishedAt', 'source', 'source_id', 'author', 'title', 'description', 'content', 'url'])

def save_df(df, df_name):
    return df.to_pickle(f'{datetime.datetime.now().strftime("%y%m%d-%H%M%S")}-{df_name}.pkl')

if __name__ == "__main__":
    mydb = connect_base(mysql_u, mysql_p)
    df = select_data(mydb)
    save_df(df)