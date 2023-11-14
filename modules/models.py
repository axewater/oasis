# modules/models.py
from modules import db
from sqlalchemy import Table
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import uuid
from uuid import uuid4

chatbot_tags = Table('chatbot_tags', db.Model.metadata,
                     db.Column('chatbot_id', db.Integer, db.ForeignKey('chatbots.id')),
                     db.Column('tag_id', db.Integer, db.ForeignKey('tags.id'))
                     )


class Tag(db.Model):
    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    tag_name = db.Column(db.String(64), unique=True, nullable=False)

    def __repr__(self):
        return f"<Tag id={self.id}, tag_name={self.tag_name}>"



class Chatbot(db.Model):
    __tablename__ = 'chatbots'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    systemprompt = db.Column(db.String(256), nullable=False)
    avatarpath = db.Column(db.String(256), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    voicetype = db.Column(db.String(10), nullable=False)
    llm_model = db.Column(db.String(255), default='gpt-3.5-turbo', nullable=False)
    rating = db.Column(db.Integer, default=0)
    tags = relationship('Tag', secondary=chatbot_tags, backref='chatbots')

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'systemprompt': self.systemprompt,
            'avatarpath': self.avatarpath,
            'timestamp': self.timestamp.isoformat(),
            'voicetype': self.voicetype,
            'llm_model': self.llm_model,
            'tags': [tag.tag_name for tag in self.tags],
            'rating': self.rating
        }



class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.String(64), nullable=False)
    state = db.Column(db.Boolean, default=True)
    openai_api_key = db.Column(db.Text, default='default')
    gcloud_api_key = db.Column(db.Text, default='default')
    tts_engine = db.Column(db.Text, default='default')
    speech_enabled = db.Column(db.Boolean, default=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    lastlogin = db.Column(db.DateTime, default=datetime.utcnow)
    quota_messages = db.Column(db.Integer, default=100)
    count_messages = db.Column(db.Integer, default=0)
    fav_tags = db.Column(db.Text, default='')
    fav_bots = db.Column(db.Text, default='')
    user_id = db.Column(db.String(36), unique=True, nullable=False, default=str(uuid4()))
    avatarpath = db.Column(db.String(256), default='avatars_users/default.jpg')
    country = db.Column(db.String(64), nullable=True)
    about = db.Column(db.Text, nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return f"<User id={self.id}, name={self.name}, email={self.email}, speech_enabled={self.speech_enabled}>"



class Message(db.Model):
    __tablename__ = 'messages'

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    owner = db.Column(db.Integer, nullable=False)  # now it's the user id or bot id
    content = db.Column(db.Text, nullable=False)
    role = db.Column(db.String(64), nullable=False)
    thread = db.Column(db.String(128), nullable=False)
    order = db.Column(db.Integer, nullable=False)
    bot_id = db.Column(db.Integer, nullable=False)

    def __init__(self, owner, content, role, bot_id, order, thread=None):
        self.owner = owner
        self.content = content
        self.role = role
        self.bot_id = bot_id
        self.order = order

        # If this is the first message in the thread, generate a new UUID
        if thread is None:
            self.thread = str(uuid.uuid4())
        else:
            self.thread = thread

    def to_dict(self):
        return {
            'id': self.id,
            'timestamp': self.timestamp.strftime('%Y-%m-%d %H:%M:%S'),  # convert datetime to string
            'owner': self.owner,
            'content': self.content,
            'role': self.role,
            'thread': self.thread,
            'order': self.order,
            'bot_id': self.bot_id
        }


class Favorite(db.Model):
    __tablename__ = 'favorites'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    chatbot_id = db.Column(db.Integer, db.ForeignKey('chatbots.id'))

    user = db.relationship('User', backref='favorites')
    chatbot = db.relationship('Chatbot', backref='favorites')

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'chatbot_id': self.chatbot_id
        }


class Whitelist(db.Model):
    __tablename__ = 'whitelist'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)


class Blacklist(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    banned_name = db.Column(db.String, unique=True, nullable=False)

class Highscore(db.Model):
    __tablename__ = 'highscores'

    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(64), nullable=False)
    highscore = db.Column(db.BigInteger, nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.user_id'), nullable=False)

    def __repr__(self):
        return f"<Highscore id={self.id}, game_name={self.game_name}, highscore={self.highscore}, user_id={self.user_id}>"


