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

print(client.list_boards())
