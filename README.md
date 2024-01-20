Hola soy Fabricio David Gallo y este es mi primer proyecto web (backend y frontend). La idea es un proyecto simple, una pagina de moocs (cursos virtuales gratis) inspirado tanto en Capacitate para el empleo en cuanto a lo que examenes y calificaciones, pero tambien en cuanto al IFMG en cuanto a la visualización de contenidos ... Pero en cambio, como lo mio no es tanto el diseño haré que sea lo más simple posible, priorizando funcionalidad y responsividad ante todo.

Tecnologías empleadas y o a utilizar: Flask y su motor de plantilllas Jinja2, Html y Css, Algún que otro adorno en JavaScript (intentaré utilizar lo menos posible), MySql para los datos (por razones obvios no la subiré), Boostrap (aunque no estoy seguro)...

INSTRUCCIONES POR SI QUERES RUNEAR EL PROYECTO (Y/O COPIARLO ;D):
 1-Necesitas MYSQL SERVER, y tener instalados Flask, mysql, bla bla (siempre que no te reconozca un comando, podes buscar de donde lo importa y poner pip install (nombre del paquete) y ya deberia funcionar) NOTA: Para que no andes renegando como yo, haz un par de pruebas de peticiones. Creeme, si lo tienes mal instalado no va a funcionar bien 
 2-Ahora, en Mysql Workbench (yo uso ese pero podés usar phpMyAdmin, supongo) realizamos las siguientes consultas: CREATE DATABASE APPBD;

USE APPBD;

CREATE TABLE Usuarios ( id INT AUTO_INCREMENT, nombre VARCHAR(255), correo VARCHAR(255), password VARCHAR(255),PreguntaSeguridad VARCHAR(255),RespuestaSeguridad VARCHAR(255) PRIMARY KEY (id) );

 3-Ejecutamos inn.py
 ¡Listo! 


4-Opcional, realizar una consulta en la base de datos USE APPBD; -----> Especificamos la base de datos SET SQL_SAFE_UPDATES = 1; --->Generalmente viene activado, para no hacer estupideces (?) SELECT * FROM Usuarios; ---> Nos da toda la tabla "Usuarios"

Nota: la contraseña no es la que metiste, esto se debe a que se guardan en forma de Hash (encriptada)

ERRORES QUE TUVE DURANTE EL DESARROLLO:

AttributeError AttributeError: 'NoneType' object has no attribute 'split'

Esto se debe a que un atributo en la base de datos es 'NULL'... mi consejo, no modificar la tabla fuera del sitio, a veces buscar donde está es complejo. Por lo que hacé un roolback.

