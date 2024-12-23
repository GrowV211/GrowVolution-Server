from . import APP
from flask import url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text
from flask_bcrypt import Bcrypt
from datetime import datetime, timedelta
from pathlib import Path
from markupsafe import Markup
import secrets
import re
import os

DB = SQLAlchemy(APP)
CRYPT = Bcrypt(APP)

with APP.app_context():
    with DB.engine.connect() as conn:
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
        conn.execute(text("TRUNCATE TABLE ClientSession"))
        conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))

PROOF_PATH = Path(APP.static_folder) / 'proof'

CHATS = DB.Table('chats', DB.Column('userID', DB.Integer, DB.ForeignKey('account.id'), primary_key=True),
                 DB.Column('chatID', DB.Integer, DB.ForeignKey('chat.id'), primary_key=True))

RELATIONS = DB.Table('relations', DB.Column('user1_ID', DB.Integer, DB.ForeignKey('account.id'), primary_key=True),
                     DB.Column('user2_ID', DB.Integer, DB.ForeignKey('account.id'), primary_key=True))

TEAMS = DB.Table('teams', DB.Column('teamID', DB.Integer, DB.ForeignKey('team.id'), primary_key=True),
                 DB.Column('userID', DB.Integer, DB.ForeignKey('account.id'), primary_key=True))


def commit():
    DB.session.commit()


def add_model(model):
    DB.session.add(model)
    commit()


def delete_model(model):
    DB.session.delete(model)
    commit()


def get_date(model):
    now = datetime.now()
    date = model.timestamp

    if date.date() == now.date():
        return "Heute"
    elif date.date() == (now - timedelta(days=1)).date():
        return "Gestern"
    else:
        return date.strftime("%d.%m.%Y")


def get_time(model):
    hour = str(int(model.timestamp.strftime("%H")) + 1)
    return model.timestamp.strftime(f"{hour}:%M")


def whitespace_chars_html(string):
    string = string.replace('\n', '<br>')
    return Markup(re.sub(r' {2,}', lambda match: match.group(0).replace(' ', '&nbsp;'), string))


def get_challenges(**kwargs):
    return Content.query.filter_by(category='🏅'.encode('unicode_escape').decode('ascii'), **kwargs).all()


def mod_messages():
    if get_challenges(managed=False):
        return True

    elif Proof.query.all():
        return True

    return False


def admin_messages():
    return False


