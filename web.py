__author__ = 'yuxizhou'

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pymongo import MongoClient
import pymongo


class MongoHomeHandler(tornado.web.RequestHandler):
    def get(self):
        limit = int(self.get_argument('limit', 20))

        lines = []
        for l in self.application.c.target_info.find({}, limit=limit).sort('_id', pymongo.DESCENDING):
            lines.append([l['topic_id'], l['keyword'], l['founder_id'], l['topic_title'], l['timestamp']])

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
            lines.append([l['topic_id'], l['keyword'], l['founder_id'], l['topic_title'], l['timestamp']])

        self.render('home.html', lines=lines)


class MongoHistoryHandler(tornado.web.RequestHandler):
    def get(self):
        query = self.get_argument('q')

        lines = []
        for l in self.application.c.target_info.find({
            'founder_id': query
        }).sort('_id', pymongo.DESCENDING):
            lines.append([l['topic_id'], l['keyword'], l['founder_id'], l['topic_title'], l['timestamp']])

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
            (r"/history", MongoHistoryHandler),

            (r"/deny/(.*)", MongoDenyHandler),
        ]

        tornado.web.Application.__init__(self, _handlers, **settings)

        self.c = MongoClient('121.199.5.143').pick
        self.c.visited_topic.ensure_index('topic_id')


application = Application()


def main():
    application.listen(9999)
    tornado.ioloop.IOLoop.instance().start()


if __name__ == "__main__":
    main()