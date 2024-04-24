from flask import Flask, render_template

from inference.load_data import load_data

app = Flask(__name__)

# Load data
data = load_data("harga_cleaned.csv")
print(data.head())

@app.route('/')
def home():
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
