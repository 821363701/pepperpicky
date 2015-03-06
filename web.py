__author__ = 'yuxizhou'

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        with open('target_info', 'r') as fp:
            raw_lines = fp.readlines()

        lines = []
        for l in raw_lines[-20:]:
            lines.append(l.split('\t'))

        self.render('home.html', lines=lines)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True
        )

        _handlers = [
            (r"/pepper", HomeHandler),
        ]

        tornado.web.Application.__init__(self, _handlers, **settings)


application = Application()


def main():
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()