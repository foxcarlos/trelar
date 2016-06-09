#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'FoxCarlos'


import json
import bottle
from bottle.ext.websocket import GeventWebSocketServer
from static.python.datos import sql
from static.python.notificar import notificar
import time

# ---------------------------------------
# Ejemplo CRUD
# ---------------------------------------


@bottle.route('/restapi/<id>')
def raget(id):
    print('Entro al GET', id)
    model = {'model': 'Modelo'}
    return model


@bottle.post('/restapi')
def rapost():
    recibido = bottle.request.json
    print('Entro al POST', recibido)
    model = {'model': 'Modelo'}
    return model


@bottle.put('/restapi/<id>')
def raPUT(id):
    print('Entro al PUT', id)
    model = {'model': 'Modelo'}
    return model


@bottle.delete('/restapi/<id>')
def raDEL(id):
    print('Entro al DEL', id)
    model = {'model': 'Modelo'}
    return model

# ---------------------------------------
@bottle.route('/static/<filename:path>')
def static(filename):
    return bottle.static_file(filename, root='static/')


@bottle.route('/')
def index():
    # usuario = ''
    # bottle.response.set_cookie("account", usuario)
    # username = bottle.request.get_cookie("account")

    # print('usuario',username)
    return bottle.static_file("index.html", root='')

# bottle.debug(True)
bottle.run(host='0.0.0.0', port=8086, server=GeventWebSocketServer, reloader=True)
