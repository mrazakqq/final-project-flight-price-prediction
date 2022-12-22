import pandas as pd
import pickle
from flask import Flask, render_template, request, jsonify
from sklearn.preprocessing import LabelEncoder, OneHotEncoder
from datetime import datetime


app = Flask(__name__)
# df = pd.read_csv('./db/clean-data-label-encoding.csv')
# df_ = pd.read_csv('./db/clean-data.csv')
labelColumns = ['stops', 'class']
oheColumns = ['airline', 'source_city', 'destination_city', 'departure_time', 'arrival_time']
# cols = ['stops', 'class', 'airline', 'source_city', 'destination_city', 'departure_time', 'arrival_time']

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/resu', methods=['GET', 'POST'])
def result1():
  req = request.json
  data = pd.DataFrame([req])
  df = pd.read_csv('./db/clean-data-only-remove-outliers.csv')
  duration = pd.concat([df.duration, data.duration])
  daysLeft = pd.concat([df.days_left, data.days_left])
  durationScale = (((data.duration-duration.min())/(duration.max()-duration.min()))).to_list()
  daysLeftScale = ((data.days_left-daysLeft.mean())/daysLeft.std()).to_list()
  data.duration = durationScale[0]
  data.days_left = daysLeftScale[0]

  leStops = LabelEncoder()
  leClass = LabelEncoder()
  ohe = OneHotEncoder(handle_unknown='ignore', sparse=False)

  df.stops = leStops.fit_transform(df.stops)
  df['class'] = leClass.fit_transform(df['class'])
  ohe.fit(df[oheColumns])
  dfOhe = pd.DataFrame(ohe.transform(df[oheColumns]), columns=ohe.get_feature_names(oheColumns))
  df = pd.concat([df, dfOhe], axis=1).drop(columns=oheColumns)

  data.stops = leStops.transform(data.stops)
  data['class'] = leClass.transform(data['class'])
  ohe.transform(data[oheColumns])
  dataOhe = pd.DataFrame(ohe.transform(data[oheColumns]), columns=ohe.get_feature_names(oheColumns))
  data = pd.concat([data, dataOhe], axis=1).drop(columns=oheColumns)
  
  with open('./model/rf-model.pkl', 'rb') as file:
    model = pickle.load(file)

  prediction = model.predict(data)

  data['prediction'] = prediction[0]
  data['datetime'] = datetime.now().strftime('%y-%m-%d')

  print(data)

  return jsonify(
      {
          'status': 'Berhasil',
          'data': req,
          'dt': datetime.now().strftime('%y-%m-%d'),
          'prediction': prediction[0]
      }
  )

  




# @app.route('/rp

@app.route('/predict1', methods=['GET'])
def pred():
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
  df1.sex = label_sex.transform(df1.sex)
  df1.smoker = label_smoker.transform(df1.smoker)
  df1.region = label_region.transform(df1.region)

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

@app.route('/result', methods=['GET', 'POST'])
def result():
  if request.method == 'POST':
  #   labelColumns = ['stops', 'class']
  #   oheColumns = ['airline', 'source_city', 'destination_city', 'departure_time', 'arrival_time']
  #   # df = pd.DataFrame(columns=columns)
    #label
    stops = request.form['stops']
    travelClass = request.form['travel-class']
  #   #ohe
    airline = request.form['airline']
    sourceCity = request.form['source-city']
    destinationCity = request.form['destination-city']
    # process
    departureTime = request.form['departure-time']
    arrivalTime = request.form['arrival-time']
    departureDate = request.form['departure-date']
    # duration
    duration = datetime.strptime(arrivalTime, '%H:%M') - datetime.strptime(departureTime, '%H:%M')
    duration = datetime.strptime(str(duration), '%H:%M:%S')
    duration = datetime.strftime(duration, '%H:%M:%S')
    h, m, s = duration.split(':')
    duration = round((int(h) * 3600 + int(m) * 60 + int(s))/3600, 2)
    # days-left
    today = datetime.now()
    departureDate = datetime.strptime(departureDate, '%Y-%m-%d')
    daysLeft = departureDate - today
    daysLeftFunc = lambda x: int(x) if int(x) > 0 else 0 

    print(stops)
    print(travelClass)
    print(airline)
    print(sourceCity)
    print(destinationCity)
    print(departureTime)
    print(arrivalTime)
    print(departureDate)
    print(duration)
    print(daysLeftFunc(daysLeft.days))
    # return 'thanks'
  

  data = pd.DataFrame({
    'class': travelClass,
    'airline': airline,
    'source_city': sourceCity,
    'destination_city': destinationCity,
    'departure_time': departureTime,
    'arrival_time': arrivalTime,
    'stops': stops,
    'days_left': daysLeftFunc(daysLeft.days),
    'duration': duration
  })
  # df = df.append({
  #   'age': age, 
  #   'sex': sex, 
  #   'bmi': bmi,
  #   'children': children,
  #   'smoker': smoker,
  #   'region': region
  # }, ignore_index=True)
  # with open('./model/Lin_reg.pkl', 'rb') as file:
  #   Lin_reg_model = pickle.load(file)
  # prediction = Lin_reg_model.predict(df)
  # return render_template('result.html', pred=str(round(prediction[0], 2)), name=name)
  return render_template('res.html')

if __name__ == '__main__':
  app.run()