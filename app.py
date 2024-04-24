from flask import Flask, render_template, jsonify

from inference.load_data import load_data

app = Flask(__name__)

# Load data
data = load_data("data/harga_cleaned.csv")


@app.route('/')
def home():
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


if __name__ == '__main__':
    app.run(debug=True)
