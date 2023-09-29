from flask import Flask, render_template, url_for

app = Flask(__name__)

@app.route('/home')
def index():
    return render_template('index.html')

@app.route('/products')
def products():
    return render_template('all_products.html')

@app.route('/base')
def base():
    return render_template('base.html')

@app.route('/')
def custome_cake():
    return render_template('custome_cake.html')

@app.route('/cart')
def cart():
    return render_template('cart.html')

if __name__ == "__main__":
    app.run(debug=True)

