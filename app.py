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
from werkzeug.security import generate_password_hash
import os

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY", "dev_key_change_me")

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=False)

    description = db.Column(db.Text, nullable=False)

    image_url = db.Column(db.String(200), nullable=False)

    # STOCK (CP08)
    stock = db.Column(db.Integer, default=10)

class Customer(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)

    email = db.Column(db.String(100), unique=True, nullable=False)

    password = db.Column(db.String(255), nullable=False)

class Purchase(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    customer_name = db.Column(db.String(100), nullable=False)

    product_name = db.Column(db.String(100), nullable=False)

    price = db.Column(db.Float, nullable=False)

with app.app_context():

    db.create_all()

    if Customer.query.count() == 0:

        demo = Customer(
            name="Cliente Demo",
            email="demo@mineland.com"
        )

        db.session.add(demo)
        db.session.commit()

    if Product.query.count() == 0:

        sample_products = [

            Product(
                name="PlayStation 5",
                price=2599.99,
                stock=8,
                description="Consola de nueva generación de Sony con SSD ultrarrápido.",
                image_url="images/ps5.jpg"
            ),

            Product(
                name="Nintendo Switch 2",
                price=2459.99,
                stock=5,
                description="Consola híbrida moderna con nuevas funciones online.",
                image_url="images/switch2.jpg"
            ),

            Product(
                name="Xbox Series X",
                price=2199.99,
                stock=6,
                description="Potencia extrema gaming con resolución 4K.",
                image_url="images/xbox.jpg"
            ),

            Product(
                name="PC Gamer Razer X",
                price=2999.99,
                stock=3,
                description="Potente equipo gamer con 32 RAM y 4K.",
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

        if username == USERNAME and password == PASSWORD:

            session['user'] = username

            return redirect(url_for('dashboard'))

        error = "Usuario o contraseña incorrectos"

    return render_template(
        'login.html',
        error=error,
        page_title='Login'
    )
    
@app.route('/register_customer', methods=['GET', 'POST'])
def register_customer():

    if request.method == 'POST':

        name = request.form.get('name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Validar campos vacíos
        if not name or not email or not password or not confirm_password:

            return render_template(
                'register.html',
                error="Todos los campos son obligatorios.",
                page_title="Registro"
            )

        # Validar contraseña
        if password != confirm_password:

            return render_template(
                'register.html',
                error="Las contraseñas no coinciden.",
                page_title="Registro"
            )

        # Verificar si el correo ya existe
        existe = Customer.query.filter_by(email=email).first()

        if existe:

            return render_template(
                'register.html',
                error="El correo electrónico ya está registrado.",
                page_title="Registro"
            )

        # Encriptar contraseña
        password_hash = generate_password_hash(password)

        # Crear cliente
        customer = Customer(
            name=name,
            email=email,
            password=password_hash
        )

        db.session.add(customer)
        db.session.commit()

        return render_template(
            'register.html',
            success="¡Registro realizado correctamente! Ya puedes iniciar sesión.",
            page_title="Registro"
        )

    return render_template(
        'register.html',
        page_title="Registro"
    )
@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:

        return redirect(url_for('login'))

    products = Product.query.all()

    return render_template(
        'dashboard.html',
        products=products,
        page_title='Dashboard'
    )

@app.route('/add_product', methods=['GET', 'POST'])
def add_product():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        image = request.form.get('image_url')

        if not name or not price or not stock or not description or not image:
            return redirect(url_for('add_product'))

        new_product = Product(
            name=name,
            price=float(price),
            stock=int(stock),
            description=description,
            image_url=f"images/{image}"
        )

        db.session.add(new_product)
        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template(
        'add_product.html',
        page_title='Agregar Producto'
    )

@app.route('/edit_product/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    if request.method == 'POST':

        name = request.form.get('name')
        price = request.form.get('price')
        stock = request.form.get('stock')
        description = request.form.get('description')
        image = request.form.get('image_url')

        if not name or not price or not stock or not description or not image:
            return redirect(url_for('edit_product', product_id=product_id))

        try:
            product.name = name
            product.price = float(price)
            product.stock = int(stock)
            product.description = description
            product.image_url = f"images/{image}"

        except ValueError:
            return redirect(url_for('edit_product', product_id=product_id))

        db.session.commit()

        return redirect(url_for('dashboard'))

    return render_template(
        'edit_product.html',
        product=product,
        page_title='Editar Producto'
    )
    
@app.route('/delete_product/<int:product_id>')
def delete_product(product_id):

    if 'user' not in session:
        return redirect(url_for('login'))

    product = Product.query.get(product_id)

    if product is None:
        abort(404)

    db.session.delete(product)
    db.session.commit()

    return redirect(url_for('dashboard'))
    
@app.route('/add_to_cart/<int:product_id>')
def add_to_cart(product_id):

    product = Product.query.get(product_id)

    if product is None:
        return redirect(url_for('cart_page', error="producto_no_existe"))

    if product.stock < 1:
        return redirect(url_for('cart_page', error="sin_stock"))

    if 'cart' not in session:
        session['cart'] = []

    session['cart'].append({
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "image_url": product.image_url
    })

    session.modified = True

    return redirect(url_for('cart_page'))
    
@app.route('/cart')
def cart_page():

    cart = session.get('cart', [])

    total = sum(float(item['price']) for item in cart)

    return render_template(
        'cart.html',
        cart=cart,
        total=total,
        error=request.args.get('error'),
        success=request.args.get('success'),
        page_title='Carrito'
    )

@app.route('/remove_from_cart/<int:index>')
def remove_from_cart(index):

    cart = session.get('cart', [])

    if 0 <= index < len(cart):
        cart.pop(index)

    session['cart'] = cart
    session.modified = True

    return redirect(url_for('cart_page'))


@app.route('/clear_cart')
def clear_cart():

    session['cart'] = []
    session.modified = True

    return redirect(url_for('cart_page'))


@app.route('/checkout', methods=['GET', 'POST'])
def checkout():

    cart = session.get('cart', [])

    if len(cart) == 0:
        return redirect(url_for('cart_page', error="carrito_vacio"))

    total = sum(float(item['price']) for item in cart)

    if request.method == "POST":

        payment = request.form.get('payment')

        if payment != "123456":
            return redirect(url_for('cart_page', error="pago"))

        customer = Customer.query.first()

        if customer is None:
            return redirect(url_for('cart_page', error="no_customer"))

        for item in cart:

            product = Product.query.get(item['id'])

            if product is None:
                return redirect(url_for('cart_page', error="producto_no_existe"))

            if product.stock <= 0:
                return redirect(url_for('cart_page', error="sin_stock"))

            product.stock -= 1

            purchase = Purchase(
                customer_name=customer.name,
                product_name=product.name,
                price=product.price
            )

            db.session.add(purchase)

        db.session.commit()

        session['cart'] = []
        session.modified = True

        return redirect(url_for('cart_page', success="1"))

    return render_template(
        "checkout.html",
        cart=cart,
        total=total,
        page_title="Finalizar Compra"
    )

@app.errorhandler(404)
def page_not_found(error):

    return render_template(
        '404.html',
        page_title='No encontrado'
    ), 404

if __name__ == '__main__':

    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )
    
