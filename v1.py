r'''

This is an implementation of version 1 of the I2P reseed protocol.

See ./original-php-reseeder/reseed_mysql.php for a reference
implementation.

TODO Link to protocol specifications or write it here.

'''

import os
from random import sample as random_sample

import netdb
#from netdb import load as load_netdb

# We need some tools to ease WSGI development.
from werkzeug.wrappers import Request, Response
from werkzeug.routing import Map, Rule
from werkzeug.exceptions import HTTPException, NotFound
from werkzeug.wsgi import wrap_file


class Reseeder (object):
    ''' I2P reseeder WSGI application '''

    # Number of routers to return
    ROUTER_COUNT = 25

    # NetDB database. Each entry is a tuple of (prefix, filename)
    routers = []

    # Want to return same set of routers to each host, to make more
    # resilient against enumeration attacks.
    # key = ip-addr
    # val = list of router ids (rid)  [router = self.routers[rid]]
    # @todo should flush this cache at regular intervals.
    #       - can add ttl to each entry, then run cleanup regularly
    #       - or just restart the whole app every nth hours
    HostCache = dict()


    #URLMAP = Map
    urlmap = Map ((
        Rule ('/',                          endpoint = 'index'),
        Rule ('/netDb/<prefix>/<name>',     endpoint = 'get-file'),
        #Rule ('/netDb/<filename>',         endpoint = 'get-file'),
        #Rule ('/routerInfo-<b64hash>.dat', endpoint = 'get-file'),
    ))

    def __init__ (self, netdb_path):
        self.netdb_path = netdb_path
        self.routers = netdb.load (netdb_path)


    ## Handlers

    # @todo ETag?
    def handle_get_file (self, request, prefix, name):
        filename = os.path.join (self.netdb_path, prefix, name)
        res = Response (wrap_file (request.environ, open(filename)),
                        content_type = 'application/octet-stream',
                        direct_passthrough = True)
        res.headers.add ('Content-Length', os.path.getsize (filename))
        return res


    # Render index page listing all files
    # @todo faster to use cStringIO to buffer output?
    def render (self, router_ids):
        yield '<body><ul>'
        for rid in router_ids:
            tp = self.routers[rid]
            url = '/'.join(tp)
            name = tp[1]
            yield '<li><a href="/netDb/%s">%s</a></li>' % (url, name)
        yield '</ul></body>'


    def handle_index (self, req):
        addr = req.remote_addr
        if not addr in self.HostCache:
            rids = random_sample (xrange(len(self.routers)), self.ROUTER_COUNT)
            self.HostCache[addr] = rids
        else:
            rids = self.HostCache[addr]
        return Response (self.render(rids), mimetype='text/html')



    ## WSGI glue code bellow

    # Dispatch request based on self.urlmaps to self.handle_*
    def dispatch (self, request):
        adapter = self.urlmap.bind_to_environ (request.environ)
        try:
            endpoint, values = adapter.match()
            func = getattr (self, 'handle_' + endpoint.replace('-', '_'), None)
            if func: return func (request, **values)
            else: return Response ('No handler for: ' + endpoint, status=500)
        except HTTPException, e:
            print 'ERROR:', type(e)
            return e

    # Note: This can be overriden by middleware
    def wsgi (self, environ, start_response):
        return self.dispatch (Request(environ)) (environ, start_response)

    # WSGI entry point
    def __call__ (self, environ, start_response):
        return self.wsgi (environ, start_response)
