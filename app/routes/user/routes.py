from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask
from sqlalchemy.exc import IntegrityError
from os import error
import os 
import uuid as uuid
from werkzeug.utils import secure_filename


from ...forms.forms import LoginForm, RegisterForm, UserForm, TestForm
from ...models.models import Users, Cake, Cart, CartDetails, generate_password_hash, check_password_hash
from ...extension import db

main = Blueprint('main', __name__)
app = Flask(__name__)

# Upload Folder Untuk User (Foto Profile)
UPLOAD_FOLDER_1 = 'static/img/profile'
app.config['UPLOAD_FOLDER_1'] = UPLOAD_FOLDER_1

# Home Page / Index
@main.route('/', methods=['GET', 'POST'])
def index():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None
    cake_product = Cake.query.order_by(Cake.id_kue).limit(4)

    if current_user.is_authenticated:
        login = 'Yes'
    
    return render_template("index.html", login = login, register_form = register_form, login_form = login_form, cake_product = cake_product)

# Login Route 
@main.route('/login', methods=['POST'])
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
                    return redirect(url_for('admin.admin_dashboard'))
                else :
                    flash(f"Login Berhasil", "success")
                    return redirect(url_for('main.index'))
            else :
                flash(f'Password salah, silahkan coba lagi', "danger")
                return redirect(url_for('main.index'))
        else :
            flash(f"Email tidak ada, silahkan coba lagi!", "danger")
            return redirect(url_for('main.index'))
    else:
        flash("Oopss!!")
        return redirect(url_for('main.index'))

# Register Route
@main.route('/register', methods=['POST'])
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
            return redirect(url_for('main.index'))
        else:
            flash(f'Email sudah terdaftar!', "danger")
            return redirect(url_for('main.index'))
    else:
        flash('oops!!', "danger")
        return redirect(url_for('main.index'))
        
# Product Page
@main.route('/products')
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
        
# Custome Cake
@main.route('/custome', methods=['GET', 'POST'])
def custome():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'

    return render_template("custome_cake.html", register_form = register_form, login_form = login_form, login = login)
        

# Cart Page
@main.route('/cart', methods=['GET', 'POST'])
@login_required
def cart():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = 'Yes'
    id = current_user.id

    # Cek apakah ada keranjang
    user_cart = Cart.query.filter_by(user_id=id).first()

    if not user_cart:
        return render_template('empty_cart.html', login=login, register_form=register_form, login_form=login_form)

    # Jika ada cart, lanjutt
    cart_details = (db.session.query(
        CartDetails.id,
        Cake.nama.label('cake_name'),
        Cake.foto.label('cake_photo'),
        Cake.ukuran.label('cake_ukuran'),
        CartDetails.quantity,
        CartDetails.sub_total
    )
    .join(Cake, CartDetails.id_kue == Cake.id_kue)
    .join(Cart, CartDetails.id_cart == Cart.id_cart)
    .join(Users, Cart.user_id == Users.id)
    .filter(Users.id == id)
    .all()
    )

    user_cart = Cart.query.filter_by(user_id=id).first()
    total_price = user_cart.total_price if user_cart else 0

    return render_template('cart.html', login = login, register_form = register_form, login_form = login_form, cart_details = cart_details, total_price = total_price)
        
# Detail Page
@main.route('/details/<int:id_kue>', methods=['GET', 'POST']  )
def details(id_kue):
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None
    test_form = TestForm()

    cake = Cake.query.get_or_404(id_kue)
    

    if current_user.is_authenticated:
        login = 'Yes'
        return render_template("detail_product.html", login = login, register_form = register_form, login_form = login_form, cake = cake, test_form = test_form)
    else:
        flash(f"Akun Belum Login, Silahkan Login Terlebih Dahulu!", "danger")
        return render_template("detail_product.html", register_form = register_form, login_form = login_form, cake = cake, test_form = test_form)
        

# Profile Page
@main.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    login = 'Yes'
    user_form = UserForm()
    id = current_user.id
    user_profile = Users.query.get_or_404(id)
        
    return render_template('profile.html', user_profile = user_profile, user_form = user_form, login = login)

# Update Profile Logic
@main.route('/update_profile', methods=['GET', 'POST'])
@login_required
def update_profile():
    user_form = UserForm()
    id = current_user.id
    user_profile = Users.query.get_or_404(id)
    user_photo = user_profile.foto_profile

    if request.method == 'POST':
            user_profile.nama_depan = request.form['first_name'] 
            user_profile.nama_belakang = request.form['last_name'] 
            user_profile.no_telp = request.form['phone_number'] 
            user_profile.foto_profile = request.files['profile_pic']
            
            # Cek apakah user mengupdate foto profile
            if 'profile_pic' in request.files and request.files['profile_pic'].filename != '':
                    # Jika ada perubahan pada foto profile
                if user_photo:
                    try:
                        # Menghapus file gambar sebelumnya
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER_1'], user_photo))
                    except Exception as e:
                        # Jika gambar tidak bisa dihapus
                        flash(f'Error deleting previous image: {str(e)}', "error")
                # Upload gambar 
                pic_filename = secure_filename(request.files['profile_pic'].filename)
                pic_name = str(uuid.uuid1()) + "_" + pic_filename
                saver = request.files['profile_pic']
                user_profile.foto_profile = pic_name
                saver.save(os.path.join(app.config['UPLOAD_FOLDER_1'], pic_name))
            # Jika tidak ada perubahan pada foto profile 
            else:
                user_profile.foto_profile = user_photo
            # Simpan data 
            try:
                db.session.commit()
                flash(f'Data berhasil di update!', "success")
                return redirect(url_for('main.profile'))
            
            except:
                flash(f'Data gagal di update!', "danger")
                return redirect(url_for('main.profile'))
        
    return render_template('profile.html', user_profile = user_profile, user_form = user_form)

