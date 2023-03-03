from flask import Flask, render_template
from utils.apicryptos import obtener_precios_criptomonedas
from alpha_vantage.timeseries import TimeSeries
import pandas as pd

key = 'ISEKQWBWL7X54MDM'

app = Flask(__name__)

@app.route('/')
def index():
    # Crea una lista de símbolos de acciones
    tickers = ['AAPL', 'TSLA', 'AMZN', 'GOOGL']
    # Lista de criptomonedas que deseas obtener precios
    criptomonedas = ['bitcoin', 'ethereum', 'dogecoin', 'cardano', 'ripple', 'litecoin', 'chainlink', 'stellar', 'uniswap', 'polygon-network']

    # Obtiene los resultados del último cierre de la función últimoCierre()
    resultados = ultimoCierre(tickers)

    # Obtiene los precios de las criptomonedas de la función obtener_precios_criptomonedas()
    precios = obtener_precios_criptomonedas(criptomonedas)

    # Retorna la plantilla index.html con las variables resultados y precios
    return render_template('index.html', resultados=resultados, precios=precios)


# Define la función últimoCierre()
def ultimoCierre(tickers):
    # Crea un objeto TimeSeries de Alpha Vantage
    ts = TimeSeries(key=key, output_format='json')

    # Define una lista para almacenar los resultados
    resultados = []

    # Itera sobre cada símbolo en la lista y llama a la función get_intraday para obtener los datos
    for ticker in tickers:
        # Obtiene los datos intradía para el símbolo actual
        data, meta_data = ts.get_intraday(ticker)

        # Convierte el objeto "dict" en un objeto DataFrame de Pandas
        df = pd.DataFrame.from_dict(data, orient='index')

        # Obtiene el valor de cierre del último día disponible
        ultimo_cierre = df.iloc[-1]['4. close']

        # Agrega una tupla con el ticker y el último cierre a la lista de resultados
        resultados.append((ticker, ultimo_cierre))

    # Retorna la lista de resultados
    return resultados



if __name__ == '__main__':
    app.run(debug=True)
