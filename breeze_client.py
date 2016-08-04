#! /usr/bin/env python
# -*- coding: utf-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Breeze client module.

"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import urllib, vbem_json

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# common functions

def visit(sHostPort, sFun, dArgs, sEncodingPy='utf8', bPost=False):
    r"""Read breeze server.
    """
    sHttp = sHostPort if sHostPort.startswith('http://') else 'http://'+sHostPort
    sJsonArgs = vbem_json.getJson(oPy=dArgs, sEncodingPy=sEncodingPy)
    if bPost:
        sUrl = sHttp + '/json'
        sJsonRet = urllib.urlopen(url=sUrl, data=urllib.urlencode([('fun',sFun),('args',sJsonArgs)])).read()
    else:
        sUrl = sHttp + '/json?' + urllib.urlencode([('fun',sFun),('args',sJsonArgs)])
        sJsonRet = urllib.urlopen(url=sUrl).read()
    oPy = vbem_json.getPy(sJson=sJsonRet, sEncodingJson='utf8', sEncodingPy=sEncodingPy)
    return {
        'url'   : sUrl,
        'json'  : sJsonRet,
        'py'    : oPy,
    }

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main

def _test():
    import pprint
    
    pprint.pprint(visit('localhost:8600','getFilesListByShell',{"sPath":"/home/work"},sEncodingPy='utf8'))

if __name__ == '__main__':
    exit(_test())