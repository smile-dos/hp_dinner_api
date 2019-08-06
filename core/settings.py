"""
This is configure module.

@author: ZhangDong
"""
DEBUG = True

INSTALL_APPS = [
    "user"
]

SECRET_KEY = b"\x94\x9b\xdb\x91\xb3*\x0c4\x1b}0\xfa\xa4\x90\x81\x86\xed\\\x86\x91~\xda\xd4'\x96\xf3_\x9e\xd6S\x0c\xfe"

RPC_QUEUE = 'happy_dinner_rpc_queue'
RPC_BROKER_URL = 'amqp://config_spider:config_spider@localhost:5672/config_spider'
