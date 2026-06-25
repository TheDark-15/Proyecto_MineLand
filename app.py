"""
MineLand Center
Tienda online gaming desarrollada con Flask.
"""

from flask import (
    Flask,
    render_template,
    abort,
    request,
    redirect,
    url_for,
    session
)

from flask_sqlalchemy import SQLAlchemy

import os

app = Flask(__name__)

app.secret_key = "mineland_secret_key"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    'sqlite:///database.db'
)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String(100),
        nullable=False
    )

    price = db.Column(
        db.Float,
        nullable=False
    )

    description = db.Column(
        db.Text,
        nullable=False
    )

    image_url = db.Column(
        db.String(200),
        nullable=False
    )

with app.app_context():

    db.create_all()

    if Product.query.count() == 0:

        sample_products = [

            Product(
                name="PlayStation 5",
                price=2599.99,
                description=(
                    "Consola de nueva generación "
                    "de Sony con SSD ultrarrápido."
                ),
                image_url="images/ps5.jpg"
            ),

            Product(
                name="Nintendo Switch 2",
                price=2459.99,
                description=(
                    "Consola híbrida moderna "
                    "con nuevas funciones online."
                ),
                image_url="images/switch2.jpg"
            ),

            Product(
                name="Xbox Series X",
                price=2199.99,
                description=(
                    "Potencia extrema gaming "
                    "con resolución 4K."
                ),
                image_url="images/xbox.jpg"
            ),

             Product(
                name="PC Gamer Razer X",
                price=2999.99,
                description=(
                    "Potente equipo gamer con 664 GB y 32 Ram"
                    "con resolución 4K y tarjeta grafica incluida."
                ),
                image_url="images/pcgamer.jpg"
            )

        ]

        db.session.add_all(sample_products)

        db.session.commit()

USERNAME = "admin"
PASSWORD = "1234"

@app.route('/')
def home():

    search = request.args.get('search')

    if search:

        products = Product.query.filter(
            Product.name.contains(search)
        ).all()

    else:

        products = Product.query.all()

    return render_template(
        'index.html',
        products=products,
        page_title='Inicio'
    )

# =====================================================
# DETALLE PRODUCTO
# =====================================================

@app.route('/product/<int:product_id>')
def product_detail(product_id):

    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    return render_template(
        'product_detail.html',
        product=product,
        page_title=product.name
    )

@app.route('/about')
def about():

    return render_template(
        'about.html',
        page_title='Nosotros'
    )

@app.route('/contact')
def contact():

    return render_template(
        'contact.html',
        page_title='Contacto'
    )

@app.route('/login', methods=['GET', 'POST'])
def login():

    error = None

    if request.method == 'POST':

        username = request.form.get('username')
        password = request.form.get('password')

        if (
            username == USERNAME and
            password == PASSWORD
        ):

            session['user'] = username

            return redirect(
                url_for('dashboard')
            )

        error = (
            "Usuario o contraseña incorrectos"
        )

    return render_template(
        'login.html',
        error=error,
        page_title='Login'
    )

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:

        return redirect(
            url_for('login')
        )

    products = Product.query.all()

    return render_template(
        'dashboard.html',
        products=products,
        page_title='Dashboard'
    )

@app.route(
    '/add_product',
    methods=['GET', 'POST']
)
def add_product():

    if 'user' not in session:

        return redirect(
            url_for('login')
        )

    if request.method == 'POST':

        new_product = Product(

            name=request.form.get('name'),

            price=float(
                request.form.get('price')
            ),

            description=request.form.get(
                'description'
            ),

            image_url=(
                f"images/"
                f"{request.form.get('image_url')}"
            )
        )

        db.session.add(new_product)

        db.session.commit()

        return redirect(
            url_for('dashboard')
        )

    return render_template(
        'add_product.html',
        page_title='Agregar Producto'
    )

@app.route(
    '/edit_product/<int:product_id>',
    methods=['GET', 'POST']
)
def edit_product(product_id):

    if 'user' not in session:

        return redirect(
            url_for('login')
        )

    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    if request.method == 'POST':

        product.name = request.form.get(
            'name'
        )

        product.price = float(
            request.form.get('price')
        )

        product.description = request.form.get(
            'description'
        )

        product.image_url = (
            f"images/"
            f"{request.form.get('image_url')}"
        )

        db.session.commit()

        return redirect(
            url_for('dashboard')
        )

    return render_template(
        'edit_product.html',
        product=product,
        page_title='Editar Producto'
    )

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):

    if 'user' not in session:

        return redirect(
            url_for('login')
        )

    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    db.session.delete(product)

    db.session.commit()

    return redirect(
        url_for('dashboard')
    )

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):

    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    if 'cart' not in session:

        session['cart'] = []

    session['cart'].append({

        "id": product.id,
        "name": product.name,
        "price": product.price,
        "image_url": product.image_url

    })

    session.modified = True

    return redirect(
        url_for('cart_page')
    )

@app.route('/cart')
def cart_page():

    cart = session.get('cart', [])

    total = sum(
        item['price']
        for item in cart
    )

    return render_template(
        'cart.html',
        cart=cart,
        total=total,
        page_title='Carrito'
    )

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):

    cart = session.get('cart', [])

    if 0 <= index < len(cart):

        cart.pop(index)

    session['cart'] = cart

    session.modified = True

    return redirect(
        url_for('cart_page')
    )

@app.route('/clear_cart')
def clear_cart():

    session['cart'] = []

    session.modified = True

    return redirect(
        url_for('cart_page')
    )

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        '404.html',
        page_title='No encontrado'
    ), 404

if __name__ == '__main__':

    port = int(
        os.environ.get("PORT", 5000)
    )

    app.run(
        host='0.0.0.0',
        port=port
    )
