from flask import Flask, render_template, url_for

app = Flask(__name__)


# Home Page
@app.route('/')
def index():
    return render_template('index.html')


# Product Page
@app.route('/products')
def products():
    return render_template('all_products.html')

# Base HTML
@app.route('/base')
def base():
    return render_template('base.html')

# Custome Cake
@app.route('/custome')
def custome():
    return render_template('custome_cake.html')

# Cart Page
@app.route('/cart')
def cart():
    return render_template('cart.html')

# Detail Page
@app.route('/details')
def details():
    return render_template('detail_product.html')

if __name__ == "__main__":
    app.run(debug=True)

