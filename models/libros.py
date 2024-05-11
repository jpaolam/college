import os
from datetime import datetime

class LibrosModel:
    def __init__(self, db):
        self.db = db

    def obtener_libros(self):
        conexion = self.db.connect()
        cursor = conexion.cursor()
        cursor.execute("SELECT * FROM `libros`")
        libros = cursor.fetchall()
        conexion.commit()
        return libros

    #GUARDAR
    def guardar_libro(self, nombre, url, archivo):
        tiempo = datetime.now()
        hora_actual = tiempo.strftime('%Y%H%M%S')

        nuevo_nombre = hora_actual + "_" + archivo.filename
        archivo.save("src/img/" + nuevo_nombre)

        sql = "INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s, %s, %s);"
        datos = (nombre, nuevo_nombre, url)

        conexion = self.db.connect()
        cursor = conexion.cursor()
        cursor.execute(sql, datos)
        conexion.commit()
    
    def borrar_libro(self, libro_id):
        conexion = self.db.connect()
        cursor = conexion.cursor()

        cursor.execute("SELECT imagen FROM `libros` WHERE id=%s", (libro_id))
        libro = cursor.fetchall()

        if os.path.exists("src/img/" + str(libro[0][0])):
            os.unlink("src/img/" + str(libro[0][0]))

        cursor.execute("DELETE FROM `libros` WHERE id=%s", (libro_id))
        conexion.commit()