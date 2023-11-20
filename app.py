from flask import Flask, redirect, render_template, request, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Nullable, String, false, log
from sqlalchemy.engine import url
from sqlalchemy.sql.expression import Update
from sqlalchemy.sql.functions import user
from sqlalchemy.util import methods_equivalent
from flask_migrate import Migrate, current
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, logout_user, LoginManager, login_required, current_user
from werkzeug.utils import secure_filename
import uuid as uuid
import os

from forms import *

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://fatincake:fatin2cake_@localhost/fatin_db'
app.config['SECRET_KEY'] = "this is very secret"

# Upload Folder Untuk User (Foto Profile)
UPLOAD_FOLDER_1 = 'static/img/profile'
app.config['UPLOAD_FOLDER_1'] = UPLOAD_FOLDER_1

# Upload Folder Untuk Produk (Foto Produk)
UPLOAD_FOLDER_2 = 'static/img/foto_produk'
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2

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

# Update Product Route
@app.route('/update_product/<int:id_kue>', methods=['POST', 'GET'])
def update(id_kue):
    if current_user.role == 'admin':
        update_form = UpdateForm()
        product_to_update = Cake.query.get_or_404(id_kue)
        if request.method == 'POST':
            product_to_update.nama = request.form['nama'] 
            product_to_update.harga = request.form['harga'] 
            product_to_update.varian = request.form['varian'] 
            product_to_update.ukuran = request.form['ukuran'] 
            product_to_update.detail = request.form['detail'] 
            product_to_update.foto = request.files['foto']

            pic_filename = secure_filename(product_to_update.foto.filename)
            saver = request.files['foto']
            product_to_update.foto = pic_filename

            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER_2'], pic_filename))
                flash(f'Produk berhasil di update!', "success")
                return redirect(url_for('admin_product'))
            
            except:
                flash(f'Data gagal di update!', "danger")
                return redirect(url_for('admin_product'))
        else:
            return redirect(url_for('admin_product'))
    else:
        flash(f'Anda tidak bisa masuk ke halaman ini!', "error")
        return redirect(url_for('index'))
        

    
# Delete Product Route
@app.route('/delete_product/<int:id_kue>', methods=['POST', 'GET'])
def delete(id_kue):
    if current_user.role == 'admin':
        product_to_delete = Cake.query.get_or_404(id_kue)
        try :
            db.session.delete(product_to_delete)
            db.session.commit()
            flash(f'Produk berhasil di hapus!', "success")
            return redirect(url_for('admin_product'))
    
        except:
            flash(f'Data gagal di hapus!', "danger")
            return redirect(url_for('admin_product'))
    else :
        flash(f'Anda tidak bisa masuk di halaman ini!', "danger")
        return redirect(url_for('index'))

# Tambah Produk
@app.route('/addproduct', methods=['POST'])
def add_product():
    if current_user.role == 'admin':
        add = AddForm()
        if add.validate_on_submit():
            foto_kue = add.foto.data
            pic_filename = secure_filename(foto_kue.filename)
            saver = add.foto.data
            foto_kue = pic_filename

            add = Cake(nama = add.nama.data, 
                        harga = add.harga.data,
                        varian = add.varian.data, 
                        foto = foto_kue,
                        ukuran = add.ukuran.data,
                        detail = add.detail.data)
            # Add User ke database
            db.session.add(add)
            db.session.commit()
            saver.save(os.path.join(app.config['UPLOAD_FOLDER_2'], pic_filename))
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
        # Cek apakah ada email yang sama``
        is_email = Users.query.filter_by(email = register_form.email.data).first()
        if is_email is None:
            # Hash Password 
            role = 'user'
            foto_profile = 'kanan_profile.jpeg'
            hashed_password = generate_password_hash(register_form.password_hash.data) 
            is_email = Users(email = register_form.email.data, 
                             password_hash = hashed_password, 
                             nama_depan = register_form.first_name.data, 
                             nama_belakang = register_form.last_name.data, 
                             no_telp = register_form.phone_number.data,
                             role = role, foto_profile = foto_profile)
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
                         'harga': cake.harga, 'detail': cake.detail[:50], 'varian': cake.varian, 'ukuran': cake.ukuran}
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

    cake_product = Cake.query.order_by(Cake.id_kue)
    format_cake = [{'id_kue': cake.id_kue, 'nama': cake.nama, 'foto': cake.foto,
                    'harga': cake.harga, 'detail': cake.detail[:50], 'varian': cake.varian, 'ukuran': cake.ukuran}
                    for cake in cake_product]

    return render_template("all_products.html", login = login, register_form = register_form, login_form = login_form, cakes = format_cake, cake_product = cake_product)

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
    user_form = UserForm()
    id = current_user.id
    user_profile = Users.query.get_or_404(id)
        
    return render_template('profile.html', user_profile = user_profile, user_form = user_form, login = login)

@app.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user_form = UserForm()
    id = current_user.id
    user_profile = Users.query.get_or_404(id)

    if request.method == 'POST':
            user_profile.nama_depan = request.form['first_name'] 
            user_profile.nama_belakang = request.form['last_name'] 
            user_profile.no_telp = request.form['phone_number'] 
            user_profile.foto_profile = request.files['profile_pic']

            # Ambil nama gambar
            pic_filename = secure_filename(user_profile.foto_profile.filename)
            # Set UUID (Buat nama gambar jadi unique)
            pic_name = str(uuid.uuid1()) + "_" + pic_filename
            #Save gambar
            saver = request.files['profile_pic'] 
            #Save nama file ke database
            user_profile.foto_profile = pic_name
            try:
                db.session.commit()
                saver.save(os.path.join(app.config['UPLOAD_FOLDER_1'], pic_name))
                flash(f'Data berhasil di update!', "success")
                return redirect(url_for('profile'))
            
            except:
                flash(f'Data gagal di update!', "danger")
                return redirect(url_for('profile'))
        
    return render_template('profile.html', user_profile = user_profile, user_form = user_form)

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
    role = db.Column(db.String(20),server_default = 'user')
    foto_profile = db.Column(db.Text, nullable=False)

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

    def __repr__(self):
        return '<nama %r>' %self.nama 


if __name__ == "__main__":
    app.run(debug=True)

