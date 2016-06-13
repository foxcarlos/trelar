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


@bottle.route('/listas')
def getListas():
    '''Parametros Recibidos 1: json con el Id del Tablero
    Metodo GET que permite obtener todas
    las Listas asociadas a un tablero y devolver 
    informacion Ej:
    - tableroNombre
    - listaId
    - listaNombre
    - cantidadTarjetas en cada lista
    '''
    tableroRecibido = bottle.request.json
    tableroId = tableroRecibido['id']
    miTablero = client.get_board(tableroId)
    
    listasDevolver = []
    campos = ['tableroNombre', 'listaId', 'listaNombre', 'cantidadTarjetas']
    
    # miTablero.all_lists() busca listas abiertas y cerradas
    for lista in miTablero.open_lists():
        infLista = ( lista.board.name, lista.id, lista.name, lista.cardsCnt() )
        listasDevolver.append( json.dumps(dict( zip(campos, infLista) )) )
    print(listasDevolver)
    return listasDevolver

@bottle.route('/lista/<id>')
def getLista(id_lista):
    ''' 
     Metodo GET que permite buscar una lista
     por su ID pasado como parametro, devuelve
    - tableroNombre
    - listaId
    - listaNombre
    - cantidadTarjetas en cada lista
    '''
    tableroRecibido = bottle.request.json
    tableroId = tableroRecibido['id']
    miTablero = client.get_board('57581f7d6a945e2f6630a793')  # tableroId
    lista = tablero.get_list(id_lista)
    
    campos = ['tableroNombre', 'listaId', 'listaNombre', 'cantidadTarjetas']
    infLista = ( lista.board.name, lista.id, lista.name, lista.cardsCnt() )
    listaDevolver = json.dumps(dict( zip(campos, infLista) ))
    return listaDevolver


@bottle.route('/tarjetas')
def getTarjetas():
    ''' 
     Metodo GET que permite buscar todas las tajetas
     pereteneciente a una lista.
     
     Recibe: un JSON con la siguiente informacion:
     {tablero_id:'', lista_id: ''}
     
     Devuelve: un JSON con:
     tableroNombre', 'listaId', 'listaNombre', 'Todas las Tarjetas'
    '''
    
    jsonRecibido = bottle.request.json
    tableroId = jsonRecibido['tablero_id']
    listaId = jsonRecibido['lista_id']
    
    miTablero = client.get_board(tableroId)
    miLista = tablero.get_list(listaId)
    tarjetas = miLista.list_cards()
    # listaDeTarjetas = [ json.dumps( dict(zip( ['id', 'nombre_tarjeta'],(f.id, f.name))) ) for f in tarjetas]
    listaDeTarjetas = [ dict(zip( ['id', 'nombre_tarjeta'],(f.id, f.name))) for f in tarjetas]
    campos = ['tableroNombre', 'listaId', 'listaNombre', 'Tarjetas']
    infLista = ( miLista.board.name, miLista.id, miLista.name, listaDeTarjetas )
    listaDevolver = json.dumps(dict( zip(campos, infLista) ))
    return listaDevolver
    
    
@bottle.route('/tarjeta/<id>')
def getTarjeta(id_tarjeta):
    '''Metodo que permite obtener una 
    tarjeta basada en su ID pasado 
    como parametro'''
    
    tarjeta = client.get_card(id_tarjeta)
    
    # Propiedades de la tarjeta
    tarjeta.get_list().name  # nombre de la lista donde esta la tarjeta
    
    tarjeta.listCardMove_date()  #Litas las cuales a pertenecido esta tarjeta
    tarjeta.create_date
    tarjeta.dateLastActivity
    tarjeta.get_comments()
    tarjeta.id
    tarjeta.idLabels
    tarjeta.labels  # Lista con todas las propiedades de la etiqueta
    # Ejemplo:
    for l in tarjeta.labels:
        l.id, l.name, l.color
        
    tarjeta.idList  # parece ser lo mismo que -> tarjeta.list_id
    tarjeta.latestCardMove_date  #Fecha de la ultima vez que se movio la tarjeta
    tarjeta.list_labels  # Lista de etiquetas, una tarjeta puede contener varias labels
    # Ejemplo:
    for l in tarjeta.list_labels:
        l.id, l.name, l.color
    tarjeta.member_ids
    tarjeta.name
    
# bottle.debug(True)
bottle.run(host='0.0.0.0', port=8086, server=GeventWebSocketServer, reloader=True)
