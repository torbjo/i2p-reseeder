'''

@deb python-lxml

'''

cnt=0

def application (environ, start_response):
    start_response ('200 OK', [('Content-Type', 'text/html')])
    return generate()

    '''
    global cnt
    start_response ('200 OK', [('Content-Type', 'text/plain')])
    cnt += 1
    return 'Hello looser! You have been here %d times!' % (cnt)
#    yield 'Hello looser! You have been here %d times!' % (cnt)
    '''


import glob
#import etree
#from lxml.html import builder
#import lxml
import lxml.html
from lxml.html import builder as E
#E = lxml.html.builder

def generate():
    root = '/srv/www/i2p-netdb.innovatio.no/htdocs/'
    #prefix = 'htdocs/netdb/'
    files = glob.glob (root + 'netdb/*.dat')
    #files = map (lambda s: s[len(prefix):], files)
    #return str(files[0])
    #print files[0:20]

    L = []
    for filename in files[0:20]:
	xxx = filename[len(root):]
	L.append (E.A (xxx[6:], href=xxx))
	#L.append (E.A (filename, href=filename[len(root):]))
	L.append (E.BR)

    html = E.HTML (
	E.BODY (
	    *L
	)
    )

    # @todo faster to pass back html object?
    return lxml.html.tostring (html)


if __name__ == '__main__':
    print generate()

#    gen = application ({}, lambda *args: None)
#    print gen
#    print gen.next()
