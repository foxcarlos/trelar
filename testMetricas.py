import requests
import datetime

def listarTodasTarjetas():
    '''Mostrar Informacion de todas las tarjetas de una lista '''
    print('A continuacion se muestran todas las tarjetas:')
    data = {'tablero_id': '57581f7d6a945e2f6630a793', 'lista_id': '57582109bba4b95e66dbf4e1'}
    r = requests.get("http://127.0.0.1:8086/tarjetas", json=data)
    if r.status_code == 200:
        respJSON = r.json()
        print(respJSON)
        

def mostrarTableros():
    '''Mostrar todos los Tableros Abiertos'''
    
    print('A continuacion se muestran todos los Tableros Abiertos:')
    r = requests.get("http://127.0.0.1:8086/tableros")
    if r.status_code == 200:
        respJSON = r.json()
        print(respJSON)


def mostrarListas():
    '''Mostrar todas las Listas del Tablero trelar'''
    
    print('A continuacion se muestran todas las Listas del tablero Trelar:')
    # idTablero = '57581f7d6a945e2f6630a793'
    data = {'tablero_id': '57581f7d6a945e2f6630a793'}
    r = requests.get("http://127.0.0.1:8086/listas", json=data)
    if r.status_code == 200:
        respJSON = r.text
        print(respJSON)


def mostrarListaId():
    '''Mostrar Informacion de una Lista pasada como paramrtro del Tablero trelar'''
    
    print('A continuacion se muestra toda la informacion de una Lista:')
    idLista = '57582133019601b62df80514'
    r = requests.get("http://127.0.0.1:8086/lista/{0}".format(idLista))
    if r.status_code == 200:
        respJSON = r.text
        print(respJSON)    
        
        
def metricasTerminadas():
    '''Este Metodo busca las tarjetas que se encuentran 
    en la lista Terminadas y obtiene los dias'''
    
    # Se le pasa a la RestAPI el tablero y el Id de la Lista (Terminado)
    data = {'tablero_id': '57581f7d6a945e2f6630a793', 'lista_id': '57582133019601b62df80514'}
    r = requests.get("http://127.0.0.1:8086/tarjetas", json=data)
    
    if r.status_code == 200:
        respJSON = r.json()
        listadoTarjetas = respJSON['Tarjetas']
        print( 'A continuacion se muestran todas las tarjetas Terminadas con su Tiempo:')
        for t in listadoTarjetas:
            tarjeta_id = t['id']
            # print(tarjeta_id)
            url = "http://127.0.0.1:8086/tarjetasTerminadas/{0}".format(tarjeta_id)
            tiempos = requests.get(url)
            print(tiempos.json())

def metricasLeadTime():
    '''Este Metodo busca las tarjetas que se encuentran 
    en la lista Terminadas y obtiene los dias desde que
    esta en backlog'''
    
    # Se le pasa a la RestAPI el tablero y el Id de la Lista (Terminado)
    data = {'tablero_id': '57581f7d6a945e2f6630a793', 'lista_id': '57582133019601b62df80514'}
    r = requests.get("http://127.0.0.1:8086/tarjetas", json=data)
    
    if r.status_code == 200:
        respJSON = r.json()
        listadoTarjetas = respJSON['Tarjetas']
        print( 'A continuacion se muestran todas las tarjetas Terminadas con su Tiempo:')
        for t in listadoTarjetas:
            tarjeta_id = t['id']
            # print(tarjeta_id)
            url = "http://127.0.0.1:8086/tarjetasLeadTime/{0}".format(tarjeta_id)
            print(url)
            tiempos = requests.get(url)
            print(tiempos.json())
            

def metricasEnBackLog():
    '''Este Metodo busca las tarjetas que se encuentran 
    en la lista Backlog y obtiene los dias'''
    
    # Se le pasa a la RestAPI el tablero y el Id de la Lista en Backlog
    data = {'tablero_id': '57581f7d6a945e2f6630a793', 'lista_id': '57582109bba4b95e66dbf4e1'}
    r = requests.get("http://127.0.0.1:8086/tarjetas", json=data)
    
    if r.status_code == 200:
        respJSON = r.json()
        listadoTarjetas = respJSON['Tarjetas']
        print( 'A continuacion se muestran todas las tarjetas que aun permanecen en backlog:')
        for t in listadoTarjetas:
            tarjeta_id = t['id']
            url = "http://127.0.0.1:8086/tarjetasEnBacklog/{0}".format(tarjeta_id)
            tiempos = requests.get(url)
            print(tiempos.json())
                
if __name__ == '__main__':
    
    print('====================================================================')
    listarTodasTarjetas()
    
    print('====================================================================')    
    mostrarTableros()
    
    print('====================================================================')    
    mostrarListas()
    
    print('====================================================================')
    mostrarListaId()
    
    print('=========================================================================================')
    print('Metricas Cycle Time:Esta mide el tiempo que sucede entre el inicio y el final del proces')
    print('=========================================================================================')
    metricasTerminadas()
    
    print('=========================================================================================')
    print('Metricas Touch Time: Registra el tiempo en el cual un iten fue realmente trabajado')
    print('=========================================================================================')
    metricasEnBackLog()
    
    print('=========================================================================================')
    print('Metricas Lead Time: Registra el tiempo que sucede entre el momento en el cual se esta')
    print('pidiendo un item de trabajo y el momento de su entrega')
    print('=========================================================================================')
    metricasLeadTime()