class User(DB.Model):
    __tablename__ = 'account'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)

    first = DB.Column(DB.String(30), nullable=False)
    last = DB.Column(DB.String(30), nullable=False)
    username = DB.Column(DB.String(35), nullable=False, unique=True)
    email = DB.Column(DB.String(60), nullable=False, unique=True)
    psw_crypt = DB.Column(DB.String(256), nullable=False)

    info = DB.Column(DB.String(500), nullable=True)
    img = DB.Column(DB.String(39), nullable=True)
    alt_bg = DB.Column(DB.String(7), nullable=False)
    username_lock = DB.Column(DB.Integer, default=0)
    role = DB.Column(DB.String(5), nullable=False, default='USER')
    score = DB.Column(DB.Integer, nullable=False, default=0)

    chats = DB.relationship('Chat', secondary=CHATS, back_populates='participants')
    sent = DB.relationship('Message', back_populates='sender')

    requests_in = DB.relationship('Request', foreign_keys='Request.receiverID', back_populates='receiver')
    requests_out = DB.relationship('Request', foreign_keys='Request.requestorID', back_populates='requestor')

    relators = DB.relationship('User', secondary=RELATIONS,
                               primaryjoin=id == RELATIONS.c.user1_ID,
                               secondaryjoin=id == RELATIONS.c.user2_ID,
                               back_populates='relators',
                               foreign_keys=[RELATIONS.c.user1_ID, RELATIONS.c.user2_ID])

    posts = DB.relationship('Content', back_populates='creator')
    comments = DB.relationship('Comment', back_populates='writer')

    links = DB.relationship('Link', back_populates='user')

    challenges = DB.relationship('Challenge', back_populates='user')

    liked = DB.relationship('Like', back_populates='user')

    progress = DB.relationship('Progress', back_populates='user')
    journal = DB.relationship('Journal', back_populates='user')

    teams = DB.relationship('Team', secondary=TEAMS, back_populates='members')
    invitations = DB.relationship('Invitation', back_populates='user')

    sessions = DB.relationship('Session', back_populates='user')

    def __init__(self, first, last, username, email, password, alt_bg):
        self.first = first
        self.last = last
        self.username = username
        self.email = email

        self.psw_crypt = CRYPT.generate_password_hash(password).decode()

        self.img = None
        self.alt_bg = alt_bg

    def set_username(self, username):
        self.username = username
        self.username_lock = 30
        commit()

    def set_email(self, email):
        self.email = email
        commit()

    def set_psw_crypt(self, password):
        self.psw_crypt = CRYPT.generate_password_hash(password).decode()
        commit()

    def set_info(self, info):
        self.info = info
        commit()

    def set_img(self, img):
        self.img = img
        commit()

    def change_role(self, role):
        self.role = role
        commit()

    def username_edit_locked(self):
        if self.username_lock > 0:
            return 1

        return 0

    def update_username_lock(self):
        if not self.username_edit_locked():
            return

        self.username_lock -= 1
        commit()

    def username_lock_time(self):
        return self.username_lock

    def check_psw(self, password):
        return CRYPT.check_password_hash(self.psw_crypt, password)

    def add_relator(self, relator):
        if not relator in self.relators:
            self.relators.append(relator)
            commit()

    def remove_relator(self, relator):
        if relator in self.relators:
            self.relators.remove(relator)
            commit()

    def name(self):
        return f"{self.first} {self.last}"

    def get_unread_messages(self):
        i = 0
        for chat in self.chats:
            for participant in chat.participants:
                if participant is not self:
                    for msg in participant.sent:
                        if not msg.is_read:
                            i += 1

        return i if i > 0 else None

    def get_unread_chat_messages(self, chat):
        i = 0
        for participant in chat.participants:
            if participant is not self:
                for msg in participant.sent:
                    if not msg.is_read:
                        i += 1

        return i if i > 0 else None

    def get_unread_requests(self):
        i = 0
        for request in self.requests_in:
            if not request.is_read:
                i += 1

        return i if i > 0 else None

    def is_mod(self):
        if self.role == 'MOD':
            return True

        return False

    def is_admin(self):
        if self.role == 'ADMIN':
            return True

        return False

    def has_liked(self, post=None, comment=None):
        if post:
            return Like.query.filter_by(userID=self.id, contentID=post).first() is not None
        else:
            return Like.query.filter_by(userID=self.id, commentID=comment).first() is not None

    def update_score(self, value):
        self.score += value

        if self.score < 0:
            self.score = 0

        commit()

    def _latest_journal_entry(self):
        return Journal.query.filter_by(userID=self.id).order_by(Journal.timestamp.desc()).first()

    def journal_time(self):
        if not self.progress:
            return None

        progress = self.progress[0]
        time = progress.journal_time
        now = datetime.now()
        hour = now.hour + 1

        journal = False

        if time == "evening" and hour >= 18:
            journal = True

        elif time == "aftnoon" and 12 <= hour < 18:
            journal = True

        elif time == "morning" and hour < 12:
            journal = True

        if journal:
            latest = self._latest_journal_entry()

            if latest and latest.timestamp.date() == now.date():
                journal = False

        return journal

    def has_done_journal(self, date):
        latest = self._latest_journal_entry()
        if latest and latest.timestamp.date() == date:
            return True

        elif not self.progress:
            return True

        return False

    def flash_managed_challenges(self):
        for challenge in self.challenges:
            if challenge.proved:
                flash(Markup(f"Dein Beweis für die Aufgabe <b>{challenge.content.headline}</b> wurde bestätigt."),
                      'success')
                delete_model(challenge)

            elif challenge.managed:
                flash(Markup(f"Dein Beweis für die Aufgabe <b>{challenge.content.headline}</b> konnte nicht bestätigt werden."),
                      'warning')
                delete_model(challenge)


class Chat(DB.Model):
    __tablename__ = 'chat'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    salt = DB.Column(DB.LargeBinary(16), nullable=False)

    participants = DB.relationship('User', secondary=CHATS, back_populates='chats')
    messages = DB.relationship('Message', back_populates='chat', cascade='all, delete-orphan')

    sessions = DB.relationship('Session', back_populates='chat')

    def __init__(self):
        self.salt = os.urandom(16)

    def _get_last_message_data(self, user):
        if self.messages:
            last = self.messages[-1]
            by_user = 'ich' if last.sender == user else last.sender.first
            if len(last.content) > 25:
                last = last.content[:25] + '...'
            else:
                last = last.content
        else:
            last = None
            by_user = None

        return {
            'message': last,
            'by_user': by_user
        } if last else None

    def get_last_message_text(self, user):
        data = self._get_last_message_data(user)

        if data:
            return f"{data['by_user']}: {data['message']}"

        return None


