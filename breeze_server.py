#! /usr/bin/env python
# -*- coding: utf-8 -*-
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
r"""Breeze server application module.

       UTF-8 JSON ->               Py Object ->
Client ------------- Breeze Server ------------ Python Adapter
       <- UTF-8 JSON               <- Py Object
"""
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
import json, collections, pydoc, inspect, bottle, vbem_json
import adapter

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# configuration

ENCODING_PY = adapter.ENCODING_PY
ADPTER_FUNCTIONS = [s for (s,o) in inspect.getmembers(adapter) if inspect.isfunction(o) and not s.startswith('_')]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# common functions

class ThreadingWSGIRefServer(bottle.ServerAdapter):
    def run(self, handler): # pragma: no cover
        import SocketServer, wsgiref.simple_server
        class ThreadingWsgiServer(SocketServer.ThreadingMixIn, wsgiref.simple_server.WSGIServer): pass
        self.options['server_class'] = ThreadingWsgiServer
        if self.quiet:
            class QuietHandler(wsgiref.simple_server.WSGIRequestHandler):
                def log_request(*args, **kw): pass
            self.options['handler_class'] = QuietHandler            
        srv = wsgiref.simple_server.make_server(self.host, self.port, handler, **self.options)
        srv.serve_forever()

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# templates

TPL_ROOT = bottle.SimpleTemplate("""
<title>Breeze Adpter</title>
<frameset rows="50%,*">
    <frameset cols="30%,*">
        <frame src="/debugger" name="frame_debugger" />
        <frame src="about:blank" name="frame_json" />
    </frameset>
    <frame src="/pydoc" name="frame_pydoc" />
</frameset>
""", encoding = 'utf8')

TPL_DEBUGGER = bottle.SimpleTemplate("""
<strong>Breeze Adpter Debugger</strong>
<form action="/json" method="GET" target='frame_json'><small>
    <label>{{oRequest.url.rsplit('/',1)[0]}}/json?fun=<br />
    <select name="fun">
    % for sName in lFunctions:
        <option value="{{ sName }}">{{ sName }}</option>
    % end
    </select><br /></label>
    <label>&args=<br />
    <textarea name="args" cols="40" rows="12"></textarea></label>
    <br /><input type="submit" value="GET" />
    <br /><li>WARNNING: Your IP {{oRequest.remote_addr}} and actions has been recorded for backend server security. Look before you leap.
</small></form>
""", encoding = 'utf8')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# bottle routers

bottle.default_app.push()

@bottle.get('/')
def bottle_get_root():
    bottle.response.content_type = 'text/html; charset=%s' % 'utf8'
    return TPL_ROOT.render()

@bottle.get('/debugger')
def bottle_get_debugger():
    bottle.response.content_type = 'text/html; charset=%s' % 'utf8'
    return TPL_DEBUGGER.render(oRequest=bottle.request, lFunctions=ADPTER_FUNCTIONS)

@bottle.get('/json')
@bottle.post('/json')
def bottle_get_json():
    dReq = bottle.request.forms if bottle.request.method == 'POST' else bottle.request.query
    oFun = getattr(adapter, dReq['fun']) # fun string -> function object
    dArgs = vbem_json.getPy(dReq['args'], sEncodingJson='utf8', sEncodingPy=ENCODING_PY) # args JSON string -> arguments dict with string
    oRet = oFun(**dArgs) # function return object with string
    bottle.response.content_type = 'application/json; charset=%s' % 'utf8'
    return vbem_json.getJson(oRet, sEncodingPy=ENCODING_PY) # return JSON string

@bottle.get('/pydoc')
def bottle_get_pydoc():
    bottle.response.content_type = 'text/html; charset=%s' % 'utf8'
    return pydoc.html.document(*pydoc.resolve(thing=adapter))

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
# main process

def main():
    r"""Main.
    """
    bottle.debug(mode=True)
    bottle.run(
        server = ThreadingWSGIRefServer,
        app = bottle.default_app.pop(), reloader = True,
        host = '0.0.0.0', port = adapter.PORT,
    )

if __name__ == '__main__':
    main()
