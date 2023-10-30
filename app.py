from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Nullable, String, false, log
from sqlalchemy.engine import url
from sqlalchemy.sql.functions import user
from sqlalchemy.util import methods_equivalent
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
    if login_form.validate_on_submit():
        user = Users.query.filter_by(email = login_form.email.data).first()
        if user:
            if check_password_hash(user.password_hash, login_form.password_hash.data):
                flash(f"Login Sukses!!", "success")
                login_user(user)
                if current_user.role == 'admin':
                    flash(f"Login Berhasil", "success")
                    return redirect(url_for('admin'))
                else :
                    flash(f"Login Berhasil", "success")
                    return redirect(url_for('index'))
            else :
                flash(f'Password salah, silahkan coba lagi', "danger")
                return redirect(url_for('index'))
        else :
            flash(f"Email tidak ada, silahkan coba lagi!", "danger")
            return redirect(url_for('index'))
    else:
        flash("Oopss!!")
        return redirect(url_for('index'))

# Register Route
@app.route('/register', methods=['POST'])
def register():
    register_form = RegisterForm()

    if register_form.validate_on_submit():
        # Cek apakah ada email yang sama
        is_email = Users.query.filter_by(email = register_form.email.data).first()
        if is_email is None:
            # Hash Password 
            role = 'user'
            hashed_password = generate_password_hash(register_form.password_hash.data) 
            is_email = Users(email = register_form.email.data, 
                             password_hash = hashed_password, 
                             nama_depan = register_form.first_name.data, 
                             nama_belakang = register_form.last_name.data, 
                             no_telp = register_form.phone_number.data,
                             role = role)
            # Add User ke database
            db.session.add(is_email)
            db.session.commit()
            flash(f'Registrasi Berhasil!', "success")
            return redirect(url_for('index'))
        else:
            flash(f'Email sudah terdaftar!', "danger")
            return redirect(url_for('index'))
    else:
        flash('oops!!', "danger")
        return redirect(url_for('index'))
        
# Home Page / Index
@app.route('/', methods=['GET', 'POST'])
def index():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'
    
    return render_template("index.html", login = login, register_form = register_form, login_form = login_form)
        
# Admin Page
@login_required
@app.route('/admin', methods=['GET', 'POST'])
def admin():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'

    return render_template("admin.html", login = login, register_form = register_form, login_form = login_form)


# Product Page
@app.route('/products')
def products():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'
    else:
         flash(f"Akun Belum Login, Silahkan Login Terlebih Dahulu!", "error")

    return render_template("all_products.html", login = login, register_form = register_form, login_form = login_form)
# Base HTML
@app.route('/base')
def base():

    return render_template("base.html")
        
# Custome Cake
@app.route('/custome', methods=['GET', 'POST'])
def custome():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'
        return render_template("custome_cake.html", login = login, register_form = register_form, login_form = login_form)
    else:
        flash(f"Akun Belum Login, Silahkan Login Terlebih Dahulu!", "danger")
        return render_template("custome_cake.html", register_form = register_form, login_form = login_form)
        

# Cart Page
@app.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = 'Yes'

    return render_template('cart.html', login = login, register_form = register_form, login_form = login_form)
        

# Detail Page
@app.route('/details', methods=['GET', 'POST']  )
def details():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'
        return render_template("detail_product.html", login = login, register_form = register_form, login_form = login_form)
    else:
        flash(f"Akun Belum Login, Silahkan Login Terlebih Dahulu!", "danger")
        return render_template("detail_product.html", register_form = register_form, login_form = login_form)
        

# Account Page
@app.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    login = 'Yes'
    login_form = LoginForm()
    register_form = RegisterForm()

    email = current_user.email
    number = current_user.no_telp
    first = current_user.nama_depan
    last = current_user.nama_belakang
    role = current_user.role

    if current_user.role == '':
        role = 'User'
        
    return render_template('profile.html', register_form = register_form, login_form = login_form, email = email, number = number, first= first, last = last, role = role, login = login)

# Logout 
@app.route('/logout')
def logout():
    logout_user()

    flash("Berhasil logout", "success")

    return redirect(url_for('index')) 

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
    role = db.Column(db.String(20),server_default = 'user' )

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

