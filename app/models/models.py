from flask_login import UserMixin
from sqlalchemy import Nullable

from ..extension import db, generate_password_hash, check_password_hash

# DATABASE MODEL 
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(220), nullable=False)
    nama_depan = db.Column(db.String(30), nullable=False)
    nama_belakang = db.Column(db.String(30))
    no_telp = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20),server_default = 'user')
    foto_profile = db.Column(db.Text, nullable=False)
    cart = db.relationship('Cart', backref='users_carts')
    orders = db.relationship('Orders', backref='users_orders')


    @property
    def password(self):
        raise AttributeError('password is not readable attribute !')
    
    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password) 

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<Email %r>' %self.email 


class Cake(db.Model):
    id_kue = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.Text, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.Text, nullable=False)
    varian = db.Column(db.String(30), nullable=False)
    ukuran = db.Column(db.String(30), nullable=False)
    cart_details = db.relationship('CartDetails', backref='cake_carts')
    order_details = db.relationship('OrderDetails', backref='cake_orders')

    def __repr__(self):
        return '<nama %r>' %self.nama 
    
class Cart(db.Model):
    id_cart = db.Column(db.Integer,primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    total_price = db.Column(db.Integer, nullable=False)
    cart_details = db.relationship('CartDetails', backref='cart')

class CartDetails(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    id_cart = db.Column(db.Integer, db.ForeignKey('cart.id_cart'), nullable= False)
    id_kue = db.Column(db.Integer, db.ForeignKey('cake.id_kue'), nullable= False)
    quantity = db.Column(db.Integer, nullable = False)
    sub_total = db.Column(db.Float, nullable = False)
    message = db.Column(db.Text, nullable = False) 
     
class Orders(db.Model):
    id_orders = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable= False)
    nama = db.Column(db.String(100), nullable=False)
    pickup_date = db.Column(db.String(20), nullable=False)
    picktup_time = db.Column(db.String(20), nullable=False)
    total_price = db.Column(db.Integer, nullable=False)
    order_status = db.Column(db.String(40), nullable=False)
    payment_methods = db.Column(db.String(30), nullable=False)
    order_details = db.relationship('OrderDetails', backref='orderdetails')
    
class OrderDetails(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    id_orders = db.Column(db.Integer, db.ForeignKey('orders.id_orders'), nullable = False)
    id_kue = db.Column(db.Integer, db.ForeignKey('cake.id_kue'), nullable= False)
    quantity = db.Column(db.Integer, nullable = False)
    sub_total = db.Column(db.Float, nullable = False)
    message = db.Column(db.Text, nullable = False)   