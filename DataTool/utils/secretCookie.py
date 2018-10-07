# -*- coding:utf-8 -*- 
# --------------------
# Author:       SDN
# Description:	生成安全cookie码
# Time:         2017/3/1
# --------------------

if __name__ == '__main__':
    import base64, uuid
    print base64.b64encode(uuid.uuid4().bytes + uuid.uuid4().bytes)
