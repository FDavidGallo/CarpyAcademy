# Impor itar las librerías necesarias
from PILmport Image, ImageDraw, ImageFont


# Abrir la imagen de fondo del certificado
imagen = Image.open("c:\\Users\\Usuario\\Desktop\\proyectos\\Palo paje Tech\\CarpyAcademy\\static\\fondo.jpg")

# Crear un objeto para dibujar sobre la imagen
dibujar = ImageDraw.Draw(imagen)

# Especificar el nombre del participante
nombre = "Juan Pérez"+" aprobó el curso "+"Haciendo tortas fritas"

# Especificar la fuente y el color del texto
fuente = ImageFont.truetype("arial.ttf", 44)
color = (234, 165, 46)

# Calcular la posición del texto centrado en la imagen
ancho, alto = imagen.size
ancho_texto = dibujar.textlength(nombre, font=fuente)
alto_texto = fuente.size

x = (ancho - ancho_texto) // (4.5)
y = (alto - alto_texto) // (2.12)

# Dibujar el texto sobre la imagen
dibujar.text((x, y), nombre, font=fuente, fill=color)
nombre="Federación, 1/2/24"

x = (ancho - ancho_texto) // (0.55)
y = (alto - alto_texto) // (1.02)
dibujar.text((x, y), nombre, font=fuente, fill=color)
# Guardar la imagen modificada en formato PDF
imagen.save("certificado.pdf")
