from trello import TrelloClient


# api_key='your-key' - 05571f7ecf0d9177c020b9ab3495aaac
# api_secret='your-secret' - 03a65f30fb4946c03cba7998327f7e10025493f7e036408d6efbcdbd63fc66f5
# token='your-oauth-token-key' - 1316a12594687b611d0c631896b9b421436bd955d0d376162521c5ed267155d8
# token_secret='your-oauth-token-secret' - 5d0d9ac40b148703315c54e64b7998d2

client = TrelloClient(api_key='05571f7ecf0d9177c020b9ab3495aaac',
    api_secret='03a65f30fb4946c03cba7998327f7e10025493f7e036408d6efbcdbd63fc66f5',
    token='1316a12594687b611d0c631896b9b421436bd955d0d376162521c5ed267155d8',
    token_secret='5d0d9ac40b148703315c54e64b7998d2'
)

def getTableros(filtro=""):
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

# Obtener un tablero por su ID
tablero = client.get_board('57581f7d6a945e2f6630a793')
print(tablero)

# Obtener todas las listas de un tablero
print( tablero.all_lists() )

# Obtener de un tablero una lista o columna por su ID
tablero.get_list('57582109bba4b95e66dbf4e1')

# Listar los tableros Abiertos
print( client.list_boards(board_filter="open") )

# Listar todos los tableros
print( client.list_boards() )

# Listar columnas
abiertos = client.list_boards(board_filter="open")
for b in abiertos:
    b.all_lists()

# Listar atributos
for b in abiertos:
    for l in b.all_lists():
        for c in l.list_cards():
            print( c.fetch() )

# Otros Comandos de pruebas realizados para obtener inforamcion de las tarjetas

"""
>>> c.assign
>>> c.attach
>>> c.attachments
>>> c.attriExp
>>> c.board
<Board trelar>

>>> c.checklists
>>> c.client
<trello.trelloclient.TrelloClient object at 0xb41b4c4c>

>>> c.closed
False

>>> c.comment
<bound method Card.comment of <Card Testing a py-trello, obtener un listado de todos los tableros.>>

>>> c.create_date
datetime.datetime(2016, 6, 9, 4, 49, 2, 620000, tzinfo=tzutc())

>>> c.dateLastActivity
datetime.datetime(2016, 6, 9, 4, 49, 2, 610000, tzinfo=tzutc())

>>> c.date_last_activity
datetime.datetime(2016, 6, 9, 4, 49, 2, 610000, tzinfo=tzutc())

>>> c.desc
u''

>>> c.description
u''

>>> c.due
>>> c.due_date
''

>>> c.id
u'5758f53e74a534e5f6ef252b'

>>> c.idBoard
u'57581f7d6a945e2f6630a793'

>>> c.idLabels
[]

>>> c.idList
u'57582126be36c73d6688b24b'

>>> c.idMembers
[]

>>> c.idShort
16

>>> c.labels
[]

>>> c.label_ids
[]

>>> c.shortUrl
u'https://trello.com/c/9bDQNh0q'

>>> c.trello_list
<List En Desarrollo>

>>> c.url
u'https://trello.com/c/9bDQNh0q/16-testing-a-py-trello-obtener-un-listado-de-todos-los-tableros'

"""
