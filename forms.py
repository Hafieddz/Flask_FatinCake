from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, ValidationError, BooleanField, TextAreaField, IntegerField
from flask_wtf.file import FileAllowed, FileField
from wtforms.validators import DataRequired, EqualTo, Length, data_required, length

# Register Form 
class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired()])
    password_hash = PasswordField("Password", validators=[DataRequired(), EqualTo('confirm_password', message='password harus sama!'), length(8)])
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
    profile_pic = FileField("Profile Picture", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Hanya bisa upload gambar!')])
    submit_form = SubmitField("Update Data")
    
# Update Product Form
class UpdateForm(FlaskForm):
    nama = StringField("Nama Kue", validators=[DataRequired()])
    harga = StringField("Harga Kue", validators=[DataRequired()])
    varian = StringField("Varian", validators=[DataRequired()])
    foto = FileField("Foto Produk", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Hanya bisa upload gambar!')])
    ukuran = StringField("Ukuran", validators=[DataRequired()])
    detail = TextAreaField("Detail", validators=[DataRequired()])
    submit_update = SubmitField("Update")

# Add Product Form
class AddForm(FlaskForm):
    nama = StringField("Nama Kue", validators=[DataRequired()])
    harga = StringField("Harga Kue", validators=[DataRequired()])
    varian = StringField("Varian", validators=[DataRequired()])
    foto = FileField("Foto Produk", validators=[DataRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Hanya bisa upload gambar!')])
    ukuran = StringField("Ukuran", validators=[DataRequired()])
    detail = TextAreaField("Detail", validators=[DataRequired()])
    submit_add = SubmitField("Tambah") 

class TestForm(FlaskForm):
    submit_test = SubmitField('Tambah ke keranjang')