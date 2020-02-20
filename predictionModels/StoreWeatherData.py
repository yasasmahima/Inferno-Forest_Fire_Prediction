import os.patth
import pickle
from datetime import timedelta

from predictionModels.GetData import extract_weather_api,getTargetDate


weatherRecord1='weatherRecords_1.pkl'
weatherRecord2='weatherRecords_2.pkl'

if(os.path.isfile(weatherRecord2)):
    print("Successfully Added 1000 Records to the Files")

elif(os.path.isfile(weatherRecord1)):
    with open(weatherRecord2,'rc')as file:
        records=pickle.load(file)
