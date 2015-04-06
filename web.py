# coding=utf-8
__author__ = 'yuxizhou'

import os
import tornado.httpserver
import tornado.ioloop
import tornado.web
from pymongo import MongoClient
import pymongo

LIMIT_DEFAULT = 50


class MongoHandler(tornado.web.RequestHandler):
    def get_all_topic(self, keyword, limit):
        lines = []
        for l in self.application.c.all_topic.find({
            'keyword': keyword,
        }, limit=limit).sort('_id', pymongo.DESCENDING):
            lines.append([l['topic_id'], l['keyword'], l['founder_id'], l['topic_title'], l['timestamp']])

        return lines

    def get_history(self, q):
        lines = []
        for l in self.application.c.all_topic.find({
            'founder_id': q
        }).sort('_id', pymongo.DESCENDING):
            lines.append([l['topic_id'], l['keyword'], l['founder_id'], l['topic_title'], l['timestamp']])

        return lines


class MongoPepperHandler(MongoHandler):
    def get(self):
        limit = int(self.get_argument('limit', LIMIT_DEFAULT))
        lines = self.get_all_topic(u'上海', limit)
        self.render('home.html', lines=lines)


class MongoAllHandler(MongoHandler):
    def get(self, area):
        limit = int(self.get_argument('limit', LIMIT_DEFAULT))
        lines = self.get_all_topic(area, limit)
        self.render('home.html', lines=lines)


class MongoDenyHandler(MongoHandler):
    def get(self, deny_id):
        self.application.c.deny_id.insert({
            'deny_id': deny_id
        })

        self.application.c.all_topic.remove({
            'founder_id': deny_id
        })

        self.write('0')


class MongoSearchHandler(MongoHandler):
    def get(self):
        self.render('search.html')

    def post(self):
        query = self.get_argument('q')
        lines = self.get_history(query)
        self.render('home.html', lines=lines)


class MongoHistoryHandler(MongoHandler):
    def get(self):
        query = self.get_argument('q')
        lines = self.get_history(query)
        self.render('home.html', lines=lines)


pipeline = [
    {
        '$sort': {
            '_id': -1
        }
    },
    {
        '$limit': 1000
    },
    {
        "$group": {
            "_id": "$keyword",
            "count": {
                "$sum": 1
            }
        }
    }
]


class MongoHomeHandler(MongoHandler):
    def get(self):
        result = []

        for i in self.application.c.all_topic.aggregate(pipeline)['result']:
            result.append(i)

        result = sorted(result, key=lambda r: r['count'])
        result.reverse()

        self.render('index.html', result=result)


class Application(tornado.web.Application):
    def __init__(self):
        settings = dict(
            template_path=os.path.join(os.path.dirname(__file__), "templates"),
            debug=True
        )

        _handlers = [
            (r"/", MongoHomeHandler),
            (r"/all/(.*)", MongoAllHandler),
            (r"/pepper", MongoPepperHandler),
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