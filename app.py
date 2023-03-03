from flask import Flask, render_template
from utils.apicryptos import obtener_precios_criptomonedas
from alpha_vantage.timeseries import TimeSeries
import pandas as pd
import requests
import matplotlib.pyplot as plt   # add this line

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

    # Genera el gráfico y obtiene el nombre del archivo
    filename = grafico()

    # Retorna la plantilla index.html con las variables resultados, precios y filename
    return render_template('index.html', resultados=resultados, precios=precios, filename=filename)



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


def grafico():
    key = 'PX915KW5TU85V9VM'
    symbol = 'AAPL'
    url = f'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol={symbol}&apikey={key}'

    response = requests.get(url)
    data = response.json()

    # Obtener solo los datos de los precios
    precioHistoricoApple = data['Time Series (Daily)']

    # Convertir las fechas al formato de fecha y hora de Python
    df = pd.DataFrame.from_dict(precioHistoricoApple, orient='index')
    df.index = pd.to_datetime(df.index)

    # Leer los datos de precios históricos de Apple en un DataFrame de Pandas
    df = df.astype(float)

    # Crear el gráfico usando Matplotlib
    fig, ax = plt.subplots()
    ax.plot(df.index, df['4. close'])
    ax.set_xlabel('Fecha')
    ax.set_ylabel('Precio')
    ax.set_title('Evolucion Ultimos 6 meses')

    # Guardar el gráfico en un archivo
    filename = 'static/grafico.png'
    fig.savefig(filename)

    # Retornar el nombre del archivo para que pueda ser mostrado en la página web
    return filename



if __name__ == '__main__':
    app.run(debug=True)