class Message(DB.Model):
    __tablename__ = 'message'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    senderID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)
    chatID = DB.Column(DB.Integer, DB.ForeignKey('chat.id'), nullable=False)

    content = DB.Column(DB.String, nullable=False)
    timestamp = DB.Column(DB.TIMESTAMP, server_default=DB.func.current_timestamp(), nullable=False)
    is_read = DB.Column(DB.Boolean, nullable=False, default=False)

    chat = DB.relationship('Chat', foreign_keys=[chatID], back_populates='messages')
    sender = DB.relationship('User', foreign_keys=[senderID], back_populates='sent')

    def __init__(self, sender, content, chat):
        self.senderID = sender
        self.content = content
        self.chatID = chat

    def get_content(self):
        return whitespace_chars_html(self.content)

    def set_read(self):
        self.is_read = True
        commit()

    def date(self):
        return get_date(self)

    def time(self):
        return get_time(self)


class Request(DB.Model):
    __tablename__ = 'request'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    requestorID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)
    receiverID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)
    is_read = DB.Column(DB.Boolean, nullable=False, default=False)

    receiver = DB.relationship('User', foreign_keys=[receiverID], back_populates='requests_out')
    requestor = DB.relationship('User', foreign_keys=[requestorID], back_populates='requests_in')

    def __init__(self, requestor, receiver):
        self.requestorID = requestor
        self.receiverID = receiver

    def set_read(self):
        self.is_read = True
        commit()


class Content(DB.Model):
    __tablename__ = 'content'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    creatorID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)

    headline = DB.Column(DB.String(128), nullable=False)
    body = DB.Column(DB.String(10240), nullable=False)
    category = DB.Column(DB.String(12), nullable=False)
    likes = DB.Column(DB.Integer, nullable=False, default=0)
    timestamp = DB.Column(DB.TIMESTAMP, server_default=DB.func.current_timestamp(), nullable=False)
    edited = DB.Column(DB.Boolean, nullable=False, default=False)
    managed = DB.Column(DB.Boolean)
    provable = DB.Column(DB.Boolean)

    creator = DB.relationship('User', foreign_keys=[creatorID], back_populates='posts')
    comments = DB.relationship('Comment', back_populates='post')

    challenges = DB.relationship('Challenge', back_populates='content')

    linked_likes = DB.relationship('Like', back_populates='post')

    def __init__(self, creator, headline, body, category):
        self.creatorID = creator
        self.headline = headline
        self.body = body
        self.category = category.encode('unicode_escape').decode('ascii')

        if self.is_challenge():
            self.managed = False
            self.provable = False

    def get_content(self):
        return whitespace_chars_html(self.body)

    def get_category(self):
        return self.category.encode('utf-8').decode('unicode_escape')

    def get_category_text(self):
        category = self.get_category()

        category_map = {
            '💬': '💬 - Allgemeines',
            '👫': '👫 - Beziehungen',
            '❤️': '❤️ - Dating',
            '💼': '💼 - Karriere',
            '🌱': '🌱 - Gesundheit',
            '🔮': '🔮 - Spirituelles',
            '🏅': '🏅 - Aufgaben',
            '🌍': '🌍 - Diskussionen'
        }

        return category_map.get(category, f"{category} - Unbekannt")

    def like(self):
        self.likes += 1
        commit()

    def unlike(self):
        self.likes -= 1
        commit()

    def is_challenge(self):
        return True if self.get_category() == '🏅' else False

    def accepted(self, user):
        if not user:
            return None
        return Challenge.query.filter_by(userID=user.id, contentID=self.id).first() is not None

    def set_provable(self):
        self.provable = True
        commit()

    def set_managed(self):
        self.managed = True
        commit()

    def date(self):
        return get_date(self)

    def time(self):
        return get_time(self)

    def edit(self, headline, content):
        self.headline = headline
        self.body = content
        self.edited = True
        commit()


