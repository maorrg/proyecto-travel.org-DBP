from sqlalchemy import Column, Integer, String, Sequence, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from database import connector
import datetime


class Viajero(connector.Manager.Base):
    __tablename__ = 'viajeros'
    id = Column(Integer, Sequence('viajero_id_seq'), primary_key=True)
    nombre = Column(String(50))
    apellido = Column(String(50))
    correo = Column(String(40))
    usuario = Column(String(12))
    contrasena = Column(String(12))
    edad = Column(Integer)
    pais = Column(String(25))


class Guia(connector.Manager.Base):
    __tablename__ = 'guias'
    id = Column(Integer, Sequence('guias_id_seq'), primary_key=True)
    nombre = Column(String(50))
    correo = Column(String(40))
    telefono = Column(String(15))
    usuario = Column(String(12))
    contrasena = Column(String(12))
    pais = Column(String(25))


class Experiencia(connector.Manager.Base):
    __tablename__ = 'experiencias'
    id = Column(Integer, Sequence('viajero_id_seq'), primary_key=True)
    titulo = Column(String(50))
    descripcion = Column(String(500))
    precio = Column(Integer)
    fecha = Column(DateTime())
    calificacion = Column(Integer)
    guia_id = Column(Integer, ForeignKey('guias.id'))
    create_on = Column(DateTime,default=datetime.datetime.now())


class Comentario(connector.Manager.Base):
    __tablename__ = 'comentarios'
    id = Column(Integer, Sequence('comentario_id_seq'), primary_key=True)
    titulo = Column(String(50))
    descripcion = Column(String(500))
    viajero_id = Column(Integer, ForeignKey('viajeros.id'))
    guia_id = Column(Integer, ForeignKey('guias.id'))


class Itinerario(connector.Manager.Base):
    __tablename__ = 'intinerarios'
    id = Column(Integer, Sequence('comentario_id_seq'), primary_key=True)
    id_experiencia = Column(Integer)
    id_viajero = Column(Integer)
    id_guia = Column(Integer)
    fecha_inicio = Column(DateTime())
    fecha_fin = Column(DateTime())