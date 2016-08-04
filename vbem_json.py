#! /usr/bin/env python
# -*- coding: utf-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""QA JSON codec library.

"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import json, vbem_i18n

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# common functions

def getJson(oPy, sEncodingPy='utf8'):
    r"""Encode python object with specified encoding string inside to JSON ASCII string.
    """
    return json.dumps(obj=oPy, encoding=sEncodingPy)
    
def getPy(sJson, sEncodingJson='utf8', sEncodingPy='utf8', sErrors='replace'):
    r"""Decode specified encoding JSON string to python object with only specified encoding string inside.
    NOTE: sEncodingPy can be `unicode`
    """
    uJson = vbem_i18n.transform(oPy=sJson, sFrom=sEncodingJson , sTo=unicode, sErrors=sErrors)
    oPyU = json.loads(s=uJson)
    return oPyU if sEncodingPy is unicode else vbem_i18n.transform(oPy=oPyU, sTo=sEncodingPy, sErrors=sErrors)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main

def _test():
    sJson = '{"a":"����1","b":["����2","english",255]}'
    print 'JSON ori:',sJson
    
    oPy2 = getPy(sJson, sEncodingJson='gb18030', sEncodingPy='gb18030')
    print 'Python GB:',oPy2
    print 'reverse', getJson(oPy2, sEncodingPy='gb18030')
    
    oPy3 = getPy(sJson, sEncodingJson='gb18030', sEncodingPy='utf8')
    print 'Python UTF:',oPy3
    print 'reverse', getJson(oPy3, sEncodingPy='utf-8')
    
    oPy4 = getPy(sJson, sEncodingJson='gb18030', sEncodingPy=unicode)
    print 'Python Unicode:',oPy4
    print 'reverse', getJson(oPy4, sEncodingPy='utf-8')

if __name__ == '__main__':
    exit(_test())
    
