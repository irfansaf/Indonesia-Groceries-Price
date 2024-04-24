from flask import Flask, render_template, jsonify

from inference.load_data import load_data

app = Flask(__name__)

# Load data
data = load_data("data/harga_cleaned.csv")


@app.route('/')
def home():
    prices_2021 = data.set_index('Komoditas (Rp)')['2021'].to_dict()
    prices_2022 = data.set_index('Komoditas (Rp)')['2022'].to_dict()
    prices_2023 = data.set_index('Komoditas (Rp)')['2023'].to_dict()
    prices_2024 = data.set_index('Komoditas (Rp)')['2024'].to_dict()

    print(prices_2021)
    return render_template('index.html')


@app.route('/price')
def get_all_prices():
    # Transpose the data so that the dates are the keys
    transposed_data = data.set_index('Komoditas (Rp)').T

    # Convert the transposed data to a dictionary
    prices = transposed_data.to_dict()

    return jsonify(prices)


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
