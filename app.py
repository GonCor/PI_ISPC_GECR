from flask import Flask, render_template
import pandas as pd
from alpha_vantage.timeseries import TimeSeries

key = 'ISEKQWBWL7X54MDM'

app = Flask(__name__)

# Define la ruta principal de la aplicación Flask
@app.route('/')
def index():
    # Crea una lista de símbolos de acciones
    tickers = ['AAPL', 'TSLA', 'AMZN', 'GOOGL']

    # Obtiene los resultados del último cierre de la función últimoCierre()
    resultados = ultimoCierre(tickers)

    # Retorna el resultado en un template HTML
    return render_template('resultados.html', resultados=resultados)

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
