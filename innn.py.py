#importamos todas las librerias necesarias
from flask import Flask, request, render_template, redirect, url_for,make_response,flash,session
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
import mysql.connector
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash #las contraseñas se guardan en forma de hash,un toque de seguridad...

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
        return render_template('index.html', nombre="identifiquese :)")
    
@app.route('/cursos') #ruta Solo de cursos
def  cursos():
 if current_user.is_authenticated:
        return render_template('cursos.html', nombre=NombreDelUsuario)
 else:
    return render_template('cursos.html', nombre="identifiquese :)")
 
@app.route('/about') #acerca de...
def  about():
 if current_user.is_authenticated:
        return render_template('about.html', nombre=NombreDelUsuario)
 else:
    return render_template('about.html', nombre="identifiquese :)")

@app.route('/contacto')
def  contacto():
 if current_user.is_authenticated:
        return render_template('contacto.html', nombre=NombreDelUsuario)
 else:
    return render_template('contacto.html', nombre="identifiquese :)")
 
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
app.secret_key = 'admin' #Clave ultrasecreta (?)

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

#Las siguientes variables son necesarias para poder recuperar la cuenta del usuario
# el sistema de recuperación consiste en  registrarse con una pregunta secreta  y su respuesta.
PreguntaSecreta=""
RespuestaSecreta=""
RespuestaUsuario=""

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')        # Obtenemos mail y contraseña
        password = request.form.get('password')  #
        cursor = db.cursor() #Instanciamos nuestro cursor para la base de datos
        query = "SELECT * FROM Usuarios WHERE correo = %s"
        params = (email,)
        cursor.execute(query, params)
        user = cursor.fetchone()
        cursor.close()  # Importante cerrrar el cursor
        session['PreguntaSecreta'] = user[4] #Recuperamos la pregunta y respuesta secreta
        session['RespuestaSecreta'] = user[5]
        if user:
            # Checkeamos que el usuario haya metido la contraseña correcta
            if check_password_hash(user[3], password):  # "password" está en la cuarta (tercera desde el 0) columna
                user = User(user[1], user[0])
                login_user(user)
                return redirect(url_for('protected'))
            else:
               flash('Usuario o contraseña incorrectos, si no tiene una cuenta, registrese.')
    return render_template('login.html',nombre="logueando")



@app.route('/RecuperandoCuenta', methods=['GET', 'POST'])  #Esta 
def RecuperandoCuenta():
    pregunta_secreta = session.get('PreguntaSecreta')
    if request.method == 'POST':
        RespuestaUsuario = request.form.get('Respuesta')
        new_password = request.form.get('new_password')
        if session.get('RespuestaSecreta') == RespuestaUsuario:
            # Generamos el hash de la nueva contraseña
            hashed_password = generate_password_hash(new_password)
            # Obtenemos el correo del usuario
            email = session.get('email')
            # Actualizamos la contraseña en la base de datos
            cursor = db.cursor()
            query = "UPDATE Usuarios SET password = %s WHERE correo = %s"
            params = (hashed_password, email)
            cursor.execute(query, params)
            db.commit()
            cursor.close()
            flash('Contraseña cambiada exitosamente')
            return redirect(url_for('login'))
        else:
            flash('Respuesta incorrecta')
    return render_template('recuperar.html', pregunta=pregunta_secreta)



@app.route('/register', methods=['GET', 'POST']) #para registrarse
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        PreguntaSeguridad = request.form.get('PreguntaSeguridad') # Estas dos serviran para recuperar la contraseña en caso de que al usuario se le olvide
        RespuestaSeguridad = request.form.get('RespuestaSeguridad')
        password = request.form.get('password')  # Obtenemos la contraseña del formulario
        cursor = db.cursor()

        # Checkeamos que el  mail no se encuentre ya registrado
        query = "SELECT * FROM Usuarios WHERE correo = %s" # se lo preguntamos a la base de datos
        params = (email,)
        cursor.execute(query, params)
        user = cursor.fetchone()

        if user:
            cursor.close()
            flash('Este correo electrónico ya está registrado. Por favor, intenta con otro')
            return redirect(url_for('register')) # vuelve a login
           

        hashed_password = generate_password_hash(password)  # Hasheamos la contraseña
        query = "INSERT INTO Usuarios (nombre, correo, password,PreguntaSeguridad,RespuestaSeguridad) VALUES (%s, %s, %s,%s,%s)"
        params = (name, email, hashed_password,PreguntaSeguridad,RespuestaSeguridad)
        cursor.execute(query, params)
        db.commit()
        cursor.close()  # Cerramos el cursor para que no se rompa (?)
        return redirect(url_for('login'))
    return render_template('register.html', nombre="registrando")


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
    cursor.close()  
   # return f"Estás logueado, {NombreDelUsuario}. ¡Bienvenido!"  --> ignorar
    return redirect(url_for('home'))

@app.route('/logout') # Es para que el usurio se desloguee
def logout():
    logout_user()
    return redirect(url_for('home'))


  
    

'''
---------------------------------------------
------COMPROBACIONES Y PUESTA EN MARCHA------
---------------------------------------------
'''
print("Hola, esta aplicación web flask fue creada por Fabricio David Gallo")
if db.is_connected(): #Comprbación de conexión a mysql
    print("Conexión exitosa a la base de datos.")
else:
    print("No se pudo conectar a la base de datos.")

if __name__ == "__main__": #¿Nuestra objeto flask se instanció correctamente?
    app.run(debug=True)    # entonces  ejecutar en modo debuggin

