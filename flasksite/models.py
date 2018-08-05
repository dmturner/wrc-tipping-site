from datetime import datetime
from flasksite import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer,
                   primary_key=True)
    username = db.Column(db.String(20),
                         unique=True,
                         nullable=False)
    email = db.Column(db.String(120),
                      unique=True,
                      nullable=False)
    image_file = db.Column(db.String(20),
                           nullable=False,
                           default='default.jpg')
    password = db.Column(db.String(60),
                         nullable=False)
    posts = db.relationship('Post',
                            backref='author',
                            lazy=True)
    selections = db.relationship('Selection',
                                 backref='user',
                                 lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Selection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    top10_selection_1 = db.Column(db.String(20), nullable=False)
    top10_selection_2 = db.Column(db.String(20), nullable=False)
    top10_selection_3 = db.Column(db.String(20), nullable=False)
    top10_selection_4 = db.Column(db.String(20), nullable=False)
    top10_selection_5 = db.Column(db.String(20), nullable=False)
    top10_selection_6 = db.Column(db.String(20), nullable=False)
    top10_selection_7 = db.Column(db.String(20), nullable=False)
    top10_selection_8 = db.Column(db.String(20), nullable=False)
    top10_selection_9 = db.Column(db.String(20), nullable=False)
    top10_selection_10 = db.Column(db.String(20), nullable=False)
    stage_two_selection = db.Column(db.String(20), nullable=False)
    power_stage_selection = db.Column(db.String(20), nullable=False)

    def __repr__(self):
        return f"Post('{self.id}', '{self.event_id})"


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country_name = db.Column(db.String(30), nullable=False)
    full_name = db.Column(db.String(120), nullable=False)
    year = db.Column(db.String(4), nullable=False)
    start_date_time = db.Column(db.Integer, nullable=False)
    end_date_time = db.Column(db.Integer, nullable=False)
    active = db.Column(db.Boolean, nullable=False)
    result = db.Column(db.Text, nullable=True)

    def __repr__(self):
        return f"Post('{self.id}', '{self.country_name})"
