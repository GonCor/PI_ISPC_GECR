import pandas as pd
from alpha_vantage.timeseries import TimeSeries

key = 'ISEKQWBWL7X54MDM'

# Crea una lista de símbolos de acciones
tickers = ['GOOGL', 'AAPL', 'MSFT', 'AMZN']

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

# Ejemplo de uso
resultados = ultimoCierre(tickers)
print(resultados)


