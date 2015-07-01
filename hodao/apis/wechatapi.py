# coding:utf8
"""

Author: ilcwd
"""

import flask
from wechat.server import (
    WechatApplication,
    text_reply,
    news_reply,

    EVENT_SUBSCRIBE,
    MSG_TEXT,
)


from hodao.core import application, C
from hodao import util


wechatapp = WechatApplication(application, '/api/wechat', C.WECHAT_TOKEN)


@wechatapp.text('A')
@wechatapp.text('a')
def express_service():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """【<a href="%s">猛戳蓝字</a>】提交、查询订单\n"""
        """了解怎么取件请回复：帮助"""
    ) % (util.make_auth_url(to_user, redirect='/order/create'),)
    return text_reply(from_user, to_user, content)


@wechatapp.text('B')
@wechatapp.text('b')
def hoshop_service():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """进入Ho-shop【<a href="%s">请点击蓝字</a>】\n"""
        """寻求合作请回复：E"""
    ) % util.make_hoshop_url(to_user)
    return text_reply(from_user, to_user, content)


@wechatapp.text('C')
@wechatapp.text('c')
def dalaba_service():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """请输入 #大喇叭#你想说的话\n"""
    )
    return text_reply(from_user, to_user, content)


@wechatapp.text('D')
@wechatapp.text('d')
def bd_service():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """请联系我们的客服微信：xhkddq\n"""
        """或者致电：13-2468-68361 K先生\n"""
    )
    return text_reply(from_user, to_user, content)


@wechatapp.text('E')
@wechatapp.text('e')
def client_service():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """客服代表：\n"""
        """Ho道调侃帝 微信号：xhkddq\n"""
    )
    return text_reply(from_user, to_user, content)


@wechatapp.text(u'.*大喇叭.*', is_re=True)
def dalaba_reply():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """Ho道已经听到你想说的话，待客服审核后将帮你群发~\n"""
    )
    return text_reply(from_user, to_user, content)


@wechatapp.text(u'帮助')
def qujian_reply():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    article = [
        "快递代理服务须知，请花几分钟时间看完，谢谢",
        "",
        r"https://mmbiz.qlogo.cn/mmbiz/fUvZSJMfnNEoOsUGf9WuRA3FB5lquqFIlu9Tv5NHLicwiaJJhwiaRR7alv0klmSXSrvEQrr7pMDSibgnZudcrEsVxA/0",
        r"http://mp.weixin.qq.com/s?__biz=MzA4MDI2NjMyOA==&mid=201293892&idx=1&sn=4ecde436ca20ee0bddf13273a4ed6ba0#rd"
    ]

    return news_reply(from_user, to_user, [article])


@wechatapp.text(C.SERVER_MANAGEMENT_MAGIC_WORD)
def express_service():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """管理员好！\n"""
        """【<a href="%s">猛戳蓝字</a>】\n"""
        """管理订单。"""
    ) % (util.make_auth_url(to_user, redirect='/login/'+C.SERVER_MANAGEMENT_MAGIC_WORD),)
    return text_reply(from_user, to_user, content)



@wechatapp.event(EVENT_SUBSCRIBE)
def subscribe_msg():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """星海用Ho道！生活无难度～/礼物/礼物\n\n"""
        """【<a href="%s">点击进入Ho道菜单</a>】\n\n"""
        """【<a href="http://mp.weixin.qq.com/s?__biz=MzA4MDI2NjMyOA==&mid=213306361&idx=2&sn=eddd15c8099b9b75d66f4ee7136e9cdc#rd">点击获取《不小心》音乐会介绍</a>】 \n\n"""
        """找客服，请回复：E\n"""

        # """B. Ho-shop\n"""
        # """C. Ho道大喇叭\n"""
        # """D. 寻求合作\n"""
        # """E. 人工服务\n"""
        # """如回复：A\n"""
        %
        (
            util.make_auth_url(to_user, redirect='/order/create'),
        )
    )
    return text_reply(from_user, to_user, content)


@wechatapp.message(MSG_TEXT)
def help_msg():
    from_user = flask.g.wechat['ToUserName']
    to_user = flask.g.wechat['FromUserName']

    content = (
        """星海用Ho道！生活无难度～/礼物/礼物\n\n"""
        """【<a href="%s">点击进入Ho道菜单</a>】\n\n"""
        """【<a href="http://mp.weixin.qq.com/s?__biz=MzA4MDI2NjMyOA==&mid=213306361&idx=2&sn=eddd15c8099b9b75d66f4ee7136e9cdc#rd">点击获取《不小心》音乐会介绍</a>】 \n\n"""
        """找客服，请回复：E\n"""
        %
        (
            util.make_auth_url(to_user, redirect='/order/create'),
        )
    )
    return text_reply(from_user, to_user, content)
