import datetime
import heapq

class Base(object):
    pass


class Post(Base):

    def __init__(self, uid, posted_by, content, title, 
            comments=None, timestamp=None):
        self.uid = uid
        self.posted_by = posted_by
        self.content = content 
        self.title = title
        self.comments = comments
        self.timestamp = timestamp

        if self.comments is None:
            self.comments = []
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now()

    def __lt__(self, other):
        return self.timestamp < other.timestamp


class Comment(Base):

    def __init__(self, uid, posted_by, content, timestamp=None):
        self.uid = uid
        self.posted_by = posted_by
        self.content = content 
        self.timestamp = timestamp
        if self.timestamp is None:
            self.timestamp = datetime.datetime.now()


class User(Base):

    def __init__(self, username, ip_address, cookie, since=None):
        self.username = username
        self.ip_address = ip_address
        self.user_since = datetime.datetime.now()
        self._cookie = None

    @property
    def cookie(self):
        pass



class Store(Base):

    def __init__(self):
        self.timed_posts = []
        self.posts = {}
        self.users = {}
        self.user_by_ip = {}

    def get_user_by_id(self, uid):
        return self.users[uid]

    def get_full_post_by_id(self, uid):
        return self.posts[uid]

    def get_newest_posts(self, count=30):
        return heapq.nlargest(count, self.timed_posts)

    def add_user(self, user):
        self.users[user.username] = user
        self.users_by_ip[user.ip_address] = user

    def add_post(self, post):
        self.posts[post.uid] = post
        heapq.heappush(self.timed_posts, post)

    def add_comment(self, post_id, comment):
        post = self.posts[post_id]
        post.comments.append(comment)

