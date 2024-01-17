from flask import Flask, render_template, make_response,url_for
import time
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')
@app.route('/cursos')
def  course():
    return render_template('cursos.html')
@app.route('/about')
def  about():
    return render_template('cursos.html')
@app.route('/contact')
def  contact():
    return render_template('cursos.html')
@app.route('/query')
def preguntas():
    return make_response('Hola mundo', 200)
@app.errorhandler(404)
def page_not_found(error):
    # Redirige al usuario a la página de inicio después de 5 segundos
    Respuesta404 = make_response("Disculpe, no pudimos encontrar la página que busca ... Será redirigido al Inicio", 404)
    Respuesta404.headers['Refresh'] = '5;url=' + url_for('home')
    return Respuesta404
if __name__ == '__main__':
    app.run(debug=True)
