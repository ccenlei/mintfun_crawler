#!/usr/bin/python3

from sanic import Sanic
from sanic.response import HTTPResponse, file
from sanic_ext import Extend

from views.mint_views import UserDataView, NftDataView

# 服务创建
app = Sanic(name="MINT_NFT_INVALIDATOR")
app.add_route(UserDataView.as_view(), "/user")
app.add_route(NftDataView.as_view(), "/nft")
Extend(app)  # http://localhost:8000/docs/swagger


@app.get("/")
async def index(request) -> HTTPResponse:
    return await file("htmls/index.html")


@app.get("/signin")
async def register(request) -> HTTPResponse:
    return await file("htmls/user.html")
