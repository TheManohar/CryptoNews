#!/usr/bin/python3.7

import pandas as pd
from load import connect_base
from CN_config import mysql_u, mysql_p

def show_tables(db_name):
    mydb = connect_base(mysql_u, mysql_p)
    mycursor = mydb.cursor()
    mycursor.execute(f'USE {db_name}')
    mycursor.execute("SHOW TABLES")
    mydb.close()
    return [x for x in mycursor]

def show_columns(db_name, table_name):
    mydb = connect_base(mysql_u, mysql_p)
    mycursor = mydb.cursor()
    mycursor.execute(f'USE {db_name}')
    mycursor.execute(f'SHOW COLUMNS FROM {table_name}')
    mydb.close()
    return [x[0] for x in mycursor]

def select_data(db_name, table_name):
    mydb = connect_base(mysql_u, mysql_p)
    mycursor = mydb.cursor()
    mycursor.execute(f'USE {db_name}')
    mycursor.execute(f'SHOW COLUMNS FROM {table_name}')
    column_names = [x[0] for x in mycursor]
    mycursor.execute(f'SELECT * FROM {table_name}')
    myresult = mycursor.fetchall()
    df = pd.DataFrame(myresult, columns=column_names)
    df.name = f'df_{table_name}'
    mydb.close()
    return df

def save_df(df):
    return df.to_pickle(f'/home/msitapati/CryptoNews/df_data/{df.name}.pkl')

if __name__ == "__main__":
    mydb = connect_base(mysql_u, mysql_p)
    df = select_data(mydb, 'msitapati$crypto_news', 'articles')
    save_df(df)
    print(f'CREATED: {df.name}.pkl')