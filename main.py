import v1

Reseeder = v1.Reseeder


if __name__ == '__main__':
    import sys
    from werkzeug.serving import run_simple
    #run_simple ('localhost', 80, Reseeder())
    #app = Reseeder (NETDB)
    app = Reseeder (sys.argv[1])
    run_simple ('localhost', 8080, app, use_debugger=True, use_reloader=True)
