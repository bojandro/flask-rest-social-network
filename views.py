from flask import jsonify, request, make_response, Blueprint
from service.db import db
from models.models import User, Post, Like
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import datetime
from config import SECRET_KEY
import uuid
import jwt


main_blueprint = Blueprint('views', __name__)

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token is missing!'}), 401

        try: 
            data = jwt.decode(token, SECRET_KEY)
            current_user = User.query.filter_by(id=data['id']).first()
        except Exception as e:
            return jsonify({'message' : 'Token is invalid!', 'exception': str(e)}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@main_blueprint.route('/user', methods=['GET'])
def get_all_users():
    users = User.query.all()

    output = []

    for user in users:
        user_data = {}
        user_data['id'] = user.id
        user_data['username'] = user.username
        user_data['password'] = user.password
        output.append(user_data)

    return jsonify({'users' : output})

@main_blueprint.route('/post', methods=['GET'])
@token_required
def get_all_posts(current_user):
    posts = Post.query.filter_by(author_id=current_user.id).all()

    output = []

    for post in posts:
        post_data = {}
        post_data['id'] = post.id
        post_data['author_id'] = post.author_id
        post_data['text'] = post.text
        post_data['liked_by'] = str(post.liked_by.all())
        output.append(post_data)

    return jsonify({'posts' : output})

@main_blueprint.route('/user/<id>', methods=['GET'])
def get_one_user(id):

    user = User.query.filter_by(id=id).first()

    if not user:
        return jsonify({'message' : 'No user found!'})

    user_data = {}
    user_data['id'] = user.id
    user_data['username'] = user.username
    user_data['password'] = user.password

    return jsonify({'user' : user_data})

@main_blueprint.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')
    id = str(uuid.uuid4())
    print(id)
    new_user = User(id=id, username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message' : 'New user created!'})

@main_blueprint.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    user = User.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'id': user.id,
                            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=20)},
                            SECRET_KEY)

        return jsonify({'token': token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

@main_blueprint.route('/post', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.get_json()
    print("DATA:__", data)
    new_post = Post(text=data['text'], author_id=current_user.id)
    db.session.add(new_post)
    db.session.commit()

    return jsonify({'message' : "Post created!"})

@main_blueprint.route('/<post_id>/like', methods=['POST'])
@token_required
def like_action(current_user, post_id):
    post = Post.query.filter_by(id=post_id).first()
    print(post)
    if post:
        if not post.is_liked(current_user.id):
            User.query.filter_by(id=current_user.id).first().like_post(post_id)
        else:
            User.query.filter_by(id=current_user.id).first().unlike_post(post_id)
        db.session.commit()
        return jsonify({'message' : "Post liked!"})

