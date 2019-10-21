from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import datetime
import json
import time

db = connector.Manager()
engine = db.createEngine()

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


#Login con metodo post
@app.route('/login' , methods =['POST']) #Como se puede utilizar mas de un metodo, se recibibe un arreglo
def login():
    #El metodo crea un diccionario en donde la clave es el nombre del input y el valor es el contenido ingresado
    username = request.form['user'] #Le asignamos a la variable username lo ingresado en el formulario insertado en el html
    password = request.form['password']

    db_session = db.getSession(engine)

    user = db_session.query(entities.User).filter(
        entities.User.username == username
    ).filter(
    entities.User.password == password
    ).first()

    if user != None:
        session['usuario'] = username
        session['logged_user'] = user.id
        return render_template('chat.html')
    else:
        return "Sorry "+username+" no esta en la base de datos"


@app.route('/viajeros', methods = ['POST'])
def create_viajeroDevExtream():
    c =  json.loads(request.form['values'])
    #c = json.loads(request.data)
    viajero = entities.Viajero(
        nombre=c['nombre'],
        apellido=c['apellido'],
        correo=c['correo'],
        usuario=c['usuario'],
        contrasena=c['contrasena'],
        edad = c['edad'],
        pais = c['pais']
    )
    session = db.getSession(engine)
    session.add(viajero)
    session.commit()
    return 'Created Viajero'

@app.route('/viajeros/<id>', methods = ['GET'])
def get_viajero(id):
    db_session = db.getSession(engine)
    viajeros = db_session.query(entities.User).filter(entities.Viajero.id == id)
    for viajero in viajeros:
        js = json.dumps(viajero, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')


@app.route('/viajeros', methods = ['GET'])
def get_viajeros():
    session = db.getSession(engine)
    dbResponse = session.query(entities.Viajero)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/viajeros/<id>', methods = ['PUT'])
def update_viajero(id):
    session = db.getSession(engine)
    #id = request.form['key']
    viajero = session.query(entities.Viajero).filter(entities.Viajero.id == id).first()
    #c = json.loads(request.form['values'])
    c = json.loads(request.data) #Cambio para no usar Json
    for key in c.keys():
        setattr(viajero, key, c[key])
    session.add(viajero)
    session.commit()
    return 'Updated Viajero'

@app.route('/viajeros', methods = ['PUT'])
def update_viajeroDevExtream():
    session = db.getSession(engine)
    id = request.form['key']
    viajero = session.query(entities.Viajero).filter(entities.Viajero.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(viajero, key, c[key])
    session.add(viajero)
    session.commit()
    return 'Updated Viajero'

@app.route('/viajeros/<id>', methods = ['DELETE'])
def delete_viajero(id):
    #id = request.form['key']
    session = db.getSession(engine)
    viajero = session.query(entities.Viajero).filter(entities.Viajero.id == id).one()
    session.delete(viajero)
    session.commit()
    return "Deleted Viajero"

@app.route('/viajeros', methods = ['DELETE'])
def delete_viajeroDevExtream():
    id = request.form['key']
    session = db.getSession(engine)
    viajero = session.query(entities.Viajero).filter(entities.Viajero.id == id).one()
    session.delete(viajero)
    session.commit()
    return "Deleted Viajero"


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    #Get data form request
    time.sleep(3)
    message = json.loads(request.data)
    username = message['username']
    password = message['password']

    # Look in database
    db_session = db.getSession(engine)

    try:
        user = db_session.query(entities.User
            ).filter(entities.User.username==username
            ).filter(entities.User.password==password
            ).one()
        session['logged_user'] = user.id
        message = {'message':'Authorized'}
        return Response(message, status=200,mimetype='application/json')
    except Exception:
        message = {'message':'Unauthorized'}
        return Response(message, status=401,mimetype='application/json')


@app.route('/current', methods = ['GET'])
def current_user():
    db_session = db.getSession(engine)
    user = db_session.query(entities.User).filter(entities.User.id == session['logged_user']).first()
    return Response(json.dumps(user,cls=connector.AlchemyEncoder),mimetype='application/json')

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return render_template('login.html')



if __name__ == '__main__':
    app.secret_key = ".."
    app.run(debug=True,port=8000, threaded=True, host=('127.0.0.1'))