from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Nullable, String, log
from sqlalchemy.engine import url
from sqlalchemy.sql.functions import user
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_migrate import Migrate
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://fatincake:fatin2cake_@localhost/fatin_db'
app.config['SECRET_KEY'] = "this is very secret"
db = SQLAlchemy(app) 
migrate = Migrate(app, db)

app.app_context().push() 

# Login Manager - Autentikasi Untuk Login 
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'index'

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))


# Register Form 
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message='password harus sama!')])
    confirm_password = PasswordField("Konfirmasi Password", validators=[DataRequired()])
    first_name = StringField("Nama Depan", validators=[DataRequired()])
    last_name = StringField("Nama Belakang")
    phone_number = StringField("No Telepon", validators=[DataRequired()])
    submit_register = SubmitField("Register")

# Login Form 
class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired()])
    submit_login = SubmitField("Log In")
    
# Login Route 
@app.route('/login', methods=['POST'])
def login():
    login_form = LoginForm()
    register_form = RegisterForm()

    if login_form.validate_on_submit():
        user = Users.query.filter_by(email = login_form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, login_form.password_hash.data):
                flash('Login Success!!')
                login_user(user)
                return redirect(url_for('index'))
            else :
                flash('Password is wrong!')
                return redirect(url_for('index'))
        else :
            flash('Login Failed!!')
            return redirect(url_for('index'))
    else:
        flash("Oopss!!")
        return redirect(url_for('index'))

# Register Route
@app.route('/register', methods=['POST'])
def register():
    register_form = RegisterForm()
    login_form = LoginForm()

    if register_form.validate_on_submit():
        # Cek apakah ada email yang sama
        is_email = Users.query.filter_by(email = register_form.email.data).first()
        if is_email is None:
            # Hash Password 
            hashed_password = generate_password_hash(register_form.password_hash.data) 
            is_email = Users(email = register_form.email.data, 
                             password_hash = hashed_password, 
                             nama_depan = register_form.first_name.data, 
                             nama_belakang = register_form.last_name.data, 
                             no_telp = register_form.phone_number.data)
            # Add User ke database
            db.session.add(is_email)
            db.session.commit()
            flash('User Registered!')
            return redirect(url_for('index'))
        else:
            flash('we cant register ur email')
            return redirect(url_for('index'))
    else:
        flash('oops!!')
        return redirect(url_for('index'))
        

# Home Page / Index
@app.route('/', methods=['GET', 'POST'])
def index():
    register_form = RegisterForm()
    login_form = LoginForm()
    email = None

    if current_user.is_authenticated:
        flash("Halo Teman!")
        email = 'Yes'
    else:
        flash("Akun Belum Login, Silahkan Login Terlebih Dahulu!")

    return render_template("index.html", email = email, register_form = register_form, login_form = login_form)
        
# Product Page
@app.route('/products')
def products():
    register_form = RegisterForm()
    login_form = LoginForm()

    if current_user.is_authenticated:
        flash("Halo Teman!")
        email = 'Yes'
    else:
         flash("Akun Belum Login, Silahkan Login Terlebih Dahulu!")

    return render_template("all_products.html", register_form = register_form, login_form = login_form)
# Base HTML
@app.route('/base')
def base():
    register_form = RegisterForm()
    login_form = LoginForm()

    if current_user.is_authenticated:
        flash("Halo Teman!")
        email = 'Yes'
    else:
        flash("Akun Belum Login, Silahkan Login Terlebih Dahulu!")

    return render_template("index.html", email = email, register_form = register_form, login_form = login_form)
        
# Custome Cake
@app.route('/custome', methods=['GET', 'POST'])
def custome():
    register_form = RegisterForm()
    login_form = LoginForm()

    if current_user.is_authenticated:
        flash("Halo Teman!")
        email = 'Yes'
        return render_template("custome_cake.html", email = email, register_form = register_form, login_form = login_form)
    else:
        flash("Akun Belum Login, Silahkan Login Terlebih Dahulu!")
        return render_template("custome_cake.html", register_form = register_form, login_form = login_form)
        

# Cart Page
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    register_form = RegisterForm()
    login_form = LoginForm()

    return render_template('cart.html')
        

# Detail Page
@app.route('/details', methods=['GET', 'POST']  )
def details():
    register_form = RegisterForm()
    login_form = LoginForm()

    if current_user.is_authenticated:
        flash("Halo Teman!")
        email = 'Yes'
        return render_template("detail_product.html", email = email, register_form = register_form, login_form = login_form)
    else:
        flash("Akun Belum Login, Silahkan Login Terlebih Dahulu!")
        return render_template("detail_product.html", register_form = register_form, login_form = login_form)
        

# Account Page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():

    return render_template('profile.html')


# Logout 
@app.route('/logout')
def logout():
    logout_user()
    login_form = LoginForm()
    register_form = RegisterForm()
    flash("Berhasil Logout")

    return redirect(url_for('index', register_form = register_form, login_form = login_form ))

# Empty Cart (Delete After Ready!)
@app.route('/carts')
def carts():
    form = LoginForm()
    return render_template('cart_empty.html', form = form)


# DATABASE MODEL 
class Users(db.Model, UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.String(220), nullable=False)
    nama_depan = db.Column(db.String(30), nullable=False)
    nama_belakang = db.Column(db.String(30))
    no_telp = db.Column(db.String(20), nullable=False)

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

