import datetime
import uuid
import jwt

from flask import jsonify, request, make_response, Blueprint
from service.db import db
from sqlalchemy import func, cast, Date
from models.models import User, Post, Like

from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
from config import SECRET_KEY, TOKEN_EXPIRATION_TIME


main_blueprint = Blueprint('views', __name__)


def token_required(f):
    """
    Decorator to check a token
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message': 'Missing token!'}), 401

        try:
            data = jwt.decode(token, SECRET_KEY)
        except jwt.ExpiredSignatureError:
            return jsonify({"message": "Token expired, log in again!"})

        current_user = User.query.filter_by(id=data['id']).first()

        if not current_user:
            return jsonify({'message': 'Invalid token!'}), 401

        current_user.update_last_action()
        return f(current_user, *args, **kwargs)

    return decorated

# Function exists for the testing purposes
@main_blueprint.route('/users', methods=['GET'])
def get_all_users():
    """
    Get a list of all users
    """
    users = User.query.all()

    output = []
    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['last_login'] = user.last_login
        user_data['last_action'] = user.last_action
        output.append(user_data)

    return jsonify({'users': output})

@main_blueprint.route('/signup', methods=['POST'])
def create_user():
    """
    Sign up with credentials
    """
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    id = str(uuid.uuid4())

    new_user = User(id=id, username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'New user created!'})

@main_blueprint.route('/login')
def login():
    """
    Log in with credentials and get a token
    """
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify',
                             401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify',
                             401,
                             {'WWW-Authenticate': 'Basic realm="Login required!"'})

    user.update_last_login()
    user.update_last_action()
    
    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=TOKEN_EXPIRATION_TIME)},
                           SECRET_KEY)

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401,
                         {'WWW-Authenticate': 'Basic realm="Login required!"'})

@main_blueprint.route('/post', methods=['GET'])
@token_required
def get_user_posts(current_user):
    """
    Get a list of specified user's posts 
    """
    posts = Post.query.filter_by(author_id=current_user.id).all()

    output = []
    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['author_id'] = post.author_id
        post_data['text'] = post.text
        post_data['liked_by'] = str(post.liked_by.all())
        output.append(post_data)

    return jsonify({'posts': output})

# Function exists for the testing purposes
@main_blueprint.route('/posts', methods=['GET'])
def get_all_posts():
    """
    Get a list of all the posts
    """
    posts = Post.query.all()

    output = []
    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['author_id'] = post.author_id
        post_data['text'] = post.text
        post_data['liked_by'] = str(post.liked_by.all())
        output.append(post_data)

    return jsonify({'posts': output})

@main_blueprint.route('/post', methods=['POST'])
@token_required
def create_post(current_user):
    """
    Create a new post
    """
    data = request.get_json()

    new_post = Post(text=data['text'], author_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message': "Post created!"})

@main_blueprint.route('/<post_id>/like', methods=['POST'])
@token_required
def like_action(current_user, post_id):
    """
    Like/unlike a post
    """
    post = Post.query.filter_by(id=post_id).first()

    if post:
        if not post.is_liked(current_user.id):
            User.query.filter_by(id=current_user.id).first() \
                .like_post(post_id)
            return jsonify({'message': "Post liked!"})
        else:
            User.query.filter_by(id=current_user.id).first() \
                .unlike_post(post_id)
            return jsonify({'message': "Post unliked!"})

    return jsonify({'message': "Invalid post!"})

@main_blueprint.route('/analytics', methods=['GET'])
def analytics():
    """
    Get analytics for likes aggregated by day
    """
    date_from = request.args.get('date_from')
    date_to = request.args.get('date_to')

    result = db.session.query(cast(Like.date, Date), func.count('*')) \
        .filter(cast(Like.date, Date) >= date_from) \
        .filter(cast(Like.date, Date) <= date_to) \
        .group_by(cast(Like.date, Date)).all()

    output = []
    for date in result:
        like_data = {}
        like_data['date'] = date[0]
        like_data['like_count'] = date[1]
        output.append(like_data)

    return jsonify({'analytics': output})
