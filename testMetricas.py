# Mostrar todos los Tableros Abiertos
http://127.0.0.1:8086/tableros

# Mostrar todas las Listas del Tablero trelar
http://127.0.0.1:8086/listas/57581f7d6a945e2f6630a793

# Mostrar Informacion de una Lista pasada como paramrtro del Tablero trelar
http://127.0.0.1:8086/lista/57582133019601b62df80514

# Mostrar Informacion de todas las tarjetas de una lista 
http://127.0.0.1:8086/tarjetas


import requests
r = requests.get("http://127.0.0.1:8086/tarjetas")
if r.status_code == 200:
    respJSON = r.json()
    listadoTarjetas = respJSON['Tarjetas']
    for t in listadoTarjetas:
        tarjeta_id = t['id']
        


requests.get("/tarjetaBuscarMovmientos/", params = {"id_tarjeta":"575e3f6ddf99f52d0b8b8795"})
