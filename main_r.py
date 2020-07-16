import datetime
import time
from extract import get_news_t
from load import connect_base, insert_data
from transform import read_data, parse_data
from db_dump import select_data, save_df
from data_analysis import save_dash_df
from data_analysis import get_df_clean, get_df_daily
from CN_config import mysql_u, mysql_p

qInTitle = 'crypto OR bitcoin OR ethereum'

if __name__=='__main__':
    while True:
        get_news_t(qInTitle)
        print(f'Created: JSON for {qInTitle} {datetime.datetime.now().strftime("%y%m%d-%H%M%S")}')

        data = read_data()
        parsed_data = parse_data(data)
        print('Success! Data has been Parsed')

        #mydb = connect_base(mysql_u, mysql_p)
        insert_data(parsed_data)
        print('Success! Data instered into MySQL')

        print(f'Newest article: {parsed_data[0]}')

        df = select_data('msitapati$crypto_news', 'articles')
        save_df(df)
        print(f'CREATED: {df.name}.pkl')

        df_clean = get_df_clean()
        df_daily = get_df_daily()
        save_dash_df(df_clean)
        print(f'CREATED: {df_clean.name}.pkl')
        save_dash_df(df_daily)
        print(f'CREATED: {df_daily.name}.pkl')

        time.sleep(3600)