from flask import Flask, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError
from wtforms.validators import DataRequired, email
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://fatincake:fatin2cake_@localhost/fatin_db'
app.config['SECRET_KEY'] = "this is very secret"
db = SQLAlchemy(app) 
migrate = Migrate(app, db)

app.app_context().push() 

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Log In")
    

# Home Page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = LoginForm()
    email = None
    if form.validate_on_submit():
        user = Users.query.filter_by(email = form.email.data).first()
        if user is None:
            # Hash Password 
            hashed_password = generate_password_hash(form.password_hash.data) 
            user = Users(email = form.email.data, password_hash = hashed_password)
            db.session.add(user)
            db.session.commit()

        else:
            return render_template('index.html', email = email, form = form)
        
        email = form.email.data
        form.email.data = ''
        form.password_hash.data = ''
        
    return render_template('index.html',email = email, form = form)

# Product Page
@app.route('/products')
def products():
    form = LoginForm()
    email = None
    
    return render_template('all_products.html', form = form, email = email)

# Base HTML
@app.route('/base')
def base():

    return render_template('base.html' )

# Custome Cake
@app.route('/custome', methods=['GET', 'POST'])
def custome():
    form = LoginForm()
    email = None

    return render_template('custome_cake.html', form = form, email = email)

# Cart Page
@app.route('/cart', methods=['GET', 'POST'])
def cart():
    form = LoginForm()
    email = None

    return render_template('cart.html', form = form, email = email)

# Detail Page
@app.route('/details', methods=['GET', 'POST']  )
def details():
    form = LoginForm()
    email = None

    return render_template('detail_product.html', form = form, email = email)

# Account Page
@app.route('/profile', methods=['GET', 'POST']  )
def profile():
    form = LoginForm()
    email = None

    return render_template('profile.html', form = form, email = email)

# Empty Cart (Delete After Ready!)
@app.route('/carts')
def carts():
    form = LoginForm()
    return render_template('cart_empty.html', form = form)


# DATABASE MODEL 
class Users(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(220), nullable=False)

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

if __name__ == "__main__":
    app.run(debug=True)

