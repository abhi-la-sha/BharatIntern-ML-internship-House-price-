from flask import Flask, render_template, request, jsonify
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open("RidgeModel.pkl", 'rb'))

@app.route('/')
def index():
    housesize = sorted(data['total_sqft'].unique())
    bathrooms = sorted(data['bath'].unique())
    beds = sorted(data['size'].unique())
    area = sorted(data['area_type'].unique())
    balcony = sorted(data['balcony'].unique())

    return render_template('index.html', housesize=housesize, bathrooms=bathrooms, beds=beds, area= area, balcony=balcony)

@app.route('/predict', methods=['POST'])
def predict():
    housesize = request.form.get('total_sqft')
    bathrooms = request.form.get('bath')
    beds = request.form.get('size')
    area = request.form.get('area_type')
    balcony = request.form.get('balcony')

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[housesize,bathrooms,beds,area,balcony]],
                               columns=['total_sqft','bath','size','area_type','balcony'])

    print("Input Data:")
    print(input_data)

    # Handle unknown categories in the input data
    for column in input_data.columns:
        unknown_categories = set(input_data[column]) - set(data[column].unique())
        if unknown_categories:
            # Handle unknown categories (e.g., replace with a default value)
            input_data[column] = input_data[column].replace(unknown_categories, data[column].mode()[0])

    print("Processed Input Data:")
    print(input_data)

    # Predict the price
    prediction = pipe.predict(input_data)[0]

    return str(prediction)
from flask import Flask, render_template, request
import pandas as pd
import pickle

app = Flask(__name__)
data = pd.read_csv('cleaned_data.csv')
pipe = pickle.load(open("RidgeModel.pkl", 'rb'))

@app.route('/')
def index():
    housesize = sorted(data['total_sqft'].unique())
    bathrooms = sorted(data['bath'].unique())
    beds = sorted(data['size'].unique())
    area = sorted(data['area_type'].unique())
    balcony = sorted(data['balcony'].unique())

    return render_template('index.html', housesize=housesize, bathrooms=bathrooms, beds=beds, area= area, balcony=balcony)

@app.route('/predict', methods=['POST'])
def predict():
    housesize = request.form.get('total_sqft')
    bathrooms = request.form.get('bath')
    beds = request.form.get('size')
    area = request.form.get('area_type')
    balcony = request.form.get('balcony')

    # Create a DataFrame with the input data
    input_data = pd.DataFrame([[housesize,bathrooms,beds,area,balcony]],
                               columns=['total_sqft','bath','size','area_type','balcony'])

    print("Input Data:")
    print(input_data)

    # Convert 'baths' column to numeric with errors='coerce'
    input_data['bath'] = pd.to_numeric(input_data['bath'], errors='coerce')

    # Convert input data to numeric types
    input_data = input_data.astype({'total_sqft': float, 'bath': int, 'size': int, 'area_type': str, 'balcony':int })

    # Handle unknown categories in the input data
    for column in input_data.columns:
        unknown_categories = set(input_data[column]) - set(data[column].unique())
        if unknown_categories:
            print(f"Unknown categories in {column}: {unknown_categories}")
            # Handle unknown categories (e.g., replace with a default value)
            input_data[column] = input_data[column].replace(unknown_categories, data[column].mode()[0])

    print("Processed Input Data:")
    print(input_data)

    # Predict the price
    prediction = pipe.predict(input_data)[0]

    return str(prediction)

if __name__ == "__main__":
    app.run(debug=True, port=5000)


if __name__ == "__main__":
    app.run(debug=True, port=5000)
