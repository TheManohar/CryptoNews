#!/usr/bin/python3.7

import datetime
import mysql.connector
from load import connect_base
from CN_config import mysql_u, mysql_p

def show_tables(mydb, db_name):
    import mysql.connector
    mycursor = mydb.cursor()
    mycursor.execute(f'USE {db_name}')
    mycursor.execute("SHOW TABLES")
    return [x for x in mycursor]

def show_columns(mydb, db_name, table_name):
    mycursor = mydb.cursor()
    mycursor.execute(f'USE {db_name}')
    mycursor.execute(f'SHOW COLUMNS FROM {table_name}')
    return [x[0] for x in mycursor]

def select_data(mydb, db_name, table_name):
    mycursor = mydb.cursor()
    mycursor.execute(f'USE {db_name}')
    mycursor.execute(f'SHOW COLUMNS FROM {table_name}')
    column_names = [x[0] for x in mycursor]
    mycursor.execute(f'SELECT * FROM {table_name}')
    myresult = mycursor.fetchall()
    return pd.DataFrame(myresult, columns=column_names)

def save_df(df, df_name):
    return df.to_pickle(f'df_data/{df_name}.pkl')

if __name__ == "__main__":
    mydb = connect_base(mysql_u, mysql_p)
    df = select_data(mydb, 'crypto_news', 'articles')
    save_df(df, 'df_articles')