import os
import sys

project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(project_dir)

from utils import rpc_client
from werkzeug import security

if __name__ == '__main__':
    username = input("please input username[6-20]:")
    password = input("please input password[6-20]:")
    try:
        rpc_client.rpc_proxy.create_user(username=username, password=security.generate_password_hash(password=password))
    except Exception as e:
        print(e)
