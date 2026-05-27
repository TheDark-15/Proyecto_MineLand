# ============================================================
#  MineLand — Aplicación Web Flask
#  Página de inicio inspirada en la estética de Minecraft
#  Autor  : MineLand Dev
#  Python : 3.14.3
#  Uso    : python app.py   (requiere: pip install Flask)
# ============================================================

from flask import Flask, render_template

# Inicializar la aplicación Flask
# static_folder y template_folder usan las rutas por defecto,
# pero se declaran explícitamente para mayor claridad.
app = Flask(
    __name__,
    static_folder="static",       # Sirve CSS, JS e imágenes
    template_folder="templates"   # Contiene index.html
)


# ----------------------------------------------------------
# Ruta principal — Página de inicio
# ----------------------------------------------------------
@app.route("/")
def index():
    """Renderiza la página de inicio de MineLand."""
    return render_template("index.html")


# ----------------------------------------------------------
# Rutas de secciones (páginas futuras — placeholder 200 OK)
# ----------------------------------------------------------
@app.route("/jugar")
def jugar():
    return "<h2 style='font-family:sans-serif;text-align:center;margin-top:10%'>🎮 Sección JUGAR — Próximamente</h2>"


@app.route("/noticias")
def noticias():
    return "<h2 style='font-family:sans-serif;text-align:center;margin-top:10%'>📰 Sección NOTICIAS — Próximamente</h2>"


@app.route("/tienda")
def tienda():
    return "<h2 style='font-family:sans-serif;text-align:center;margin-top:10%'>🛒 Sección TIENDA — Próximamente</h2>"


@app.route("/comunidad")
def comunidad():
    return "<h2 style='font-family:sans-serif;text-align:center;margin-top:10%'>🌐 Sección COMUNIDAD — Próximamente</h2>"


# ----------------------------------------------------------
# Punto de entrada
# ----------------------------------------------------------
if __name__ == "__main__":
    # debug=True activa el recargado automático durante el desarrollo
    # Acceder en: http://127.0.0.1:5000
    app.run(debug=True)