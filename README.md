Hola soy Fabricio David Gallo y este es mi primer proyecto web (backend y frontend). La idea es un proyecto simple, una pagina de moocs (cursos virtuales gratis) inspirado tanto en Capacitate para el empleo en cuanto a lo que examenes y calificaciones, pero tambien en cuanto al IFMG en cuanto a la visualización de contenidos ... Pero en cambio, como lo mio no es tanto el diseño haré que sea lo más simple posible, priorizando funcionalidad y responsividad ante todo.

Tecnologías empleadas y o a utilizar: Flask y su motor de plantilllas Jinja2, Html y Css, Algún que otro adorno en JavaScript (intentaré utilizar lo menos posible), MySql para los datos (por razones obvios no la subiré), Boostrap (aunque no estoy seguro)...

INSTRUCCIONES POR SI QUERES RUNEAR EL PROYECTO (Y/O COPIARLO ;D):
 1-Necesitas MYSQL SERVER, y tener instalados Flask, mysql, bla bla (siempre que no te reconozca un comando, podes buscar de donde lo importa y poner pip install (nombre del paquete) y ya deberia funcionar) NOTA: Para que no andes renegando como yo, haz un par de pruebas de peticiones. Creeme, si lo tienes mal instalado no va a funcionar bien 
 2-Ahora, en Mysql Workbench (yo uso ese pero podés usar phpMyAdmin, supongo) realizamos las siguientes consultas: CREATE DATABASE APPBD;

CREATE TABLE Usuarios ( id INT AUTO_INCREMENT, nombre VARCHAR(255), correo VARCHAR(255), password VARCHAR(255),PreguntaSeguridad VARCHAR(255),RespuestaSeguridad VARCHAR(255), PRIMARY KEY (id) );

USE APPBD;

CREATE TABLE NotasExamenes ( IdNotas INT AUTO_INCREMENT, id int,  InglesA1 DOUBLE,TortasFritas DOUBLE,MVC  DOUBLE, FOREIGN KEY (id) REFERENCES Usuarios (id), PRIMARY KEY (IdNotas) );

DELIMITER $$
CREATE TRIGGER llenar_notas AFTER INSERT ON Usuarios
FOR EACH ROW
BEGIN
  INSERT INTO NotasExamenes (id, InglesA1, TortasFritas, MVC)
  VALUES (new.id, 0, 0, 0);
END $$
DELIMITER ;

USE APPBD;
SELECT *
FROM Usuarios
INNER JOIN NotasExamenes
ON Usuarios.id = NotasExamenes.id;
 3-Ejecutamos inn.py
 ¡Listo! 


4-Opcional, realizar una consulta en la base de datos USE APPBD; -----> Especificamos la base de datos SET SQL_SAFE_UPDATES = 1; --->Generalmente viene activado, para no hacer estupideces (?) SELECT * FROM Usuarios; ---> Nos da toda la tabla "Usuarios"

Nota: la contraseña no es la que metiste, esto se debe a que se guardan en forma de Hash (encriptada)

ERRORES QUE TUVE DURANTE EL DESARROLLO:

AttributeError AttributeError: 'NoneType' object has no attribute 'split'

Esto se debe a que un atributo en la base de datos es 'NULL'... mi consejo, no modificar la tabla fuera del sitio, a veces buscar donde está es complejo. Por lo que hacé un roolback.

COMO AÑADIR UN CURSO:
1)- Agregamos  el  nombre del nuevo curso en nuestra base de datos, por ej:
ALTER TABLE NotasExamenes
ADD COLUMN NOMBREDELNUEVOCURSO DOUBLE DEFAULT 0;

2)- agregamos la ruta
@app.route('/Curso') 
def  Curso():
    if current_user.is_authenticated:
        try:       #este control de  errores es por si la sesión del usuario ha exppirado o intenta ingresar al curso sin pasar por login
            cursor = db.cursor()
            query = "SELECT ADD COLUMN NOMBREDELNUEVOCURSO INT DEFAULT 0;
            FROM NotasExamenes WHERE id = %s"
            params = (idUsuario,)
            cursor.execute(query, params)
            NotaCurso = cursor.fetchone()[0]
            results = cursor.fetchall()
            cursor.close()  
            return render_template('BaseCursos.html',ExamenCurso="InglesA1Examen", NotaCurso=NotaCurso, nombre=NombreDelUsuario,NombreDelCurso="Inglés A1", ClasesDelCurso=["Bienvenida","Aula 1","Aula2","Aula3","Aula 4"],Aula0= {'Google': 'https://www.google.com', 'Bing': 'https://www.bing.com'},Aula1={},Aula2={},Aula3={},Aula4={},Aula5={},Aula6={},Aula7={},Aula8={},Aula9={},Aula10={})
        except NameError:
         logout_user()
         return redirect(url_for('home'))    
    else:
        return redirect(url_for('home'))
EXPLICACION:  la lista ClasesDelCurso va guardando  todos los titulos de nuestras aulas; cada aula tiene su contenido en un diccionario: donde la clave es el texto en pantalla y el valor el link a dicho recurso.