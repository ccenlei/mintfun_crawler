#!/usr/bin/python3


from sanic.response import HTTPResponse, json
from sanic.views import HTTPMethodView

from utils import database_utils


# 用户数据操作路由
class UserDataView(HTTPMethodView):
    # 此处应链接数据库操作，但前期条件有限，直接读取文件即可
    async def get(self, request) -> HTTPResponse:
        datas = database_utils.user_select_all()
        user_list = []
        for data in datas:
            name = data['name']
            host = data['host']
            # 数据脱敏
            lens = len(name)
            name_midd = name[1:lens - 1]
            name_str = name.replace(name_midd, '***')
            user = host.replace(name, name_str)
            user_list.append(user)
        return json(user_list)


# NFT数据操作路由
class NftDataView(HTTPMethodView):
    # 此处应链接数据库操作，但前期条件有限，直接读取内存即可
    async def get(self, request) -> HTTPResponse:
        nft_data = database_utils.nft_select_new()
        # nft_data.json = database_utils.NftData('123')
        # nft_data.json.name = 'test'
        # nft_data.json.total_mints = 90
        # nft_data.json.twitter = 'https://twitter.com/i/timeline'
        # nft_data.json.opensea = 'https://twitter.com/i/timeline'
        if nft_data == 0:
            resp_map = {"status": 404, "message": "no nft now."}
            return json(resp_map)
        return json(nft_data.to_map())
