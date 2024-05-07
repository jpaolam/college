#Lo que esto es importar la plantilla html
#con render_template
from flask import Flask
from flask import render_template, request, redirect
from flaskext.mysql import MySQL

#se crea la aplicación
app = Flask(__name__)
mysql= MySQL()

app.config['MYSQL_DATABASE_HOST']='localhost'
app.config['MYSQL_DATABASE_USER']='root'
app.config['MYSQL_DATABASE_PASSWORD']=''
app.config['MYSQL_DATABASE_DB']='sitio'
#inicializar
mysql.init_app(app)

#Capturamos lo que el usuario pondra en el navegador
@app.route('/')
#Cuando el usuario acceda al servidor y/o ruta
# va a buscar ese index. html
def inicio():
    #se hace una ruta de acceso y se renderiza
    return render_template('site/index.html')

@app.route('/libros')
def libros():
    return render_template('site/libros.html')

@app.route('/nosotros')
def nosotros():
    return render_template('site/nosotros.html')

@app.route('/admin/')
def admin_index():
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():
    #conexion
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    #recuperar todo
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template('admin/libros.html', libros=libros)

#recepcionan los datos
@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    #se va a recolectar
    _nombre=request.form['txtNombre']
    _url=request.form['txtDescarga']
    _archivo=request.files['imagen']

    sql="INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s, %s, %s);"
    datos=(_nombre,_archivo.filename,_url)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute(sql,datos)
    conexion.commit()

    print(_nombre)
    print(_url)
    print(_archivo)

    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    #se va a recolectar
    _id=request.form['txtID']
    print(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros` WHERE id=%s", (_id))
    #recuperar todo
    libro=cursor.fetchall()
    conexion.commit()
    print(libro)

    #BORRAR
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("DELETE FROM `libros` WHERE id=%s", (_id))
    conexion.commit()

    return redirect('/admin/libros')

#Se consulta si la app está lista y se hace en un modo debug
#para que cuando actualicemos el index ese se actualice
if __name__ == '__main__' :
    app.run(debug=True)