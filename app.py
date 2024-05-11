import os
from flask import Flask, render_template, request, redirect, session
from config.db import Database
from models.libros import LibrosModel
from flask import send_from_directory #para obtener info de la imagen

app = Flask(__name__)
app.secret_key = "develoteca"

db = Database(app)
libros_model = LibrosModel(db)

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
    return send_from_directory(os.path.join('src/img/'),imagen)

@app.route('/libros')
def libros():
    libros= libros_model.obtener_libros()

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

    libros= libros_model.obtener_libros()
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

    libros_model.guardar_libro(_nombre, _url, _archivo)
    return redirect('/admin/libros')

@app.route('/admin/libros/borrar', methods=['POST'])
def admin_libros_borrar():
    if 'login' not in session:
        return redirect('/admin/login')
    
    libro_id = request.form['txtID']
    libros_model.borrar_libro(libro_id)
    return redirect('/admin/libros')

#Se consulta si la app está lista y se hace en un modo debug
#para que cuando actualicemos el index ese se actualice
if __name__ == '__main__' :
    app.run(debug=True)