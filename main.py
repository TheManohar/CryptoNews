from extract import get_news_t
import datetime
import time

qInTitle = 'crypto OR bitcoin OR ethereum'

if __name__=='__main__':
    while True:
        get_news_t(qInTitle)
        print(f'Created: NEWS for {qInTitle} {datetime.datetime.now().strftime("%y%m%d-%H%M%S")}')
        time.sleep(300)