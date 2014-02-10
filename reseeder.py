r'''

This is an implementation of version 1 of the I2P reseed protocol.

See ./original-php-reseeder/reseed_mysql.php for a reference
implementation.

TODO Link to protocol specifications or write it here.

TODO: Need way to reload netDb database from disk.
      1) do at regular interval
      2) monitor directory tree and reload when changed

'''

import os
import time
import errno
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

    # Number of routers to return. Please do *not* change this!
    ROUTER_COUNT = 60

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

    # How often to clear HostCache (in seconds)
    cache_clear_interval = 24*3600
    # Unix timestamp of when to clear cache.
    cache_clear_ts = 0

    # Maps URLs to handler methods.
    urlmap = Map ((
        Rule ('/',                          endpoint = 'index'),
        Rule ('/routerInfo-<b64hash>.dat',  endpoint = 'get-file'),
    ))


    # Constructor
    def __init__ (self, netdb_path):
        self.netdb_path = netdb_path
        self.routers = netdb.load (netdb_path)
        print 'Loaded %d routers from: %s' % (len(self.routers), netdb_path)


    ## Handlers

    # @todo ETag?
    def handle_get_file (self, request, b64hash):
        name = 'routerInfo-' + b64hash + '.dat'
        prefix = 'r' + b64hash[0]
        filename = os.path.join (self.netdb_path, prefix, name)
        try:
            res = Response (wrap_file (request.environ, open(filename, 'rb')),
                            content_type = 'application/octet-stream',
                            direct_passthrough = True)
            res.headers.add ('Content-Length', os.path.getsize (filename))
            return res
        except IOError, err:
            if err.errno not in (errno.ENOENT,): raise
            raise NotFound()


    # Render index page listing all files
    # @todo faster to use cStringIO to buffer output?
    def render (self, router_ids):
        yield '<html><head><title>NetDB</title></head><body><ul>'
        for rid in router_ids:
            # new
            #b64hash = self.routers[rid]
            #name = 'routerInfo-' + b64hash + '.dat'
            tp = self.routers[rid]
            url = tp[1]
            #url = '/'.join(tp)
            name = tp[1]
            yield '<li><a href="%s">%s</a></li>' % (url, name)
            #yield '<li><a href="/netDb/%s">%s</a></li>' % (url, name)
        yield '</ul></body></html>'


    def handle_index (self, req):
        self.expire_host_cache()
        addr = req.remote_addr
        if not addr in self.HostCache:
            sz = len(self.routers)
            rids = random_sample (xrange(sz), min(sz, self.ROUTER_COUNT))
            self.HostCache[addr] = rids
        else:
            rids = self.HostCache[addr]
        return Response (self.render(rids), mimetype='text/html')


    # Clear the host cache every 24 hours.
    # Note: It might be better to store a TTL on each entry and remove
    # entries based on that. This is probably faster and simpler.
    def expire_host_cache (self):
        if time.time() < self.cache_clear_ts: return
        print 'expire-host-cache: removed %d entries.' % len(self.HostCache)
        self.HostCache.clear()
        self.cache_clear_ts = time.time() + self.cache_clear_interval



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
	    # @todo if not httexec print it
            #print 'ERROR:', type(e)
            return e

    # Note: This can be overridden by middleware
    def wsgi (self, environ, start_response):
        return self.dispatch (Request(environ)) (environ, start_response)

    # WSGI entry point
    def __call__ (self, environ, start_response):
        return self.wsgi (environ, start_response)
