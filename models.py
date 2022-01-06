from extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(70), unique=True)
    password = db.Column(db.String(80))
    date_last_login = db.Column(db.Date)
    date_last_activity = db.Column(db.Date)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class Like(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)