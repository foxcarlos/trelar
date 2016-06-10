#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'FoxCarlos'


import json
import bottle
from bottle.ext.websocket import GeventWebSocketServer
# from static.python.datos import sql
# from static.python.notificar import notificar
# import time
from constants import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_TOKEN, TRELLO_TOKEN_SECRET
from trello import TrelloClient


client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_SECRET,
    token=TRELLO_TOKEN,
    token_secret=TRELLO_TOKEN_SECRET
)

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


@bottle.route('/tableros')
def getTableros():
    '''Metodo GET que permite listar todos
    los tableros, recibe un JSON con el filtro
    que se desea aplicar, Ej: closed, open y
    devolver una lista con varios objetos JSON
    con la informacio del id y nombre del tablero'''

    filtro = bottle.request.json

    filtroPasado = filtro
    tableros = client.list_boards(board_filter=filtroPasado)
    lista = []

    registros = [(tn.name, tn.id) for tn in tableros]
    for f in registros:
        campos = ['nombre_tablero', 'id_tablero']
        convertir = dict(zip(campos, f))
        lista.append(convertir)
    tablerosDevolver = json.dumps(lista)
    return tablerosDevolver


@bottle.route('/tableros/<id>')
def getTablero(id_tablero):
    '''Metodo GET que permite obtener un
    tableros por su Id'''

    tablero = client.get_board(id_tablero)

    return tablero

# bottle.debug(True)
bottle.run(host='0.0.0.0', port=8086, server=GeventWebSocketServer, reloader=True)
