__author__ = 'yuxizhou'

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web


deny = []
try:
    with open('deny_id', 'r') as fp:
        for line in fp:
            deny.append(line[:-1])
except IOError:
    print 'no deny_id file'


class HomeHandler(tornado.web.RequestHandler):
    def get(self):
        limit = int(self.get_argument('limit', 20))

        # todo autoreload

        with open('target_info', 'r') as fp:
            raw_lines = fp.readlines()

        lines = []
        for l in raw_lines[-limit:]:
            split_line = l.split('\t')
            if split_line[2].replace('/about', '')[8:-1] in deny:
                continue
            lines.append(split_line)

        self.render('home.html', lines=lines)


class DenyHandler(tornado.web.RequestHandler):
    def get(self, deny_id):
        deny.append(deny_id)

        with open('deny_id', 'a') as fp:
            fp.write('{}\n'.format(deny_id))
        self.write('deny ok')


class SearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search.html')

    def post(self):
        query = self.get_argument('q')

        with open('target_info', 'r') as fp:
            raw_lines = fp.readlines()

        lines = []
        for l in raw_lines:
            split_line = l.split('\t')
            if split_line[2].find(query) > -1:
                lines.append(split_line)

        self.render('home.html', lines=lines)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True
        )

        _handlers = [
            (r"/pepper", HomeHandler),
            (r"/search", SearchHandler),

            (r"/deny/(.*)", DenyHandler),
        ]

        tornado.web.Application.__init__(self, _handlers, **settings)


application = Application()


def main():
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()