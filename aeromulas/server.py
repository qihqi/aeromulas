import json
import asyncio
import datetime
import calendar
from asyncio import coroutine
from aiohttp import web

from .models import Store, Post, Base

store = Store()

def serialize(model):
    return model.__dict__

class ObjEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, Base):
            return obj.__dict__
        if isinstance(obj, datetime.datetime):
            return calendar.timegm(obj.timetuple())
        return json.JSONDecoder.default(self, obj)


def json_dumps(content):
    return json.dumps(content, cls=ObjEncoder).encode('utf8')

@coroutine
def get_posts(request):
    result = { 
        'result': 
            [(p.title, p.timestamp, p.posted_by) for p in store.get_newest_posts()]
    }
    return web.Response(body=json_dumps(result))

@coroutine
def create_post(request):
    body = yield from request.content.read()
    body = body.decode('utf8')
    print(body)
    content = json.loads(body)
    post = Post(**content)
    store.add_post(post)
    return web.Response(body='{"status": "success"}'.encode('utf8'))
    
    
@coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/api/post/', get_posts)
    app.router.add_route('POST', '/api/post/', create_post)
    srv = yield from loop.create_server(app.make_handler(), '0.0.0.0', 8000)
    return srv


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    loop.run_forever()
