from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import jwt
import uuid

from extensions import db
from settings import SECRET_KEY
from models import User, Post, Like

net = Blueprint('net', __name__)


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        if not token:
            return jsonify({'message': 'a valid token is missing'})

        try:
            data = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return jsonify({'message': 'token is invalid'})
        return f(current_user, *args, **kwargs)

    return decorator


def update_user_last_activity(user_id):
    user = User.query.filter_by(id=user_id).first()
    user.datetime_last_activity = datetime.now()
    db.session.commit()


@net.route('/login', methods=['POST'])
def login():
    auth = request.form

    if not auth or not auth.get('email') or not auth.get('password'):
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="Login required !!"'}
        )

    user = User.query.filter_by(email=auth.get('email')).first()

    if not user:
        return make_response(
            'Could not verify',
            401,
            {'WWW-Authenticate': 'Basic realm ="User does not exist !!"'}
        )

    if check_password_hash(user.password, auth.get('password')):
        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, SECRET_KEY, "HS256")

        user.datetime_last_login = datetime.now()
        user.datetime_last_activity = datetime.now()
        db.session.commit()

        return make_response(jsonify({'token': token}), 201)

    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )


@net.route('/sign_up', methods=['POST'])
def signup():
    data = request.form
    name, email, password = data.get('name'), data.get('email'), data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password),
            datetime_last_login=datetime.now(),
            datetime_last_activity=datetime.now()
        )
        db.session.add(user)
        db.session.commit()

        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, SECRET_KEY, "HS256")

        return make_response(jsonify({'token': token}), 201)
    else:
        return make_response('User already exists. Please Log in.', 202)


@net.route('/post/create', methods=['POST'])
@token_required
def create_post(current_user):
    data = request.form
    title, description, user_id = data.get('title'), data.get('description'), data.get('user_id')

    if user_id == current_user.id:
        post = Post(
            title=title,
            description=description,
            user_id=user_id
        )
        db.session.add(post)
        db.session.commit()

        update_user_last_activity(user_id)

        return make_response('Post successfully created.', 201)
    else:
        return make_response('User id isn`t valid.', 403)


@net.route('/post/like', methods=['POST'])
@token_required
def like_post(current_user):
    data = request.form
    user_id, post_id = data.get('user_id'), data.get('post_id')

    if user_id != current_user.id:
        return make_response('User id isn`t valid.', 403)

    update_user_last_activity(user_id)

    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()

    if like:
        return make_response('Like is already present.', 202)

    post = Post.query.filter_by(id=post_id).first()

    if not post:
        return make_response('Post doesn`t exist.', 404)

    like = Like(
        user_id=user_id,
        post_id=post_id,
        created_date=date.today()
    )
    db.session.add(like)
    db.session.commit()

    return make_response('You liked this post!', 201)


@net.route('/post/unlike', methods=['POST'])
@token_required
def unlike_post(current_user):
    data = request.form
    user_id, post_id = data.get('user_id'), data.get('post_id')

    if user_id != current_user.id:
        return make_response('User id isn`t valid.', 403)

    update_user_last_activity(user_id)

    like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()

    if like:
        db.session.delete(like)
        db.session.commit()

        return make_response('You removed like.', 200)

    return make_response('Like isn`t present.', 404)


@net.route('/analytics', methods=['GET'])
@token_required
def analytics_likes(current_user):
    try:
        date_from = datetime.strptime(request.args.get('date_from'), '%Y-%m-%d').date()
        date_to = datetime.strptime(request.args.get('date_to'), '%Y-%m-%d').date()

        likes_between_user_dates = Like.query.filter(Like.created_date.between(date_from, date_to)).all()

        response_dict = {}

        for like in likes_between_user_dates:
            str_like_created_date = str(like.created_date)
            if str_like_created_date in response_dict:
                counter = response_dict.get(str_like_created_date)
                counter += 1
                response_dict[str_like_created_date] = counter
            else:
                response_dict[str_like_created_date] = 1

        return make_response(jsonify(response_dict), 200)

    except ValueError:
        return make_response('Bad request.', 400)
    except TypeError:
        return make_response('Bad request.', 400)


@net.route('/analytics/<user_id>', methods=['GET'])
@token_required
def analytics_user(current_user, user_id):
    user = User.query.filter_by(id=user_id).first()

    if not user:
        return make_response('User does not exist.', 404)

    return make_response(jsonify({'last user activity': user.datetime_last_activity,
                                  'last user login': user.datetime_last_login}), 200)
