#membuat API dengan flask
from flask import Flask
from flask import jsonify, request
from flask_ngrok import run_with_ngrok
from datetime import datetime

app = Flask(__name__)
server = run_with_ngrok
# run_with_ngrok(app)
server(app)

@app.route('/', methods=['GET'])
def index():
  return jsonify(
      {
          'Nama': 'Bangjek API Sukses'
      }
  )

@app.route('/predict', methods=['GET'])
def result():
  path = '/content/drive/MyDrive/Colab Notebooks/digitalskola/data-set-sample/insurance.csv'
  df = pd.read_csv(path, index_col=0)
  data = request.json
  df1 = pd.DataFrame(data, index=[0])

  #data pre-processing
  label_sex = LabelEncoder()
  label_smoker = LabelEncoder()
  label_region = LabelEncoder()

  #data prepreocssing dari csv
  df.sex = label_sex.fit_transform(df.sex)
  df.smoker = label_smoker.fit_transform(df.smoker)
  df.region = label_region.fit_transform(df.region)
  
  #data prepreocssing dari postman
  df1.sex = label_sex.fit_transform(df1.sex)
  df1.smoker = label_smoker.fit_transform(df1.smoker)
  df1.region = label_region.fit_transform(df1.region)

  #Load model
  with open('Lin_reg.pkl', 'rb') as file:
    Lin_reg = pickle.load(file)

  prediction = Lin_reg.predict(df1)
  print(prediction)

  data['prediction'] = prediction[0]
  data['datetime'] = datetime.now().strftime('%y-%m-%d')
  with open('data_collection.txt', 'a') as file: #a = append
    file.write(f'{data}\n')

  return jsonify(
      {
          'status': 'Berhasil',
          'prediction': str(prediction[0])
      }
  )

if __name__ == '__main__':
  app.run()