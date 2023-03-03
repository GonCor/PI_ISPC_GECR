import requests

def obtener_precios_criptomonedas(criptomonedas):
    # URL de la API de CoinGecko para obtener los precios de las criptomonedas
    url = 'https://api.coingecko.com/api/v3/simple/price'

    # Parámetros de la solicitud API
    params = {
        'ids': ','.join(criptomonedas),
        'vs_currencies': 'usd'
    }

    # Realizar la solicitud a la API de CoinGecko
    response = requests.get(url, params=params)

    # Obtener los precios de las criptomonedas
    precios = response.json()

    # Devolver los precios como un diccionario
    return precios




