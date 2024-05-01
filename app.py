import pandas as pd
from flask import Flask, render_template, jsonify, request
from flask_cors import CORS

from inference.load_data import load_data

app = Flask(__name__)
CORS(app)

# Load data
data = load_data("data/harga_cleaned.csv")


@app.route('/')
def home():

    return render_template('index.html')


@app.route('/price')
def get_all_prices():
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    if start_date and end_date:
        # Convert the dates to pandas datetime format and normalize to remove the time component
        start_date = pd.to_datetime(start_date).normalize()
        end_date = pd.to_datetime(end_date).normalize()

        # Convert the DataFrame columns to datetime, excluding non-datetime columns
        datetime_columns = pd.to_datetime(data.columns[2:], errors='coerce')

        # Create a boolean mask that checks if the dates in the DataFrame are within the provided date range
        mask = (datetime_columns >= start_date) & (datetime_columns <= end_date)

        # Filter the data based on the mask and concatenate with the first two columns
        filtered_data = pd.concat([data.iloc[:, :2], data.loc[:, data.columns[2:][mask]]], axis=1)
    else:
        # If no dates are provided, use the entire data
        filtered_data = data

    prices = []
    for index, row in filtered_data.iterrows():
        groceries = {
            "name": row['Komoditas (Rp)'],
            "price": row.drop(['No', 'Komoditas (Rp)']).to_dict(),
            "category": row['No']
        }
        prices.append(groceries)

    return jsonify({"groceries": prices})


@app.route('/price/<date>')
def get_all_prices_by_date(date):
    if date is None:
        # If no date is provided, return the prices for all dates
        prices = data.to_dict(orient='index')
    else:
        # If a date is provided, return the prices for that date
        prices = data.set_index('Komoditas (Rp)')[date].to_dict()

    return jsonify(prices)


@app.route('/price/commodity/<commodity>')
def get_prices_by_commodity(commodity):
    # Get the prices for the given commodity
    prices = data[data['Komoditas (Rp)'] == commodity].to_dict(orient='records')

    return jsonify(prices)


@app.route('/price/commodity/<commodity>/<date>')
def get_prices_by_commodity_and_date(commodity, date):
    # Get the prices for the given commodity
    price = data.loc[data['Komoditas (Rp)'] == commodity, date].values[0]

    return jsonify({commodity: price})


@app.route('/list/commodity')
def list_commodity():
    # Get the list of commodities
    commodities = data['Komoditas (Rp)'].unique()

    return jsonify(commodities.tolist())


@app.route('/list/date')
def list_date():
    # Get the list of dates
    dates = data.columns[2:]

    return jsonify(dates.tolist())


if __name__ == '__main__':
    app.run(debug=True)
