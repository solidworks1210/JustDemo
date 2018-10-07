# -*- coding:utf-8 -*- 
# --------------------
# Author:		Ken
# Description:	MD5工具类
# --------------------


def md5(strg):
    import hashlib
    import types
    if isinstance(strg, types.StringType):
        m = hashlib.md5()
        m.update(strg)
        result = m.hexdigest()
        return result
    elif type(strg) == type(u''):
        temp = strg.encode('utf-8')
        m = hashlib.md5()
        m.update(temp)
        result = m.hexdigest()
        # print 'msid', result
        return result
    else:
        return None

if __name__ == '__main__':
    import sys
    if len(sys.argv) == 2:
        print md5(sys.argv[1])

