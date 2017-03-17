from tornado.options import options, define, parse_command_line
# import django.core.handlers.wsgi
from django.core.wsgi import get_wsgi_application
import tornado.httpserver
import tornado.ioloop
import tornado.web
import tornado.wsgi
import os
define('port', type=int, default=8001)

def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog.settings")
    parse_command_line()
    # wsgi_app = tornado.wsgi.WSGIContainer(django.core.handlers.wsgi.WSGIHandler())
    wsgi_app = tornado.wsgi.WSGIContainer(get_wsgi_application())
    tornado_app = tornado.web.Application([
      (r'/static/(.*)', tornado.web.StaticFileHandler, {'path': os.path.join(os.path.join(os.getcwd()),"app/static")}),
      ('.*', tornado.web.FallbackHandler, dict(fallback=wsgi_app)),
    ])
    server = tornado.httpserver.HTTPServer(tornado_app)
    server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()

if __name__ == '__main__':
    main()