# Logout 
@main.route('/logout')
@login_required
def logout():
    logout_user()

    flash("Berhasil logout", "success")

    return redirect(url_for('main.index')) 

# Tambah ke keranjang Logic
@main.route('/user/add_products/<int:cake_id>', methods = ['GET', 'POST'])
def add_to_cart(cake_id):
    if request.method == 'POST':
        cake = Cake.query.get_or_404(cake_id)
        # Variabel yang dimasukkan ke dalam database
        cart_value = int(request.form.get('cartValue'))
        messages = request.form['message']
        sub_total = cake.harga
        id = current_user.id
        id_kue = cake_id
        # Query cart_details berdasarkan id_kue
        is_cart_details = CartDetails.query.filter_by(id_cart = id, id_kue = id_kue).first()
        # Query cart 
        is_cart = Cart.query.filter_by(user_id = id).first()

        # Jika terdapat id_kue yang sama 
        if is_cart_details:
            # Menambahkan jumlah produk ke kue yang sudah ada sebelumnya
            is_cart_details.quantity += cart_value
            is_cart_details.sub_total = sub_total * is_cart_details.quantity
            is_cart_details.message = messages
            total_price = cart_value * sub_total
            # Mengupdate total_price pada cart
            is_cart.total_price = is_cart.total_price + total_price
            
        else:
            total_price = cart_value * sub_total
            sub_total = cart_value * sub_total
            
            # Values yang akan dimasukkan ke dalam database
            add_to_cart = Cart(id_cart = id, total_price = total_price, user_id = id)
            add_to_cart_details = CartDetails(id_cart = id , quantity = cart_value, sub_total = sub_total, id_kue = id_kue, message = messages)
    
            # Lakukan percobaan apabila belum ada id_cart yang sama (user belum punya cart) harusnya berhasil
            try:
                db.session.add(add_to_cart)
                db.session.commit()

                db.session.add(add_to_cart_details)
                db.session.commit()
                flash(f'Produk berhasil ditambahkan!', 'success')
                return redirect(url_for('main.details', id_kue = cake_id))

            # Terjadi apabila user sudah punya keranjang, akan tetapi produk tersebut dimasukkan ke dalam cart_details dan update total_price pada cart
            except IntegrityError as e:
                db.session.rollback()
                is_cart.total_price = is_cart.total_price + total_price
    
                db.session.add(add_to_cart_details)
                db.session.commit()
                flash('Produk Berhasil Ditambahkan!', 'success')
                return redirect(url_for('main.details', id_kue = cake_id))
            
            # Terjadi apabila datanya tidak bisa dimasukkan
            except Exception as e:
                db.session.rollback()
                flash(f'gagal update data, Error : {e}', 'error')
                return redirect(url_for('main.index'))
        try :
            db.session.commit()
            flash('Produk berhasil ditambahkan!', 'success')
            return redirect(url_for('main.details', id_kue = cake_id))

        except Exception as e:
            db.session.rollback()
            flash(f'Gagal update data --> Except e = 2, Error : {e}.', 'error')
            return redirect(url_for('main.details', id_kue = cake_id))

    return redirect(url_for('main.cart'))

# Hapus keranjang logic
@main.route('/user/delete_cart/<int:detail_id>', methods = ['GET', 'POST'])
@login_required
def delete_cart(detail_id):
    # Mengambil id cart_details (produk pada cart yg ingin dihapus)
    id = detail_id
    user_id = current_user.id
    # Query datanya 
    cart_to_delete = CartDetails.query.get_or_404(id)
    # Query cart berdasarkan user_id
    current_cart = Cart.query.get_or_404(user_id)
    # Mengambil total price pada keranjang yg ingin dihapus (sub_total)
    deletedProductPrice = cart_to_delete.sub_total
    # Mengambil data total price 
    total_price = current_cart.total_price
    
    # Update total price pada tabel cart, misal x = 46.000 - 16.000 = 30.000
    newPrice = total_price - deletedProductPrice
    # Mengupdate kolom total_price
    current_cart.total_price = newPrice
    
    carts_id = current_cart.id_cart
    
    try :
        db.session.delete(cart_to_delete)
        # Menghitung jumlah data yang ada pada cart_details user
        cart_details_row = CartDetails.query.filter(CartDetails.id_cart == carts_id).count()
    
        if cart_details_row == 0:
            # Jika tidak ada produk lagi, hapus juga entri cart
            db.session.delete(current_cart)
            
        db.session.commit()
        flash(f'Produk berhasil dihapus!', 'success')
        
        return redirect(url_for('main.cart'))
    
    except :
        flash(f'Produk gagal dihapus!', 'danger')
        return redirect(url_for('main.cart'))