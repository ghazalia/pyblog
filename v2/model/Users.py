from commons import db
import datetime


class BlogPostModel(db.Model):
    """
    Blogpost Model
    """
    __tablename__ = 'blogposts'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    contents = db.Column(db.Text, nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified_at = db.Column(
        db.DateTime, default=datetime.datetime.utcnow(),
        onupdate=datetime.datetime.utcnow())


class UserModel(db.Model):
    '''
    User Model
    '''
    # table name
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow())
    modified_at = db.Column(db.DateTime, default=datetime.datetime.utcnow(
    ), onupdate=datetime.datetime.utcnow())
    blogposts = db.relationship(
        'BlogPostModel', backref='users', lazy='dynamic')
