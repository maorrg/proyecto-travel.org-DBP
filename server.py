from flask import Flask,render_template, request, session, Response, redirect
from database import connector
from model import entities
import datetime
import json
import time
import os
from flask_session import Session


db = connector.Manager()
engine = db.createEngine()
sess = Session()


app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/static/<content>')
def static_content(content):
    return render_template(content)


#Login con metodo post
@app.route('/login' , methods =['POST']) #Como se puede utilizar mas de un metodo, se recibibe un arreglo
def login():
    usuario = request.form['usuario']
    contrasena = request.form['contrasena']

    db_session = db.getSession(engine)

    viajero = db_session.query(entities.Viajero).filter(
        entities.Viajero.usuario == usuario
    ).filter(
    entities.Viajero.contrasena == contrasena
    ).first()

    if viajero != None:
        session['usuario'] = usuario
        session['logged_user'] = viajero.id
        return render_template('calendar.html')
    else:
        return render_template('recuperar.html')


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

@app.route('/registrar' , methods =['POST'])
def registrar():

    #c =  json.loads(request.form['values'])
    c = json.loads(request.data)
    viajero = entities.Viajero(
        nombre=c['nombre'],
        apellido = c['apellido'],
        correo = c['correo'],
        usuario = c['usuario'],
        contrasena = c['contrasena'],
        edad = c['edad'],
        pais = c['pais']
    )

    user = c['usuario']

    session = db.getSession(engine)

    trip = session.query(entities.Viajero).filter(
        entities.Viajero.usuario == user
    ).first()


    if trip != None:
        message = { 'status': 404, 'message': 'Already exist'}
        return Response(json.dumps(message), status=404, mimetype='application/json')


    session.add(viajero)
    session.commit()


    message = { 'status': 200, 'message': 'Register'}
    return Response(json.dumps(message), status=200, mimetype='application/json')




@app.route('/recuperar' , methods =['POST'])
def recuperar_cuenta():
    usuario = request.form['usuario']
    correo = request.form['correo']
    contrasena1 = request.form['contrasena1']
    contrasena2 = request.form['contrasena2']

    session = db.getSession(engine)
    viajero = session.query(entities.Viajero).filter(entities.Viajero.usuario == usuario).first()
    c = json.loads(request.data)
    c['contrasena'] = contrasena1
    session.add(viajero)
    session.commit()
    return 'Cambiar contrasena'


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



@app.route('/experiencias', methods = ['POST'])
def create_experiencia():
    #c =  json.loads(request.form['values'])
    c = json.loads(request.data)
    experiencia = entities.Experiencia(
        titulo=c['titulo'],
        descripcion = c['descripcion'],
        precio = c['precio'],
        calificacion = c['calificacion'],
        create_on=datetime.datetime(2000,2,2)
    )
    session = db.getSession(engine)
    session.add(experiencia)
    session.commit()
    message = { 'status': 200, 'message': 'Experiencia creada'}
    return Response(json.dumps(message), status=200, mimetype='application/json')


@app.route('/experiencias', methods = ['GET'])
def get_experienciasDevExtream():
    sessionc = db.getSession(engine)
    dbResponse = sessionc.query(entities.Experiencia)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')

@app.route('/experiencias/<id>', methods = ['GET'])
def get_experienciaid(id):
    db_session = db.getSession(engine)
    experiencias = db_session.query(entities.Experiencia).filter(entities.Experiencia.id == id)
    for experiencia in experiencias:
        js = json.dumps(experiencia, cls=connector.AlchemyEncoder)
        return  Response(js, status=200, mimetype='application/json')

    message = { 'status': 404, 'message': 'Not Found'}
    return Response(message, status=404, mimetype='application/json')


@app.route('/experiencias', methods = ['PUT'])
def update_experiencia():
    session = db.getSession(engine)
    id = request.form['key']
    experiencia = session.query(entities.Experiencia).filter(entities.Experiencia.id == id).first()
    c = json.loads(request.form['values'])
    for key in c.keys():
        setattr(experiencia, key, c[key])
    session.add(experiencia)
    session.commit()
    return 'Updated Experiencia'

@app.route('/experiencias', methods = ['DELETE'])
def delete_experiencia():
    id = request.form['key']
    session = db.getSession(engine)
    experiencia = session.query(entities.Experiencia).filter(entities.Experiencia.id == id).one()
    session.delete(experiencia)
    session.commit()
    return "Deleted Experiencia"