class Comment(DB.Model):
    __tablename__ = 'comment'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    writerID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)
    contentID = DB.Column(DB.Integer, DB.ForeignKey('content.id'), nullable=False)
    commentID = DB.Column(DB.Integer, DB.ForeignKey('comment.id'))

    content = DB.Column(DB.String(2560), nullable=False)
    likes = DB.Column(DB.Integer, nullable=False, default=0)
    timestamp = DB.Column(DB.TIMESTAMP, server_default=DB.func.current_timestamp(), nullable=False)
    edited = DB.Column(DB.Boolean, nullable=False, default=False)

    writer = DB.relationship('User', foreign_keys=[writerID], back_populates='comments')
    post = DB.relationship('Content', foreign_keys=[contentID], back_populates='comments')

    parent = DB.relationship('Comment', foreign_keys=[commentID], back_populates='answers', remote_side=[id])
    answers = DB.relationship('Comment', foreign_keys=[commentID], back_populates='parent')

    linked_likes = DB.relationship('Like', back_populates='comment')

    def __init__(self, writer, post, content, comment):
        self.writerID = writer
        self.contentID = post
        self.content = content

        if comment:
            self.commentID = comment

    def get_content(self):
        return whitespace_chars_html(self.content)

    def is_reply(self):
        return self.commentID is not None

    def like(self):
        self.likes += 1
        commit()

    def unlike(self):
        self.likes -= 1
        commit()

    def date(self):
        return get_date(self)

    def time(self):
        return get_time(self)

    def edit(self, content):
        self.content = content
        self.edited = True
        commit()


class Link(DB.Model):
    __tablename__ = 'link'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    userID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)

    link = DB.Column(DB.String(256), nullable=False)
    titel = DB.Column(DB.String(128), nullable=False)
    social = DB.Column(DB.String(12))

    user = DB.relationship('User', foreign_keys=[userID], back_populates='links')

    def __init__(self, user, link, titel, social=None):
        self.userID = user
        self.link = link
        self.titel = titel
        self.social = social

    def is_social(self):
        return self.social is not None


class Challenge(DB.Model):
    __tablename__ = 'challenge'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    userID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)
    contentID = DB.Column(DB.Integer, DB.ForeignKey('content.id'), nullable=False)

    done = DB.Column(DB.Boolean, nullable=False, default=False)
    proved = DB.Column(DB.Boolean, nullable=False, default=False)
    managed = DB.Column(DB.Boolean, nullable=False, default=False)

    user = DB.relationship('User', foreign_keys=[userID], back_populates='challenges')
    content = DB.relationship('Content', foreign_keys=[contentID], back_populates='challenges')

    proof = DB.relationship('Proof', back_populates='challenge')

    def __init__(self, user, content):
        self.userID = user
        self.contentID = content

    def finish(self):
        self.done = True
        commit()

    def set_proved(self):
        self.proved = True
        commit()

    def set_managed(self):
        self.managed = True
        commit()


class Proof(DB.Model):
    __tablename__ = 'proof'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    challengeID = DB.Column(DB.Integer, DB.ForeignKey('challenge.id'), nullable=False)

    proof1 = DB.Column(DB.String(45), nullable=False)
    proof2 = DB.Column(DB.String(45))
    proof3 = DB.Column(DB.String(45))
    proof4 = DB.Column(DB.String(45))
    proof5 = DB.Column(DB.String(45))

    challenge = DB.relationship('Challenge', foreign_keys=[challengeID], back_populates='proof')

    def __init__(self, challenge, **kwargs):
        self.challengeID = challenge

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def get_proves(self):
        proves = {}

        for proof_attr in ['proof1', 'proof2', 'proof3', 'proof4', 'proof5']:
            proof_value = getattr(self, proof_attr)
            if proof_value:
                proves[proof_attr] = proof_value

        return proves

    def get_proves_html(self):
        proves = ""

        for key, value in self.get_proves().items():
            proves += f"<li><a href='{url_for('static', filename=f'proof/{value}')}' target='_blank'>{key}</a></li>"

        return Markup(proves)

    def delete_files(self):
        for proof in self.get_proves().values():
            (PROOF_PATH / proof).unlink()


class Like(DB.Model):
    __tablename__ = 'likes'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    userID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)
    contentID = DB.Column(DB.Integer, DB.ForeignKey('content.id'))
    commentID = DB.Column(DB.Integer, DB.ForeignKey('comment.id'))

    user = DB.relationship('User', foreign_keys=[userID], back_populates='liked')
    post = DB.relationship('Content', foreign_keys=[contentID], back_populates='linked_likes')
    comment = DB.relationship('Comment', foreign_keys=[commentID], back_populates='linked_likes')

    def __init__(self, user, content=None, comment=None):
        self.userID = user
        self.contentID = content
        self.commentID = comment


