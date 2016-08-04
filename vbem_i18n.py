#! /usr/bin/env python
# -*- coding: utf-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""QA internationalization codec library.

"""

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import collections

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# common functions

def transform(oPy, sFrom='utf8', sTo='utf8', sErrors='replace'):
    r"""Transform encoding recusively.
    sFrom: encoding for all string in source object
    sTo: encoding for all basestring in destination object
    NOTE: sTo can be `unicode`
    """
    if isinstance(oPy, basestring):
        u = oPy if isinstance(oPy, unicode) else oPy.decode(encoding=sFrom, errors=sErrors)
        return u if sTo is unicode else u.encode(encoding=sTo, errors=sErrors)
    elif isinstance(oPy, collections.Mapping): # dict
        return type(oPy)((
            transform(oPy=k, sFrom=sFrom, sTo=sTo, sErrors=sErrors),
            transform(oPy=v, sFrom=sFrom, sTo=sTo, sErrors=sErrors),
        ) for (k,v) in oPy.iteritems())
    elif isinstance(oPy, collections.Sequence): # list, tuple (basestring tested above)
        return type(oPy)(transform(oPy=e, sFrom=sFrom, sTo=sTo, sErrors=sErrors) for e in oPy)
    else: # others
        return oPy
        
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main

def _test():
    s = '����1234'
    u = s.decode('gb18030')
    print 'ori', s, repr(s), repr(u)
    
    r = transform(s, sFrom='gbk', sTo='gbk')
    print 'gb-gb', r, repr(r)
    
    r = transform(s, sFrom='gbk', sTo='utf8')
    print 'gb-utf', r, repr(r)

    r = transform(s, sFrom='gbk', sTo=unicode)
    print 'gb-uni', repr(r)
    
    r = transform(u, sFrom=unicode, sTo='gbk')
    print 'uni(gb)->gb', r, repr(r)

    r = transform(u, sFrom=unicode, sTo='utf8')
    print 'uni(gb)->utf', r, repr(r)

    r = transform(u, sFrom=unicode, sTo=unicode)
    print 'uni(gb)->uni', repr(r)

if __name__ == '__main__':
    exit(_test())

