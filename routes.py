from flask import Blueprint, request, jsonify, make_response
from functools import wraps
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import uuid

from extensions import db
from settings import SECRET_KEY
from models import User, Post

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

        return make_response(jsonify({'token': token}), 201)

    return make_response(
        'Could not verify',
        403,
        {'WWW-Authenticate': 'Basic realm ="Wrong Password !!"'}
    )

@net.route('/sign_up', methods=['POST'])
def signup():
    data = request.form

    name, email = data.get('name'), data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()

    if not user:
        user = User(
            public_id=str(uuid.uuid4()),
            name=name,
            email=email,
            password=generate_password_hash(password)
        )
        db.session.add(user)
        db.session.commit()

        token = jwt.encode({
            'public_id': user.public_id,
            'exp': datetime.utcnow() + timedelta(minutes=45)
        }, SECRET_KEY, "HS256")

        return make_response({'token': token}, 201)
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

        return make_response('Post successfully created.', 201)
    else:
        return make_response('User is not found.', 202)
