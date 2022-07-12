from pkg_resources import Requirement

# from website.views import membership
from . import db
from flask_login import UserMixin
from sqlalchemy.sql import func

UserCourse = db.Table('user_course', db.Column('id', db.Integer, primary_key=True), db.Column(
    'user_id', db.Integer, db.ForeignKey('user.id')), db.Column('course_id', db.Integer, db.ForeignKey('course.id')))
UserCompetition = db.Table('user_competition', db.Column('id', db.Integer, primary_key=True), db.Column(
    'user_id', db.Integer, db.ForeignKey('user.id')), db.Column('competition_id', db.Integer, db.ForeignKey('competition.id')))


class Note(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f"Note('{self.data}', '{self.date}')"

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    name = db.Column(db.String(100))
    email = db.Column(db.String(150), unique=True)
    contactNumber = db.Column(db.String(20))
    address = db.Column(db.String(100))
    password = db.Column(db.String(150))
    courses = db.relationship('Course', secondary=UserCourse, backref='user',lazy='select')
    posts = db.relationship('Post', backref='user')
    payments = db.relationship('Payment', backref='user')
    competitions = db.relationship(
        'Competition', secondary=UserCompetition, backref='user', lazy='select')
    tickets = db.relationship('Ticket', backref='user')
    membershipstatus=db.Column(db.String(20))
    def __repr__(self) -> str:
        return f"User('{self.name}', '{self.email}')"


class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(20))
    title = db.Column(db.String(100))
    content = db.Column(db.String(10000))
    date_posted = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.Float)
    competitionId = db.Column(db.Integer, db.ForeignKey('competition.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    def __repr__(self) -> str:
        return f"Ticket('{self.price}', '{self.competitionId}', '{self.user_id}')"


class Competition(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100))
    format = db.Column(db.String(100))
    date = db.Column(db.DateTime(timezone=True), default=func.now())

    tickets = db.relationship('Ticket', backref='competition')
    # participants = db.relationship(
        # 'User', secondary=UserCompetition, backref='competition', lazy='select')

    def __repr__(self):
        return f"Competition('{self.name}', '{self.date}')"


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    date = db.Column(db.String(100))
    duration = db.Column(db.String(100))
    requirements = db.Column(db.String(200))
    courseCoordinatorId = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    # participants = db.relationship(
        # 'User', secondary=UserCourse, backref='course', lazy='select')
    price = db.Column(db.Float)

    def __repr__(self):
        return f"Courses('{self.name}', '{self.date}', '{self.duration}', '{self.requirements}')"


class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True,
                   nullable=False, autoincrement=True)
    amount = db.Column(db.Float)
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type = db.Column(db.String(100))
    def __repr__(self) -> str:
        return f"Payment('{self.amount}', '{self.date}', '{self.user_id}', '{self.type}')"
    # to do add payment type
