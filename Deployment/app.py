from flask import Flask, request, jsonify
from flask_cors import CORS
import os, requests, dotenv

app = Flask(__name__)
CORS(app)
dotenv.load_dotenv()

@app.route("/")
def index():
    return "Bima Sakti API is online!"

@app.route("/stunting", methods=['POST'])
def stunting():
    if request.method == 'POST':
        # ambil data dari request
        data = request.get_json()
        umur = data['umur']
        kelamin = data['kelamin']
        tinggi_badan = data['tinggi_badan']
        
        # convert kelamin jadi angka
        if kelamin.lower() == 'male':
            kelamin_angka = 0
        elif kelamin.lower() == 'female':
            kelamin_angka = 1
        
        # Setting API and End point
        api_ibm = os.getenv("API_IBM")
        scoring_url_stunting = os.getenv("END_POINT_STUNTING")
        
        # Import API IBM
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": api_ibm, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]
        
        def prediction_stunt(umur, kelamin_angka, tinggi_badan):
            if umur <= 60 and (kelamin_angka >= 0 and kelamin_angka <= 1) and tinggi_badan <= 128:
                # Menyusun data untuk dikirim  
                payload_scoring = {
                    "input_data": [{
                        "fields": ["umur", "kelamin", "tinggi_badan"],
                        "values": [[umur, kelamin_angka, tinggi_badan]]
                    }]
                }
                header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
                response_scoring = requests.post(scoring_url_stunting, json=payload_scoring, headers=header)
                
                # Mengambil data yang telah dijawab API
                scoring_response = response_scoring.json()
                prediksi = scoring_response['predictions'][0]['values'][0][0]
                
                # Kondisi prediki
                if prediksi == 0:
                    result = {"stunt_predict": "Severely Stunted"}
                    return result
                elif prediksi == 1:
                    result = {"stunt_predict": "Stunted"}
                    return result
                elif prediksi == 2:
                    result = {"stunt_predict": "Normal"}
                    return result
                else:
                    result = {"stunt_predict": "Tinggi"}
                    return result
            else:
                return {"error": "Invalid input values"}
            
        try:
            return jsonify(prediction_stunt(umur, kelamin_angka, tinggi_badan))
        except Exception as e:
            return jsonify({"error": "System error", "message": str(e)})

@app.route("/diabetes", methods=['POST'])
def diabetes():
    if request.method == 'POST':
        data = request.get_json()
        pregnancies = data['pregnancies']
        glucose = data['glucose']
        blood_pressure = data['blood_pressure']
        skin_thickness = data['skin_thickness']
        insulin = data['insulin']
        bmi = data['bmi']
        dpf = data['dpf']
        age = data['age']
        
        # Setting API and End point
        api_ibm = os.getenv("API_IBM")
        scoring_url_diabetes = os.getenv("END_POINT_DIABETES")
        
        # Import API IBM
        token_response = requests.post('https://iam.cloud.ibm.com/identity/token', data={"apikey": api_ibm, "grant_type": 'urn:ibm:params:oauth:grant-type:apikey'})
        mltoken = token_response.json()["access_token"]
        
        def prediction_diabetes(pregnancies, glucose, blood_pressure ,skin_thickness ,insulin ,bmi ,dpf ,age):
            # Menyusun data untuk dikirim  
            payload_scoring = {
                "input_data": [{
                    "fields": ["pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin", "bmi", "dpf", "age"],
                    "values": [[pregnancies, glucose, blood_pressure, skin_thickness, insulin, bmi, dpf, age]]
                    }]
                }
            header = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + mltoken}
            response_scoring = requests.post(scoring_url_diabetes, json=payload_scoring, headers=header)
            
            # Mengambil data yang telah dijawab API
            scoring_response = response_scoring.json()
            prediksi = scoring_response['predictions'][0]['values'][0][0]
            
            # Kondisi prediki
            if prediksi == 0:
                result = {'prediction':'Pasien tidak terkena diabetes'}
                return result
            elif prediksi == 1:
                result = {'prediction':'Pasien terkena diabetes'}
                return result
            else:
                result = {'prediction':'Not Found'}
                return result
            
        try:
            return jsonify(prediction_diabetes(pregnancies, glucose, blood_pressure ,skin_thickness ,insulin ,bmi ,dpf ,age))
        except Exception as e:
            return jsonify({"error": "System error", "message": str(e)})
        
if __name__ == "__main__":
    app.run(debug=True)