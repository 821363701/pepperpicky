__author__ = 'yuxizhou'

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pymongo import MongoClient
import pymongo


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
        lines.reverse()

        self.render('home.html', lines=lines)


class DenyHandler(tornado.web.RequestHandler):
    def get(self, deny_id):
        deny.append(deny_id)

        with open('deny_id', 'a') as fp:
            fp.write('{}\n'.format(deny_id))
        self.write('0')


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
        lines.reverse()

        self.render('home.html', lines=lines)


class MongoHomeHandler(tornado.web.RequestHandler):
    def get(self):
        limit = int(self.get_argument('limit', 20))

        lines = []
        for l in self.application.c.target_info.find({}, limit=limit).sort('_id', pymongo.DESCENDING):
            lines.append(['http://m.douban.com/group/topic/{}/'.format(l['topic_id']), l['keyword'],
                          '/people/{}/about'.format(l['founder_id']), l['topic_title'], l['timestamp']])

        self.render('home.html', lines=lines)


class MongoDenyHandler(tornado.web.RequestHandler):
    def get(self, deny_id):
        self.application.c.deny_id.insert({
            'deny_id': deny_id
        })

        self.application.c.target_info.remove({
            'founder_id': deny_id
        })

        self.write('0')


class MongoSearchHandler(tornado.web.RequestHandler):
    def get(self):
        self.render('search.html')

    def post(self):
        query = self.get_argument('q')

        lines = []
        for l in self.application.c.target_info.find({
            'founder_id': query
        }).sort('_id', pymongo.DESCENDING):
            lines.append(['http://m.douban.com/group/topic/'+l['topic_id'], l['keyword'],
                          '/people/{}/about'.format(l['founder_id']), l['topic_title'], l['timestamp']])

        self.render('home.html', lines=lines)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True
        )

        _handlers = [
            (r"/pepper", MongoHomeHandler),
            (r"/search", MongoSearchHandler),

            (r"/deny/(.*)", MongoDenyHandler),
        ]

        tornado.web.Application.__init__(self, _handlers, **settings)

        self.c = MongoClient('121.199.5.143').pick


application = Application()


def main():
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()