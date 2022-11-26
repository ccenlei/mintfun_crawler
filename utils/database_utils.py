#!/usr/bin/python3
import json


# ====================================用户数据操作====================================
def user_select_all():
    return [{'name': 'coushi', 'host': 'coushi@skiff.com'},
            {'name': 'eosqianyeliu', 'host': 'eosqianyeliu@gmail.com'},
            {'name': 'home666888', 'host': 'home666888@outlook.com'}]


# ====================================NFT数据操作====================================
class NftData:
    contract = ''
    name = ''
    total_mints = 0
    twitter = ''
    discord = ''
    opensea = ''
    mint_url = ''

    def __init__(self, contract: str):
        self.contract = contract
        self.mint_url = 'https://mint.fun/' + contract

    def to_str(self):
        return ' 合约地址：%s\n\n 项目名称：%s\n\n mint总计：%d\n\n twitter：%s\n\n discord：%s\n\n opensea：%s\n\n mint_url：%s' % (
            self.contract, self.name, self.total_mints, self.twitter, self.discord, self.opensea, self.mint_url)

    def to_map(self):
        return {'contract': self.contract, 'name': self.name, 'total_mints': self.total_mints,
                'twitter': self.twitter, 'discord': self.discord, 'opensea': self.opensea, 'mint_url': self.mint_url}


nft_list = [0]
path = './views/nft_data.json'


def nft_insert(nft: NftData):
    # 存入抓取到的精品nft
    nft_list[0] = nft
    file = open(path, mode='w+')
    maps = nft.to_map()
    data = json.dumps(maps)
    file.write(data)
    file.close()


def nft_select_new():
    # 查询最新抓取的nft
    nft = nft_list[0]
    if nft == 0:
        file = open(path, mode='r')
        data = file.read()
        maps = json.loads(data)
        file.close()
        nft = NftData(maps['contract'])
        nft.name = maps['name']
        nft.total_mints = maps['total_mints']
        nft.twitter = maps['twitter']
        nft.discord = maps['discord']
        nft.opensea = maps['opensea']
        nft_list[0] = nft
    return nft
