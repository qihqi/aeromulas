import json
import asyncio
import datetime
import calendar
import sys 
from asyncio import coroutine
from aiohttp import web

from .models import Store, Post, Base, Comment

store = Store()


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
def extract_json(request):
    body = yield from request.content.read()
    body = body.decode('utf8')
    content = json.loads(body)
    return content


@coroutine
def get_posts(request):
    result = { 
        'result': 
            [(p.uid, p.title, p.timestamp, p.posted_by) for p in store.get_newest_posts()]
    }
    return web.Response(body=json_dumps(result))

@coroutine
def get_post_by_id(request):
    uid = request.match_info.get('uid') 
    post = store.get_full_post_by_id(uid)
    return web.Response(body=json_dumps(post))


@coroutine 
def post_comment(request):
    uid = request.match_info.get('uid') 
    content = yield from extract_json(request)
    comment = Comment(**content)
    store.add_comment(uid, content)
    return web.Response(body='{"status": "success"}'.encode('utf8'))


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
    app.router.add_route('GET', '/api/post', get_posts)
    app.router.add_route('GET', '/api/post/{uid}', get_post_by_id)
    app.router.add_route('POST', '/api/post/{uid}/comments', post_comment)
    app.router.add_route('POST', '/api/post', create_post)
    if 'test' in sys.argv:
        app.router.add_static('/', './dist')
    srv = yield from loop.create_server(app.make_handler(), '0.0.0.0', 8000)
    return srv


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(init(loop))
    if 'test' in sys.argv:
        import subprocess
        subprocess.call(['webpack', '-p'])
        print('webpack generation finished')
    loop.run_forever()
