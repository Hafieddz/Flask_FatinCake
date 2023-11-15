from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import Nullable, String, false, log
from sqlalchemy.engine import url
from sqlalchemy.sql.expression import Update
from sqlalchemy.sql.functions import user
from sqlalchemy.util import methods_equivalent
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField, TextAreaField
from flask_wtf.file import FileField
from wtforms.validators import DataRequired, EqualTo, Length
from flask_migrate import Migrate, current
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

# User Form (Untuk updata data user)
class UserForm(FlaskForm):
    first_name = StringField("Nama Depan", validators=[DataRequired()])
    last_name = StringField("Nama Belakang")
    phone_number = StringField("No Telepon", validators=[DataRequired()])
    profile_pic = FileField("Profile Picture")
    submit_form = SubmitField("Update Data")

# Update Product Form
class UpdateForm(FlaskForm):
    nama = StringField("Nama Kue", validators=[DataRequired()])
    harga = StringField("Harga Kue", validators=[DataRequired()])
    varian = StringField("Varian", validators=[DataRequired()])
    foto = FileField("Foto Produk", validators=[DataRequired()])
    ukuran = StringField("Ukuran", validators=[DataRequired()])
    detail = TextAreaField("Detail", validators=[DataRequired()])
    submit_update = SubmitField("Update")

# Add Product Form
class AddForm(FlaskForm):
    nama = StringField("Nama Kue", validators=[DataRequired()])
    harga = StringField("Harga Kue", validators=[DataRequired()])
    varian = StringField("Varian", validators=[DataRequired()])
    foto = FileField("Foto Produk")
    ukuran = StringField("Ukuran", validators=[DataRequired()])
    detail = TextAreaField("Detail", validators=[DataRequired()])
    submit_add = SubmitField("Tambah") 

# Update Product Route
@app.route('/updateproduct', methods=['POST', 'GET'])
def update():
    if current_user.role == 'admin':
        update = UpdateForm()

        if update.validate_on_submit():

            return redirect(url_for('admin_product'))
        else:
            flash(f'Data gagal di update!', "danger")
            return redirect(url_for('admin_product'))
            

    
@app.route('/addproduct', methods=['POST'])
def add_product():
    if current_user.role == 'admin':
        add = AddForm()
        if add.validate_on_submit():
            foto_kue = ''
            add = Cake(nama = add.nama.data, 
                        harga = add.harga.data,
                        varian = add.varian.data, 
                        foto = foto_kue,
                        ukuran = add.ukuran.data,
                        detail = add.detail.data)
            # Add User ke database
            db.session.add(add)
            db.session.commit()
            flash(f'Data berhasil di tambahkan!', "success")
            return redirect(url_for('admin_product'))
        else:
            flash(f'Data gagal di tambahkan!', "danger")
            return redirect(url_for('admin_product'))
    else:
        flash(f'Anda tidak bisa masuk di halaman ini!', "danger")
        return redirect(url_for('index'))

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
                    return redirect(url_for('admin_dashboard'))
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
@app.route('/admin_example', methods=['GET', 'POST'])
def base_admin():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'

    if current_user.role == 'admin':
        return render_template("admin/admin_base.html", login = login, register_form = register_form, login_form = login_form)
    else :
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('index'))
    
@login_required
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'

    if current_user.role == 'admin':
        return render_template("admin/admin.html", login = login, register_form = register_form, login_form = login_form)
    else :
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('index'))

@login_required
@app.route('/admin/product', methods=['GET', 'POST'])
def admin_product():
    # Form 
    register_form = RegisterForm()
    login_form = LoginForm()
    update_product = UpdateForm()
    add_product = AddForm()
    
    if current_user.role == 'admin':
        cake_product = Cake.query.order_by(Cake.id_kue)
        format_cake = [{'id_kue': cake.id_kue, 'nama': cake.nama, 'foto': cake.foto,
                         'harga': cake.harga, 'detail': cake.detail[:20], 'varian': cake.varian, 'ukuran': cake.ukuran}
                        for cake in cake_product]
        return render_template("admin/admin_product.html", register_form = register_form, login_form = login_form, update_product = update_product, add_product = add_product, cake_product = cake_product, cakes = format_cake)
    else :
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('index'))

@login_required
@app.route('/admin/order', methods=['GET', 'POST'])
def admin_order():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'

    if current_user.role == 'admin':
        return render_template("admin/admin_order.html", login = login, register_form = register_form, login_form = login_form)
    else :
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('index'))

# End Of Admin Section

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
    user_form = UserForm()

    email = current_user.email
    number = current_user.no_telp
    first = current_user.nama_depan
    last = current_user.nama_belakang
    role = current_user.role

    user_to_update = Users.query(id)

    if request.method == 'POST':
        user_to_update.foto = request.files['profile_pic']
        
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


class Cake(db.Model):
    id_kue = db.Column(db.Integer, primary_key=True)
    nama = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.Text, nullable=False)
    harga = db.Column(db.Integer, nullable=False)
    detail = db.Column(db.Text, nullable=False)
    varian = db.Column(db.String(30), nullable=False)
    ukuran = db.Column(db.String(30), nullable=False)


if __name__ == "__main__":
    app.run(debug=True)

