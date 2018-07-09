# coding: utf-8
from __future__ import unicode_literals

import random
import string
import time
from wechat_sdk import WechatBasic
import redis
# from core.models import Area


class WeChatService(object):
    def __init__(self, app_id=None, app_secret=None):
        self.redis = redis.StrictRedis(host='localhost', port=6379, db=2)
        self.app_id = app_id
        self.app_secret = app_secret
        if not app_id:
            self.wechat_admin = Area.objects.all().order_by('id')[0]
            self.wechat = WechatBasic(appid=self.wechat_admin.wx_app_id,
                                      appsecret=self.wechat_admin.wx_secret,
                                      token='123')
            self.app_id = self.wechat_admin.app_id
            self.app_secret = self.wechat_admin.app_secret
        else:
        self.wechat_admin = None
        self.wechat = WechatBasic(appid=app_id, appsecret=app_secret, token='123')

        self.get_token()

    def get_token(self):
        key = 'access_token_{0}'.format(self.app_id)
        token = self.redis.get(key)
        if not token:
            res = self.wechat.grant_token()
            token = res.get('access_token')
            self.redis.set(key, token, 3500)
        return token

    def get_js_ticket(self):
        key = 'js_ticket_{0}'.format(self.app_id)
        ticket = self.redis.get(key)
        if not ticket or ticket == 'None':
            res = self.wechat.get_jsapi_ticket()
            ticket = res.get('jsapi_ticket')
            self.redis.set(key, ticket, 3500)
        return ticket

    def get_random_str(self):
        return string.join(
            random.sample('ZYXWVUTSRQPONMLKJIHGFEDCBA1234567890zyxwvutsrqponmlkjihgfedcbazyxwvutsrqponmlkjihgfedcba',
                          32)).replace(" ", "")

    def get_js_signature(self, url):
        timestamp = int(time.time())
        nostr = self.get_random_str()
        ticket = self.get_js_ticket()
        signature = self.wechat.generate_jsapi_signature(timestamp, nostr, url, ticket)
        return {'timestamp': timestamp, 'ticket': ticket, 'noncestr': nostr, 'url': url, 'signature': signature}

    def send_message(self, open_id, message):
        token = self.get_token()
        req_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token={0}'.format(token)
        message = message.decode('utf-8')
        data = {'touser': open_id,
                'msgtype': 'text',
                'text': {'content': str('测试')}}
        result = requests.post(req_url, data=simplejson.dumps(data))
        return json.loads(result.content)


if __name__ == '__main__':
    ws = WeChatService('wx53a0bb66744d6ff8', '72714e74ea52de8a0917111bb7b4b324')
    print ws.get_js_signature('http://www.rapospectre.com')