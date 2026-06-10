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

import os

# =====================================================
# Inicialización Flask
# =====================================================

app = Flask(__name__)

app.secret_key = "mineland_secret_key"

# =====================================================
# Base de datos temporal de productos
# =====================================================

products = [
    {
        "id": 1,
        "name": "PlayStation 5",
        "price": 499.99,
        "description": (
            "Consola de nueva generación "
            "de Sony con SSD ultrarrápido."
        ),
        "image_url": "images/ps5.jpg"
    },
    {
        "id": 2,
        "name": "Nintendo Switch 2",
        "price": 449.99,
        "description": (
            "Consola híbrida moderna "
            "con nuevas funciones online."
        ),
        "image_url": "images/switch2.jpg"
    },
    {
        "id": 3,
        "name": "Xbox Series X",
        "price": 499.99,
        "description": (
            "Potencia extrema gaming "
            "con resolución 4K."
        ),
        "image_url": "images/xbox.jpg"
    },
    {
        "id": 4,
        "name": "PC Gamer RGB",
        "price": 1299.99,
        "description": (
            "Computadora gamer premium "
            "con iluminación RGB."
        ),
        "image_url": "images/pcgamer.jpg"
    }
]

# =====================================================
# CARRITO
# =====================================================

cart = []

# =====================================================
# LOGIN
# =====================================================

USERNAME = "admin"
PASSWORD = "1234"

# =====================================================
# Página principal
# =====================================================

@app.route('/')
def home():

    search = request.args.get('search')

    filtered_products = products

    if search:

        filtered_products = [
            product for product in products
            if search.lower() in product["name"].lower()
        ]

    return render_template(
        'index.html',
        products=filtered_products,
        page_title='Inicio'
    )

# =====================================================
# Detalle producto
# =====================================================

@app.route('/product/<int:product_id>')
def product_detail(product_id):

    product = next(
        (
            item for item in products
            if item["id"] == product_id
        ),
        None
    )

    if product is None:
        abort(404)

    return render_template(
        'product_detail.html',
        product=product,
        page_title=product["name"]
    )

# =====================================================
# Nosotros
# =====================================================

@app.route('/about')
def about():

    return render_template(
        'about.html',
        page_title='Nosotros'
    )

# =====================================================
# Contacto
# =====================================================

@app.route('/contact')
def contact():

    return render_template(
        'contact.html',
        page_title='Contacto'
    )

# =====================================================
# LOGIN
# =====================================================

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

            return redirect(url_for('dashboard'))

        error = "Usuario o contraseña incorrectos"

    return render_template(
        'login.html',
        error=error,
        page_title='Login'
    )

# =====================================================
# LOGOUT
# =====================================================

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect(url_for('home'))

# =====================================================
# DASHBOARD
# =====================================================

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        'dashboard.html',
        products=products,
        page_title='Dashboard'
    )

# =====================================================
# AGREGAR PRODUCTO
# =====================================================

@app.route(
    '/add_product',
    methods=['GET', 'POST']
)
def add_product():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        new_product = {
            "id": len(products) + 1,
            "name": request.form.get('name'),
            "price": float(
                request.form.get('price')
            ),
            "description": request.form.get(
                'description'
            ),
            "image_url": (
                f"images/"
                f"{request.form.get('image_url')}"
            )
        }

        products.append(new_product)

        return redirect(url_for('dashboard'))

    return render_template(
        'add_product.html',
        page_title='Agregar Producto'
    )

# =====================================================
# EDITAR PRODUCTO
# =====================================================

@app.route(
    '/edit_product/<int:product_id>',
    methods=['GET', 'POST']
)
def edit_product(product_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    product = next(
        (
            item for item in products
            if item["id"] == product_id
        ),
        None
    )

    if product is None:
        abort(404)

    if request.method == 'POST':

        product['name'] = request.form.get(
            'name'
        )

        product['price'] = float(
            request.form.get('price')
        )

        product['description'] = request.form.get(
            'description'
        )

        image_url = request.form.get(
            'image_url'
        )

        product['image_url'] = (
            f"images/{image_url}"
        )

        return redirect(
            url_for('dashboard')
        )

    return render_template(
        'edit_product.html',
        product=product,
        page_title='Editar Producto'
    )

# =====================================================
# ELIMINAR PRODUCTO
# =====================================================

@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    product = next(
        (
            item for item in products
            if item["id"] == product_id
        ),
        None
    )

    if product is None:
        abort(404)

    products.remove(product)

    return redirect(url_for('dashboard'))

# =====================================================
# CARRITO
# =====================================================

@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):

    product = next(
        (
            item for item in products
            if item["id"] == product_id
        ),
        None
    )

    if product is None:
        abort(404)

    cart.append(product)

    return redirect(url_for('cart_page'))

@app.route('/cart')
def cart_page():

    total = sum(
        item['price'] for item in cart
    )

    return render_template(
        'cart.html',
        cart=cart,
        total=total,
        page_title='Carrito'
    )

# =====================================================
# ERROR 404
# =====================================================

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        '404.html',
        page_title='No encontrado'
    ), 404

# =====================================================
# EJECUTAR FLASK
# =====================================================

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
