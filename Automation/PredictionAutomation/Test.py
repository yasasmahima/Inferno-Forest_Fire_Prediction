import flask
import pandas as pd
import tensorflow as tf
import numpy as np
import pymongo
import FWI
from sklearn.ensemble import RandomForestRegressor
import pickle
import datetime
import json
from tensorflow import keras
from keras.models import load_model




def process_data(dataset, start, end, past_size,future_size):
  datas = []
  labels = []

  start = start + past_size
  if end is None:
    end = len(dataset) - future_size

  for i in range(start,end):
    indices = range(i-past_size, i)
    datas.append(np.reshape(dataset[indices], (past_size, 1)))
    labels.append(dataset[i+future_size])
  return np.array(datas), np.array(labels)




myclient = pymongo.MongoClient("mongodb://localhost:27017/")

mydb = myclient["Inferno"]

mycol = mydb["Predictions"]

df = pd.read_csv('D:\InfernoPrediction\Weather\dataset.csv')
df['dt']=pd.to_datetime(df['dt'], unit='s')



df=df.set_index('dt',drop=False).resample('24h').mean()
dataFrameSize=len(df.index)

df2=df.reset_index(level=0, inplace=True)


temperature_model = tf.keras.models.load_model("D:\FlaskTest\TemperaturePrediction.h5")
windSpeed_model=tf.keras.models.load_model("D:\FlaskTest\WindSpeedPrediction.h5")
Rh_model=tf.keras.models.load_model("D:\FlaskTest\RHPrediction.h5")


####################################### Temperature ###################################

predict_data = df['temp']
predict_data.index = df['dt']
predict_data.head()
OUTPUT_SPLIT = 677
predict_data = predict_data.values
predict_train_mean = predict_data[OUTPUT_SPLIT:].mean()
predict_train_std = predict_data[OUTPUT_SPLIT:].std()

predict_data = (predict_data[OUTPUT_SPLIT:]-predict_train_mean)/predict_train_std

# print(len(predict_data))

future_size =0

x_test, y_test = process_data(predict_data,0,330,
                                       150,
                                       future_size)

x=temperature_model.predict(x_test)

########################################## Rh  ##################################


predict_data_RH = df['humidity']
predict_data_RH.index = df['dt']
predict_data_RH.head()
OUTPUT_SPLIT = 737
predict_data_RH = predict_data_RH.values
predict_train_mean_RH = predict_data_RH[OUTPUT_SPLIT:].mean()
predict_train_std_RH = predict_data_RH[OUTPUT_SPLIT:].std()

predict_data_RH = (predict_data_RH[OUTPUT_SPLIT:]-predict_train_mean_RH)/predict_train_std_RH

x_test, y_test = process_data(predict_data_RH,0,270,
                                       90,
                                       future_size)
# Predict the RH
Rh=Rh_model.predict(x_test)


########################################## Rh  ##################################


predict_data_wind = df['wind_speed']
predict_data_wind.index = df['dt']
predict_data_wind.head()
OUTPUT_SPLIT = 677
predict_data_wind = predict_data_wind.values
predict_train_mean_wind = predict_data_wind[OUTPUT_SPLIT:].mean()
predict_train_std_wind = predict_data_wind[OUTPUT_SPLIT:].std()

predict_data_wind = (predict_data_wind[OUTPUT_SPLIT:]-predict_train_mean_wind)/predict_train_std_wind

x_test, y_test = process_data(predict_data_wind,0,330,
                                       150,
                                       future_size)
# Predict the RH
wind=windSpeed_model.predict(x_test)


dates=df['dt']
tt=dates.values
tt=tt[827:]



# print (type(tt[1]))

temperature={}
temparray=[]

spreadModelFile="D:\FlaskTest\SpreadPickle.pkl"
with open(spreadModelFile, 'rb') as file:
    spreadModel = pickle.load(file)

spreadModel


def fahToCel(value):
    return ((float(value) - 32) * 5 / 9)


def mphToKmph(value):
    return value * 1.60934

def job():

    for i in range (len(tt)):


    # result = loaded_model.score(X_test, Y_test)
    # print(result)


        temperature=float(x[i]*predict_train_std +predict_train_mean)
        relativeHumdity=float(Rh[i]*predict_train_std_RH +predict_train_mean_RH)
        windSpeed=float(wind[i]*predict_train_std_wind +predict_train_mean_wind)

        new_input = [[fahToCel(temperature),relativeHumdity,mphToKmph(windSpeed)]]
        output = spreadModel.predict(new_input)

        risk=FWI.getRisk(temperature,windSpeed,relativeHumdity)

        details={"Date":str(tt[i].astype('M8[D]')),
             "Temperature":temperature,
             "Relative Humidity":relativeHumdity,
             "Wind Speed":windSpeed,
             "Risk":risk,
             "spread":output[0]}

        temparray.append(details)


    print(temparray[len(temparray)-1:])

# my_json_string = json.dumps(denormalized)
#

    db = mycol.insert_many(temparray[len(temparray)-2:])


job()






