import json
from flask import Flask, request, jsonify, Response
import stock_analysis
from datetime import datetime, timedelta

app = Flask(__name__)

@app.route('/forecast', methods=['GET'])
def forecast():
    data = request.get_json()
    ticker = data.get('ticker', 'PETKM.IS')  
    model = stock_analysis.create_prophet_model(ticker)
    forecast = stock_analysis.make_forecast(model, 365)
    return stock_analysis.make_forecast_chart(model, forecast)


@app.route('/dataDatePeriod', methods=['GET'])
def data_date_period():
    data = request.get_json()
    ticker = data.get('ticker', 'PETKM.IS')  

    # Get the start and end dates from the JSON data
    start = data.get('start', (datetime.now() - timedelta(days=5*365)).strftime('%Y-%m-%d'))  
    end = data.get('end', datetime.now().strftime('%Y-%m-%d'))  

    stock_value = stock_analysis.get_stock_historical_info(ticker, start, end)

    stock_value_json =  stock_value.reset_index().to_json(date_format='iso', orient='records')
    stock_value_json = json.dumps(json.loads(stock_value_json))
    # Create a response with the JSON data
    return Response(stock_value_json, mimetype='application/json')

@app.route('/dataPeriod', methods=['GET'])
def data_period():
    data = request.get_json()
    ticker = data.get('ticker', 'PETKM.IS')  
    period = data.get('period', 'max')
    stock_value = stock_analysis.get_stock_data(ticker, period)

    stock_value_json =  stock_value.reset_index().to_json(date_format='iso', orient='records')
    stock_value_json = json.dumps(json.loads(stock_value_json))
    # Create a response with the JSON data
    return Response(stock_value_json, mimetype='application/json')


if __name__ == "__main__":
  app.run()

