from flask_sqlalchemy import SQLAlchemy

from flask_login import UserMixin
from sqlalchemy.sql import func

# init 으로부터 옮김
db = SQLAlchemy()
DB_NAME = "blog_db"


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)  # id : 유일 키, Integer
    email = db.Column(db.String(150), unique=True)  # email : 같은 이메일을 가지고 있는 유저가 없도록 함, String
    username = db.Column(db.String(150), unique=True)  # username : 같은 이름을 가지고 있는 유저가 없도록 함, String
    password = db.Column(db.String(150))  # password : 비밀번호, String
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())  # 생성일자, 기본적으로 현재가 저장되도록 함
    is_staff = db.Column(db.Boolean(), default=False)  # 스태프 권한이 있는 유저인지 아닌지를 판별하는 불리언 필드
    posts = db.relationship("Post", backref='user', passive_deletes=True)
    comments = db.relationship("Comment", backref="user", passive_deletes=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}(username={self.username})>'


# User 클래스를 반환하는 함수 정의
def get_user_model():
    return User


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id : 유일 키, Integer
    name = db.Column(db.String(150), unique=True)
    # 이 카테고리가 가지고 있는 post 들
    posts = db.relationship("Post", backref='category', passive_deletes=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}(name={self.name})>'


# Category 클래스를 반환하는 함수 정의
def get_category_model():
    return Category


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id : 유일 키, Integer
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())  # 생성일자, 기본적으로 현재가 저장되도록 함
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                          nullable=False)  # 외래 키, user 테이블의 id를 참조할 것이다!
    category_id = db.Column(db.Integer, db.ForeignKey('category.id', ondelete='CASCADE'),
                            nullable=False)  # 외래 키, categorty 테이블의 id를 참조할 것이다!
    comments = db.relationship("Comment", backref="post", passive_deletes=True)

    def __repr__(self):
        return f'<{self.__class__.__name__}(title={self.title})>'


# Post 클래스를 반환하는 함수 정의
def get_post_model():
    return Post


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # id : 유일 키, Integer
    content = db.Column(db.Text(), nullable=False)
    created_at = db.Column(db.DateTime(timezone=True), default=func.now())  # 생성일자, 기본적으로 현재가 저장되도록 함
    author_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'),
                          nullable=False)  # 외래 키, user 테이블의 id를 참조할 것이다!
    post_id = db.Column(db.Integer, db.ForeignKey('post.id', ondelete='CASCADE'),
                            nullable=False)  # 외래 키, post 테이블의 id를 참조할 것이다!

    def __repr__(self):
        return f'<{self.__class__.__name__}(title={self.content})>'

def get_comment_model():
    return Comment

