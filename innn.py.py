#importamos todas las librerias necesarias
from flask import Flask, request, render_template, redirect, url_for,make_response
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
import time

app = Flask(__name__) #instanciamos nuestro objeto Flask
'''
---------------------------------------------
-------------SECCIÓN DE RUTAS---------------- 
---------------------------------------------
'''

@app.route('/') #ruta principal
def home():
    if current_user.is_authenticated: #Si el usuario está logueado se muestra su nombre, si no se pide que se loguee
        return render_template('index.html', nombre=NombreDelUsuario)
    else:
        return render_template('index.html', nombre="identifiquese...")
    
@app.route('/cursos') #ruta Solo de cursos
def  cursos():
 if current_user.is_authenticated:
        return render_template('cursos.html', nombre=NombreDelUsuario)
 else:
    return render_template('cursos.html', nombre="identifiquese...")
 
@app.route('/about') #acerca de...
def  about():
 if current_user.is_authenticated:
        return render_template('about.html', nombre=NombreDelUsuario)
 else:
    return render_template('about.html', nombre="identifiquese...")

@app.route('/contacto')
def  contacto():
 if current_user.is_authenticated:
        return render_template('contacto.html', nombre=NombreDelUsuario)
 else:
    return render_template('contacto.html', nombre="identifiquese...")
 
@app.route('/query') #esto es para unas pruebas, (en contrución)
def preguntas():
    return make_response('Hola mundo', 200)

@app.errorhandler(404) #en caso de que el usuario se meta a un lugar que no existe
def page_not_found(error):
    # Redirige al usuario a la página de inicio después de 5 segundos
    Respuesta404 = make_response("Disculpe, no pudimos encontrar la página que busca ... Será redirigido al Inicio", 404)
    Respuesta404.headers['Refresh'] = '5;url=' + url_for('home')
    return Respuesta404
'''
---------------------------------------------
------------CONFIGURACIONES------------------ 
---------------------------------------------
'''

#Configuración del Login manager
login_manager = LoginManager()
login_manager.init_app(app)
app.secret_key = 'admin'

# Configuración de la base de datos
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="root",
    database="APPBD",
    consume_results=True
)
# Esto es solo en modo debuggin, en producción obviamente todo será más seguro

# Creamos nuestra clase usuario
class User(UserMixin):
    def __init__(self, email, id):
        self.id = id
        self.email = email

@login_manager.user_loader
def load_user(user_id):
    cursor = db.cursor() #sé que hay formas más  livianas, pero no se me ocurrió otra cosa que un cursor
    query = "SELECT * FROM Usuarios WHERE id = %s"
    params = (user_id,)
    cursor.execute(query, params)
    user = cursor.fetchone() # 
    cursor.close()  # El cursor debe cerrarse
    
    if user:
        return User(user[1], user[0])
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        cursor = db.cursor()
        query = "SELECT * FROM Usuarios WHERE correo = %s"
        params = (email,)
        cursor.execute(query, params)
        user = cursor.fetchone()
        cursor.close()  # Close the cursor after fetching the data
        if user:
            user = User(user[1], user[0])
            login_user(user)
            return redirect(url_for('protected'))
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        cursor = db.cursor()
        query = "INSERT INTO Usuarios (nombre, correo) VALUES (%s, %s)"
        params = (name, email)
        cursor.execute(query, params)
        db.commit()
        cursor.close()  # Close the cursor after committing the data
        return redirect(url_for('login'))
    return render_template('register.html')

NombreDelUsuario = "identifiquese"

@app.route('/protected')
@login_required
def protected():
    global NombreDelUsuario
    user_id = current_user.get_id()  # Obtiene el ID del usuario logueado
    cursor = db.cursor()
    query = "SELECT nombre FROM Usuarios WHERE id = %s"
    params = (user_id,)
    cursor.execute(query, params)
    NombreDelUsuario = cursor.fetchone()[0]
    results = cursor.fetchall()
    cursor.close()  # Close the cursor after fetching the data
    return f"Estás logueado, {NombreDelUsuario}. ¡Bienvenido!"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

'''
---------------------------------------------
------COMPROBACIONES Y PUESTA EN MARCHA------
---------------------------------------------
'''
print("Hola, esta aplicación web flask fue creada por Fabricio D Gallo")
if db.is_connected(): #Comprbación de conexión a mysql
    print("Conexión exitosa a la base de datos.")
else:
    print("No se pudo conectar a la base de datos.")

if __name__ == "__main__": #¿Nuestra objeto flask se instanció correctamente?
    app.run(debug=True)    # entonces  ejecutar en modo debuggin

