#!/usr/bin/python3

# 获取 featured project 数据并推送
import requests

from utils import database_utils
from utils.database_utils import NftData
from utils.mint_utils import MailSender

heads = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0'}

# feature抓取相关参数
feature_url = 'https://mint.fun/api/mintfun/featured-project'
feature_title = '精品NFT mint!'

# nft数据提取相关参数
nft_data_url = 'https://mint.fun/api/copy-mint/contract/%s'

# eth price抓取相关参数
eht_price_url = 'https://www.binance.com/api/v1/aggTrades?limit=80&symbol=ETHBUSD'
eth_title = 'eth价格监控'


# feature project抓取方法
def feature_crawler(mail: MailSender):
    response = requests.get(url=feature_url, headers=heads, timeout=12)
    json_data = response.json()
    response.close()
    project = json_data['featuredProject']
    if project is None:
        print('Now, no featured project.')
        return
    # 提取数据(name, twitter)，判断是否已抓过，发送新邮件
    collection = project['collection']
    contract = collection['contract']
    nft_data_now = database_utils.nft_select_new()
    last_feature_project = nft_data_now.contract
    if last_feature_project == contract:
        print('project has been crawled.')
        return
    name = collection['name']
    urls = collection['urls']
    total_mints = collection['totalMints']
    twitter = ''
    opensea = ''
    for urll in urls:
        types = urll['type']
        url = urll['url']
        if 'twitter' == types:
            twitter = url
        elif 'opensea' == types:
            opensea = url
        else:
            pass
    nft_data = NftData(contract)
    nft_data.name = name
    nft_data.total_mints = total_mints
    nft_data.twitter = twitter
    nft_data.opensea = opensea
    mail.mail(feature_title, nft_data.to_str())
    database_utils.nft_insert(nft_data)


# 提取nft数据，0xf1fd63cdb29900a0035cdc8196e56207e087407f
def nft_crawler(contract: str):
    url = nft_data_url % contract
    response = requests.get(url=url, headers=heads, timeout=12)
    json_data = response.json()
    response.close()
    collection = json_data['collection']
    name = collection['name']
    urls = collection['urls']
    total_mints = collection['totalMints']
    twitter = ''
    opensea = ''
    for urll in urls:
        types = urll['type']
        url = urll['url']
        if 'twitter' == types:
            twitter = url
        elif 'opensea' == types:
            opensea = url
        else:
            pass
    message = ' 合约地址：%s\n\n 项目名称：%s\n\n mint总计：%d\n\n twitter：%s\n\n opensea：%s' % (
        contract, name, total_mints, twitter, opensea)
    print(message)


# eth price抓取方法
def eth_crawler(mail: MailSender):
    response = requests.get(url=eht_price_url, headers=heads, timeout=12)
    json_data = response.json()
    response.close()
    price = json_data[0]['p']
    vol = json_data[0]['q']
    msg = '最新eth挂单价格 %s 成交量 %s .' % (price, vol)
    print(msg)
    price_int = float(price)
    if price_int < 550:
        print(price_int)
        mail.mail(eth_title, msg)
