from grosto import app,db,login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(db.Model,UserMixin):
    __tablename__="user"
    id=db.Column(db.Integer,primary_key=True)
    username=db.Column(db.String(20),unique=True,nullable=False)
    email=db.Column(db.String(120),unique=True,nullable=False)
    password=db.Column(db.String(60),nullable=False)
    cart = db.Column(db.String,nullable=True)



class Category(db.Model):
    __tablename__="categories"
    c_id=db.Column(db.Integer,primary_key=True)
    c_name=db.Column(db.String,unique=True,nullable=False)

class Product(db.Model):
    __tablename__="product"
    p_id=db.Column(db.Integer,primary_key=True)
    p_name=db.Column(db.String,unique=True,nullable=False)
    category = db.Column(db.String, nullable=False)
    price=db.Column(db.Integer,nullable=False)
    stock=db.Column(db.Integer,nullable=False)
    expiry_date=db.Column(db.DateTime,nullable=False)






with app.app_context():
    db.create_all()
