from datetime import datetime
from service.db import db


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(50), primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    last_login = db.Column(db.DateTime)
    last_action = db.Column(db.DateTime)

    posts = db.relationship('Post', backref='author', lazy='dynamic')
    likes = db.relationship('Like', backref='author', lazy='dynamic')

    def __init__(self, id, username, password):
        if username.isalpha() and password:
            self.id = id
            self.username = username
            self.password = password
            current_time = datetime.now()
            self.last_action = current_time
            self.last_login = current_time
        else:
            raise ValueError

    def like_post(self, post_id):
        like = Like(self.id, post_id)
        db.session.add(like)

    def unlike_post(self, post_id):
        Like.query.filter_by(author_id=self.id, post_id=post_id).delete()

class Post(db.Model):
    __tablename__ = 'post'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(250), nullable=False)

    author_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    liked_by = db.relationship('Like', backref='post', lazy='dynamic')

    def __init__(self, text, author_id):
        if text and author_id:
            self.text = text
            self.author_id = author_id
        else:
            raise ValueError

    def is_liked(self, user_id):
        print(str(self.liked_by.all()))
        return user_id in str(self.liked_by.all())


class Like(db.Model):
    __tablename__ = 'like'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime)

    author_id = db.Column(db.String(50), db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __init__(self, author_id, post_id):
        if author_id and post_id:
            self.author_id = author_id
            self.post_id = post_id
            self.date = datetime.now()
        else:
            raise ValueError
    
    def __repr__(self):
        return self.author_id
