from itertools import product
from flask import Blueprint, redirect, render_template, request, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from flask import Flask
from sqlalchemy.exc import IntegrityError
import os 
import uuid as uuid
from werkzeug.utils import secure_filename

from ...forms.forms import LoginForm, RegisterForm, UpdateForm, AddForm
from ...models.models import Users, Cake, Cart, CartDetails, generate_password_hash, check_password_hash, OrderDetails, Orders
from ...extension import db

admin = Blueprint('admin', __name__)
app = Flask(__name__)

UPLOAD_FOLDER_2 = 'app/static/img/foto_produk'
app.config['UPLOAD_FOLDER_2'] = UPLOAD_FOLDER_2

if not os.path.exists(UPLOAD_FOLDER_2):
    os.makedirs(UPLOAD_FOLDER_2)

# Update Product Route
@admin.route('/update_product/<int:id_kue>', methods=['POST', 'GET'])
@login_required
def update(id_kue):
    if current_user.role == 'admin':
        product_to_update = Cake.query.get_or_404(id_kue)
        cake_photo = product_to_update.foto
        cake_detail = product_to_update.detail
        if request.method == 'POST':
            product_to_update.nama = request.form['nama'] 
            product_to_update.harga = request.form['harga'] 
            product_to_update.varian = request.form['varian'] 
            product_to_update.ukuran = request.form['ukuran'] 
            product_to_update.detail = request.form['detail'] 
            product_to_update.foto = request.files['foto']
            
            # Cek apakah ada foto yang diupdate
            if 'foto' in request.files and request.files['foto'].filename != '':
                if cake_photo:
                    try:
                        # Menghapus file gambar sebelumnya
                        os.remove(os.path.join(app.config['UPLOAD_FOLDER_2'], cake_photo))
                    except Exception as e:
                        # Jika gambar tidak bisa dihapus
                        flash(f'Error deleting previous image: {str(e)}', "error")
                # Upload gambar 
                pic_filename = secure_filename(request.files['foto'].filename)
                saver = request.files['foto']
                product_to_update.foto = pic_filename
                saver.save(os.path.join(app.config['UPLOAD_FOLDER_2'], pic_filename))
            else:
                # Jika tidak ada jangan lakukan perubahan
                product_to_update.foto = cake_photo

                # Jika tidak ada perubahan pada detail jangan lakukan perubahan
            if not product_to_update.detail:
                product_to_update.detail = cake_detail

            try:
                db.session.commit()
                flash(f'Produk berhasil di update!', "success")
                return redirect(url_for('admin.admin_product'))
            
            except IntegrityError as e :
                flash(f'Data gagal di update! error : {e}' , "danger")
                return redirect(url_for('admin.admin_product'))
        else:
            return redirect(url_for('admin.admin_product'))
    else:
        flash(f'Anda tidak bisa masuk ke halaman ini!', "error")
        return redirect(url_for('main.index'))
        

    
# Delete Product Route
@admin.route('/delete_product/<int:id_kue>', methods=['POST', 'GET'])
@login_required
def delete(id_kue):
    if current_user.role == 'admin':
        product_to_delete = Cake.query.get_or_404(id_kue)
        try :
            db.session.delete(product_to_delete)
            db.session.commit()
            flash(f'Produk berhasil di hapus!', "success")
            return redirect(url_for('admin.admin_product'))
    
        except:
            flash(f'Data gagal di hapus!', "danger")
            return redirect(url_for('admin.admin_product'))
    else :
        flash(f'Anda tidak bisa masuk di halaman ini!', "danger")
        return redirect(url_for('main.index'))

# Tambah Produk
@admin.route('/addproduct', methods=['POST'])
@login_required
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
            return redirect(url_for('admin.admin_product'))
        else:
            flash(f'Data gagal di tambahkan!', "danger")
            return redirect(url_for('admin.admin_product'))
    else:
        flash(f'Anda tidak bisa masuk di halaman ini!', "danger")
        return redirect(url_for('main.index'))
          
# Dashboard Admin
@admin.route('/admin/dashboard', methods=['GET', 'POST'])
@login_required
def admin_dashboard():
    
    if current_user.role == 'admin':
        product_total = Cake.query.count()
        orders_total = Orders.query.count()
        accepted_order = Orders.query.filter(Orders.order_status == 'Pesanan Diterima').count()
        rejected_order = Orders.query.filter(Orders.order_status == 'Pesanan Ditolak').count()
        return render_template("admin/admin.html", product_total = product_total, orders_total = orders_total, accepted_order = accepted_order, rejected_order = rejected_order)
    else :
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('main.index'))

# Bagian Produk
@admin.route('/admin/product', methods=['GET', 'POST'])
@login_required
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
        return redirect(url_for('main.index'))

# Bagian Pesanan
@admin.route('/admin/order', methods=['GET', 'POST'])
@login_required
def admin_order():
    register_form = RegisterForm()
    login_form = LoginForm()
    login = None

    if current_user.is_authenticated:
        login = 'Yes'

    if current_user.role == 'admin':
        orders = Orders.query.order_by(Orders.id_orders)
        return render_template("admin/admin_order.html", login = login, register_form = register_form, login_form = login_form, orders = orders)
    else :
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('main.index'))  
    
@admin.route('/get_order_details/<int:order_id>', methods=['GET'])
@login_required
def get_order_details(order_id):
    # Ambil data OrderDetails berdasarkan order_id
    order_details = db.session.query(
        OrderDetails.id_kue,
        OrderDetails.quantity,
        OrderDetails.sub_total,
        Cake.foto.label('cake_foto'),
        Cake.nama.label('cake_name'),
        Cake.ukuran.label('cake_ukuran')
    ).join(Cake, OrderDetails.id_kue == Cake.id_kue).filter(OrderDetails.id_orders == order_id).all()

    return render_template('admin/order_details.html', order_details=order_details)

@admin.route('/accept_order/<int:id_orders>', methods=['GET', 'POST'])
@login_required
def accept_order(id_orders):
    id = id_orders
    if current_user.role == 'admin':
        status = Orders.query.get_or_404(id)
        status.order_status = 'Pesanan Diterima'
        db.session.commit()
        flash(f'Pesanan Diterima', 'success')
        return redirect(url_for('admin.admin_order'))
    else:
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('main.index'))  
    
@admin.route('/reject_order/<int:id_orders>', methods=['GET', 'POST'])
@login_required
def reject_order(id_orders):
    id = id_orders
    
    if current_user.role == 'admin':
        status = Orders.query.get_or_404(id)
        status.order_status = 'Pesanan Ditolak'
        db.session.commit()
        flash(f'Pesanan Ditolak', 'success')
        return redirect(url_for('admin.admin_order'))
        
    else:
        flash("Anda tidak bisa mengakses halaman ini!", "error")
        return redirect(url_for('main.index'))  