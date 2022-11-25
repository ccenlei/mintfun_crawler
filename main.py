#!/usr/bin/python3
from apscheduler.schedulers.background import BackgroundScheduler

import server
from utils.mint_utils import MailSender
from datetime import datetime
import mint_crawler


def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press ⌘F8 to toggle the breakpoint.


def feature_job():
    # 抓取feature project的任务
    return mint_crawler.feature_crawler(mail)


def eth_price_job():
    # 抓取eth price的任务
    return mint_crawler.eth_crawler(mail)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('Python Crawler...')
    secret = input('请输入口令：')
    mail = MailSender(secret)

    # mint_crawler.nft_crawler('0xf1fd63cdb29900a0035cdc8196e56207e087407f')

    # 详见： https://zhuanlan.zhihu.com/p/144506204
    scheduler = BackgroundScheduler()
    # minutes seconds
    scheduler.add_job(feature_job, 'interval', minutes=1, next_run_time=datetime.now())
    scheduler.start()

    server.app.run(port=8081)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
