#!/usr/bin/python
# -*- coding: utf-8 -*-
__author__ = 'FoxCarlos'


import json
import bottle
from bottle.ext.websocket import GeventWebSocketServer
# from constants import TRELLO_API_KEY, TRELLO_API_SECRET, TRELLO_TOKEN, TRELLO_TOKEN_SECRET
from trello import TrelloClient
import datetime


TRELLO_API_KEY = '05571f7ecf0d9177c020b9ab3495aaac'
TRELLO_API_SECRET = '03a65f30fb4946c03cba7998327f7e10025493f7e036408d6efbcdbd63fc66f5'
TRELLO_TOKEN = '1316a12594687b611d0c631896b9b421436bd955d0d376162521c5ed267155d8'
TRELLO_TOKEN_SECRET = '5d0d9ac40b148703315c54e64b7998d2'

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
    return bottle.static_file("index.html", root='')


@bottle.route('/tableros')
def getTableros():
    '''Metodo GET que permite listar todos
    los tableros.
    
    Recibe: Un JSON con el filtro
    que se desea aplicar, Ej: closed, open y
    
    Devuelve: Una lista con varios objetos JSON
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
    tableroId = tableroRecibido['tablero_id']
    miTablero = client.get_board(tableroId)
    
    listasDevolver = []
    campos = ['tableroNombre', 'listaId', 'listaNombre', 'cantidadTarjetas']
    
    # miTablero.all_lists() busca listas abiertas y cerradas
    for lista in miTablero.open_lists():
        infLista = ( lista.board.name, lista.id, lista.name, lista.cardsCnt() )
        listasDevolver.append( json.dumps(dict( zip(campos, infLista) )) )
    print(listasDevolver)
    return listasDevolver

@bottle.route('/lista/<id_lista>')
def getLista(id_lista):
    ''' 
     Metodo GET que permite buscar una lista
     por su ID pasado como parametro, devuelve
    - tableroNombre
    - listaId
    - listaNombre
    - cantidadTarjetas en cada lista
    '''
    
    # Se coloco temporal el id del trablero como constante,
    # realmente debe llegar mediante un ajax como parametro json
    # pero para prueba se coloca asi
    
    tableroRecibido = {'id': '57581f7d6a945e2f6630a793'}  # bottle.request.json
    tableroId = tableroRecibido['id']
    miTablero = client.get_board('57581f7d6a945e2f6630a793')  # tableroId
    lista = miTablero.get_list(id_lista)
    
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
    miLista = miTablero.get_list(listaId)
    tarjetas = miLista.list_cards()
    
    listaDeTarjetas = [ dict(zip( ['id', 'nombre_tarjeta'],(f.id, f.name))) for f in tarjetas]
    campos = ['tableroNombre', 'listaId', 'listaNombre', 'Tarjetas']
    infLista = ( miLista.board.name, miLista.id, miLista.name, listaDeTarjetas )
    listaDevolver = json.dumps(dict( zip(campos, infLista) ))
    return listaDevolver

    
@bottle.route('/tarjetasTerminadas/<id_tarjeta>')
def getBuscarMovTarjeta(id_tarjeta):
    '''Metodo que permite obtener los movimientos
    de una  tarjeta (listaInical, listaFinal, fecha)
    basada en su ID pasado como parametro'''
    
    tarjeta = client.get_card(id_tarjeta)
    listaFechaMovTarjeta = [ dict(zip( ['inicio' ,'fin' ,'fecha'] ,(f[0], f[1], f[2]) )) \
    for f in tarjeta.listCardMove_date()]
    
    for j in listaFechaMovTarjeta:
        if j['inicio'] == u'En Desarrollo':
            fechaInicial = j['fecha']
        if j['fin'] == u'Terminado':
            fechaFinal = j['fecha']
    
    fechaCreacion = tarjeta.create_date
    diferencia = fechaFinal - fechaInicial
    tiempoEnDias = diferencia.days
    tiempoEnSeg = diferencia.seconds / 3600
    # model = {'Nombre Tarjeta': tarjeta.name, 'dias': tiempoEnDias, 'horas': tiempoEnSeg}
    model = {'Nombre Tarjeta': tarjeta.name, 'dias': tiempoEnDias}
    return model
    

@bottle.route('/tarjetasEnBacklog/<id_tarjeta>')
def getTarjetaEnBacklog(id_tarjeta):
    '''Metodo que permite obtener los movimientos
    de una  tarjeta (listaInical, listaFinal, fecha)
    basada en su ID pasado como parametro'''
    
    tarjeta = client.get_card(id_tarjeta)
    
    # Si la Tarjeta no se ha movido
    if not tarjeta.listCardMove_date():
        fechaCreacion = tarjeta.create_date.date()
        fechaTocadaUltimaVez = tarjeta.dateLastActivity.date()
        
        hoy = datetime.date.today()
        diferencia = hoy - fechaCreacion
        tiempoEnDias = diferencia.days
        
        diferTocadaUltVez = hoy - fechaTocadaUltimaVez
        tiempoEnDias2 = diferTocadaUltVez.days
        model = {'Nombre Tarjeta': tarjeta.name, 'diasCreada': tiempoEnDias, 'DiasDeTocadaLaUltimaVez': tiempoEnDias2}
    return model
    

@bottle.route('/tarjetasLeadTime/<id_tarjeta>')
def getBuscarTarjetasLeadTime(id_tarjeta):
    '''Metodo que permite obtener los movimientos
    de una  tarjeta (listaInical, listaFinal, fecha)
    basada en su ID pasado como parametro'''
    
    tarjeta = client.get_card(id_tarjeta)
    listaFechaMovTarjeta = [ dict(zip( ['inicio' ,'fin' ,'fecha'] ,(f[0], f[1], f[2]) )) \
    for f in tarjeta.listCardMove_date()]
    
    for j in listaFechaMovTarjeta:
        if j['inicio'] == u'Ideas (backlog)':
            fechaInicial = j['fecha']
        if j['fin'] == u'Terminado':
            fechaFinal = j['fecha']
    
    print(fechaFinal)
    fechaCreacion = tarjeta.create_date
    diferencia = fechaFinal - fechaInicial
    tiempoEnDias = diferencia.days
    tiempoEnSeg = diferencia.seconds / 3600
    # model = {'Nombre Tarjeta': tarjeta.name, 'dias': tiempoEnDias, 'horas': tiempoEnSeg}
    model = {'Nombre Tarjeta': tarjeta.name, 'dias': tiempoEnDias}
    return model

@bottle.route('/tarjeta/<id_tarjeta>')
def getTarjeta(id_tarjeta):
    '''Metodo que permite obtener una 
    tarjeta basada en su ID pasado 
    como parametro'''
    
    tarjeta = client.get_card(id_tarjeta)
    
    # Propiedades de la tarjeta
    tarjeta.get_list().name  # nombre de la lista donde esta la tarjeta
    
    tarjeta.listCardMove_date()  #Litas las cuales a pertenecido esta tarjeta Ej:
    
    #Este Metodo es el que me permite medir el tiempo que se ha mvido de una tarjeta a otra
    x = [
            [u'En Desarrollo', u'Revision', datetime.datetime(2016, 6, 13, 5, 30, 25, 99000, tzinfo=tzutc())],
            [u'Decidido', u'En Desarrollo', datetime.datetime(2016, 6, 13, 5, 28, 39, 474000, tzinfo=tzutc())]
        ]
    
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