class Progress(DB.Model):
    __tablename__ = 'progress'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    userID = DB.Column(DB.Integer, DB.ForeignKey('account.id', ondelete='CASCADE'), nullable=False)

    goal = DB.Column(DB.Text, nullable=False)
    body_current = DB.Column(DB.Text, nullable=False)
    mental_current = DB.Column(DB.Text, nullable=False)
    relations_current = DB.Column(DB.Text, nullable=False)
    personal_current = DB.Column(DB.Text, nullable=False)
    financial_current = DB.Column(DB.Text, nullable=False)
    career_current = DB.Column(DB.Text, nullable=False)
    spiritual_current = DB.Column(DB.Text, nullable=False)

    body_future = DB.Column(DB.Text, nullable=False)
    mental_future = DB.Column(DB.Text, nullable=False)
    relations_future = DB.Column(DB.Text, nullable=False)
    personal_future = DB.Column(DB.Text, nullable=False)
    financial_future = DB.Column(DB.Text, nullable=False)
    career_future = DB.Column(DB.Text, nullable=False)
    spiritual_future = DB.Column(DB.Text, nullable=False)

    question_1 = DB.Column(DB.String(128), nullable=False)
    question_2 = DB.Column(DB.String(128))
    question_3 = DB.Column(DB.String(128))
    question_4 = DB.Column(DB.String(128))
    question_5 = DB.Column(DB.String(128))

    journal_time = DB.Column(DB.String(7), nullable=False)

    user = DB.relationship('User', back_populates='progress')

    def __init__(self, user, goal, journal_time, **kwargs):
        self.userID = user
        self.goal = goal
        self.journal_time = journal_time

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def active_questions(self):
        questions = {}

        for question_attr in ['question_1', 'question_2', 'question_3', 'question_4', 'question_5']:
            question_value = getattr(self, question_attr)
            if question_value:
                questions[question_attr] = question_value

        return questions


class Journal(DB.Model):
    __tablename__ = 'journal'
    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    userID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)

    answer1 = DB.Column(DB.Text, nullable=False)
    answer2 = DB.Column(DB.Text)
    answer3 = DB.Column(DB.Text)
    answer4 = DB.Column(DB.Text)
    answer5 = DB.Column(DB.Text)

    timestamp = DB.Column(DB.TIMESTAMP, server_default=DB.func.current_timestamp(), nullable=False)

    user = DB.relationship('User', foreign_keys=[userID], back_populates='journal')

    def __init__(self, user, **kwargs):
        self.userID = user

        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)

    def active_answers(self):
        answers = {}

        for answer_attr in ['answer1', 'answer2', 'answer3', 'answer4', 'answer5']:
            answer_value = getattr(self, answer_attr)
            if answer_value:
                answers[answer_attr] = answer_value

        return answers

    def date(self):
        return get_date(self)

    def time(self):
        return get_time(self)


class Team(DB.Model):
    __tablename__ = 'team'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    name = DB.Column(DB.String(50), nullable=False)
    score = DB.Column(DB.Integer, nullable=False, default=0)

    members = DB.relationship('User', secondary=TEAMS, back_populates='teams')
    invitations = DB.relationship('Invitation', back_populates='team')

    def __init__(self, name):
        self.name = name

    def update_score(self, value):
        self.score += value

        if self.score < 0:
            self.score = 0

        commit()


class Invitation(DB.Model):
    __tablename__ = 'invitation'

    id = DB.Column(DB.Integer, primary_key=True, autoincrement=True)
    userID = DB.Column(DB.Integer, DB.ForeignKey('account.id'), nullable=False)
    teamID = DB.Column(DB.Integer, DB.ForeignKey('team.id'), nullable=False)

    user = DB.relationship('User', foreign_keys=[userID], back_populates='invitations')
    team = DB.relationship('Team', foreign_keys=[teamID], back_populates='invitations')

    def __init__(self, user, team):
        self.userID = user
        self.teamID = team


class Session(DB.Model):
    __tablename__ = 'ClientSession'

    id = DB.Column(DB.String(32), primary_key=True)
    sid = DB.Column(DB.String(32))
    tab = DB.Column(DB.String(32))

    userID = DB.Column(DB.Integer, DB.ForeignKey('account.id'))
    chatID = DB.Column(DB.Integer, DB.ForeignKey('chat.id'))

    valid = DB.Column(DB.Boolean, nullable=False, default=True)
    csrf_token = DB.Column(DB.String(32))

    user = DB.relationship('User', foreign_keys=[userID], back_populates='sessions')
    chat = DB.relationship('Chat', foreign_keys=[chatID], back_populates='sessions')

    def __init__(self, uuid):
        self.id = uuid

    def set_socket(self, sid):
        self.sid = sid
        commit()

    def set_tab(self, tab):
        self.tab = tab
        commit()

    def set_user(self, user):
        self.userID = user
        commit()

    def set_chat(self, chat):
        self.chatID = chat
        commit()

    def set_invalid(self):
        self.valid = False
        commit()

    def csrf(self, set_token=True):
        self.csrf_token = secrets.token_hex(32) if set_token else None
        commit()
        if set_token:
            return self.csrf_token
