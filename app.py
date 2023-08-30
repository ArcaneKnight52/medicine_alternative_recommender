from flask import Flask, render_template, request
import pickle
import pandas as pd

app = Flask(__name__)

# Load medicine-dataframe from pickle as a dictionary
medicines_dict = pickle.load(open('medicine_dict.pkl', 'rb'))
medicines = pd.DataFrame(medicines_dict)

# Load similarity-vector-data from pickle as a dictionary
similarity = pickle.load(open('similarity.pkl', 'rb'))

def recommend(medicine):
    medicine_index = medicines[medicines['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(enumerate(distances), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(medicines.iloc[i[0]].Drug_Name)
    return recommended_medicines

@app.route('/')
def index():
    return render_template('index.html', medicines=medicines['Drug_Name'].values)

@app.route('/recommend', methods=['POST'])
def recommendation():
    selected_medicine_name = request.form['selected_medicine_name']
    recommendations = recommend(selected_medicine_name)
    return render_template('index.html', medicines=medicines['Drug_Name'].values, selected_medicine_name=selected_medicine_name, recommendations=recommendations)

if __name__ == '__main__':
    app.run(debug=True)
