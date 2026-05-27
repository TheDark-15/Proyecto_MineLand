# ============================================================
#  MineLand — Aplicación Web Flask
#  Página de inicio inspirada en Minecraft
#  Compatible con Render
# ============================================================

from flask import Flask, render_template
import os

# Inicializar aplicación Flask
app = Flask(
    __name__,
    static_folder="static",
    template_folder="templates"
)

# ----------------------------------------------------------
# Página principal
# ----------------------------------------------------------
@app.route("/")
def index():
    return render_template("index.html")


# ----------------------------------------------------------
# Rutas adicionales
# ----------------------------------------------------------
@app.route("/jugar")
def jugar():
    return """
    <h2 style='font-family:sans-serif;
               text-align:center;
               margin-top:10%'>
        🎮 Sección JUGAR — Próximamente
    </h2>
    """


@app.route("/noticias")
def noticias():
    return """
    <h2 style='font-family:sans-serif;
               text-align:center;
               margin-top:10%'>
        📰 Sección NOTICIAS — Próximamente
    </h2>
    """


@app.route("/tienda")
def tienda():
    return """
    <h2 style='font-family:sans-serif;
               text-align:center;
               margin-top:10%'>
        🛒 Sección TIENDA — Próximamente
    </h2>
    """


@app.route("/comunidad")
def comunidad():
    return """
    <h2 style='font-family:sans-serif;
               text-align:center;
               margin-top:10%'>
        🌐 Sección COMUNIDAD — Próximamente
    </h2>
    """


# ----------------------------------------------------------
# Ejecutar aplicación (IMPORTANTE PARA RENDER)
# ----------------------------------------------------------
if __name__ == "__main__":

    # Render asigna automáticamente el puerto
    port = int(os.environ.get("PORT", 5000))

    # host="0.0.0.0" permite acceso externo
    app.run(host="0.0.0.0", port=port)
