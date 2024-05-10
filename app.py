#Lo que esto es importar la plantilla html
#con render_template
import os
from flask import Flask
from flask import render_template, request, redirect, session
from flaskext.mysql import MySQL
from datetime import datetime
from flask import send_from_directory #para obtener info de la imagen

#se crea la aplicación
app = Flask(__name__)
app.secret_key="develoteca"
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

@app.route('/img/<imagen>')
def imagenes(imagen):
    print(imagen)
    return send_from_directory(os.path.join('templates/site/img'),imagen)

@app.route('/libros')
def libros():
    #conexion
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    #recuperar todo
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)

    return render_template('site/libros.html', libros=libros)
@app.route('/nosotros')
def nosotros():
    return render_template('site/nosotros.html')

@app.route('/admin/')
def admin_index():
    #pregunta si existe la session
    if not 'login' in session:
        return redirect('/admin/login')
    return render_template('admin/index.html')

@app.route('/admin/login')
def admin_login():
    return render_template('admin/login.html')

@app.route('/admin/login', methods=['POST'])
def admin_login_post():
    _usuario=request.form['txtUsuario']
    _password=request.form['txtPassword']
    print(_usuario)
    print(_password)
    #se valida la informacion
    if _usuario=="admin" and _password=="123":
        session["login"]=True #si ingreso el usuario
        session["usuario"]="Administrador"
        return redirect("/admin")
    return render_template('admin/login.html')

@app.route('/admin/libros')
def admin_libros():
    if not 'login' in session:
        return redirect('/admin/login')

    #conexion
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT * FROM `libros`")
    #recuperar todo
    libros=cursor.fetchall()
    conexion.commit()
    print(libros)
    return render_template('admin/libros.html', libros=libros)

@app.route('/admin/cerrar')
def admin_login_cerrar():
    session.clear()
    return redirect('/admin/login')

#recepcionan los datos
@app.route('/admin/libros/guardar', methods=['POST'])
def admin_libros_guardar():
    if not 'login' in session:
        return redirect('/admin/login')
    #se va a recolectar
    _nombre=request.form['txtNombre']
    _url=request.form['txtDescarga']
    _archivo=request.files['imagen']

    tiempo = datetime.now()
    #String de hora actual
    horaActual=tiempo.strftime('%Y%H%M%S')

    if _archivo.filename!="":
        nuevoNombre=horaActual+"_"+_archivo.filename
        _archivo.save("templates/site/img/"+nuevoNombre)

    sql="INSERT INTO `libros` (`id`, `nombre`, `imagen`, `url`) VALUES (NULL, %s, %s, %s);"
    datos=(_nombre,nuevoNombre,_url)
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
    if not 'login' in session:
        return redirect('/admin/login')
    #se va a recolectar
    _id=request.form['txtID']
    print(_id)
    conexion=mysql.connect()
    cursor=conexion.cursor()
    cursor.execute("SELECT imagen FROM `libros` WHERE id=%s", (_id))
    #recuperar todo
    libro=cursor.fetchall()
    conexion.commit()
    print(libro)

    if os.path.exists("templates/site/img/"+str(libro[0][0])):
        os.unlink("templates/site/img/"+str(libro[0][0]))

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