@app.route('/experiencia/<id>', methods = ['DELETE'])
def delete_experiencia_id(id):
    session = db.getSession(engine)
    experiencia = session.query(entities.Experiencia).filter(entities.Experiencia.id == id).one()
    session.delete(experiencia)
    session.commit()
    return "Deleted Experiencia"


@app.route('/itinerario', methods = ['POST'])
def agregar_experiencia():
    c = json.loads(request.data)
    itinerario = entities.Itinerario(
        id_experiencia=c['id_experiencia'],
        id_viajero = c['id_viajero'],
        id_guia = c['id_guia']
    )
    session = db.getSession(engine)
    session.add(itinerario)
    session.commit()
    return 'Created Itinerario'


@app.route('/itinerarioAdd', methods = ['POST'])
def agregar_experiencia_json():
    c = json.loads(request.data)
    itinerario = entities.Itinerario(
        id_experiencia=c['id_experiencia'],
        id_viajero = c['id_viajero'],
        id_guia = c['id_guia']
    )

    id_itne = c['id_experiencia']
    id_viaj = c['id_viajero']

    session = db.getSession(engine)

    experiencia = session.query(entities.Itinerario).filter(
        entities.Itinerario.id_experiencia == id_itne
    ).filter(entities.Itinerario.id_viajero == id_viaj).first()

    if experiencia == None:
        session.add(itinerario)
        session.commit()
        message = { 'status': 200, 'message': 'Agregado'}
        return Response(json.dumps(message), status=200, mimetype='application/json')
    else:
        message = { 'status':400,'message': 'No agregado'}
        return Response(json.dumps(message),status=404, mimetype='application/json')


@app.route('/itinerario', methods = ['GET'])
def get_itinerario():
    sessionc = db.getSession(engine)
    dbResponse = sessionc.query(entities.Itinerario)
    data = dbResponse[:]
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/itinerario/<id_viajero>', methods = ['GET'])
def get_experiencias_viajero(id_viajero):
    db_session = db.getSession(engine)
    experiencias = db_session.query(entities.Itinerario).filter(
        entities.Itinerario.id_viajero == id_viajero)

    data = []
    for experiencia in experiencias:
        data.append(experiencia)
    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/itinerarioDatos/<id_viajero>', methods = ['GET'])
def get_experiencias_viajero2(id_viajero):
    db_session = db.getSession(engine)
    experiencias = db_session.query(entities.Itinerario).filter(
        entities.Itinerario.id_viajero == id_viajero)

    datos = db_session.query(entities.Experiencia)

    data = []
    for experiencia in experiencias:
        for dato in datos:
            if(experiencia.id_experiencia == dato.id):
                data.append(dato)

    return Response(json.dumps(data, cls=connector.AlchemyEncoder), mimetype='application/json')


@app.route('/deleteExperiencia/<id_exp>/<id_user>', methods = ['DELETE'])
def borrar_experiencia_del_itinerario(id_exp,id_user):
    session = db.getSession(engine)
    experiencia = session.query(entities.Itinerario).filter(entities.Itinerario.id_experiencia == id_exp).filter(entities.Itinerario.id_viajero == id_user).one()
    session.delete(experiencia)
    session.commit()
    message = { 'status': 200, 'message': 'Borrado'}
    return Response(json.dumps(message), status=200, mimetype='application/json')


@app.route('/authenticate', methods = ['POST'])
def authenticate():
    #Get data form request
    #time.sleep(3)
    c = json.loads(request.data)
    usuario=c['usuario']
    contrasena = c['contrasena']

    db_session = db.getSession(engine)

    viajero = db_session.query(entities.Viajero).filter(
        entities.Viajero.usuario == usuario
    ).filter(
    entities.Viajero.contrasena == contrasena
    ).first()

    if viajero != None:
        message = {'message':'Authorized','user_id':viajero.id,'username':viajero.usuario,'nombre':viajero.nombre}
        return Response(json.dumps(message), status=200,mimetype='application/json')
    else:
        message = {'message':'Unauthorized'}
        return Response(json.dumps(message), status=401,mimetype='application/json')


@app.route('/current', methods = ['GET'])
def current_user():
    if 'usuario' in session:
        db_session = db.getSession(engine)
        viajero = db_session.query(entities.Viajero).filter(entities.Viajero.id == session['logged_user']).first()
        return Response(json.dumps(viajero,cls=connector.AlchemyEncoder),mimetype='application/json')
    else:
        return render_template('index.html')

@app.route('/logout', methods = ['GET'])
def logout():
    session.clear()
    return render_template('index.html')



if __name__ == '__main__':
    app.run(debug=True,port=8000, threaded=True, host=('127.0.0.1'))
