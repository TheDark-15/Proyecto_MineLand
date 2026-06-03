"""
MineLand Center
Tienda online gaming desarrollada con Flask.
"""

from flask import Flask, render_template, abort

# =====================================================
# Inicialización Flask
# =====================================================

app = Flask(__name__)

# =====================================================
# Base de datos temporal de productos
# =====================================================

products = [
    {
        "id": 1,
        "name": "PlayStation 5",
        "price": 499.99,
        "description": (
            "Consola de nueva generación de Sony "
            "con gráficos avanzados y SSD ultrarrápido."
        ),
        "image_url": "images/ps5.jpg"
    },
    {
        "id": 2,
        "name": "Nintendo Switch 2",
        "price": 449.99,
        "description": (
            "Consola híbrida de Nintendo "
            "con nuevas funciones online."
        ),
        "image_url": "images/switch2.jpg"
    },
    {
        "id": 3,
        "name": "Xbox Series X",
        "price": 499.99,
        "description": (
            "Potencia extrema para juegos en 4K "
            "con Ray Tracing."
        ),
        "image_url": "images/xbox.jpg"
    },
    {
        "id": 4,
        "name": "PC Gamer RGB",
        "price": 1299.99,
        "description": (
            "Computadora gamer de alto rendimiento "
            "con iluminación RGB."
        ),
        "image_url": "images/pcgamer.jpg"
    }
]

# =====================================================
# Página principal
# =====================================================

@app.route('/')
def home():
    """
    Página principal.
    """

    return render_template(
        'index.html',
        products=products,
        page_title='Inicio'
    )

# =====================================================
# Detalle del producto
# =====================================================

@app.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    Página de detalles del producto.
    """

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
    """
    Página nosotros.
    """

    return render_template(
        'about.html',
        page_title='Nosotros'
    )

# =====================================================
# Contacto
# =====================================================

@app.route('/contact')
def contact():
    """
    Página contacto.
    """

    return render_template(
        'contact.html',
        page_title='Contacto'
    )

# =====================================================
# Error 404
# =====================================================

@app.errorhandler(404)
def page_not_found(error):
    """
    Error personalizado 404.
    """

    return render_template(
        '404.html',
        page_title='No encontrado'
    ), 404

# =====================================================
# Ejecutar Flask
# =====================================================
import os

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
