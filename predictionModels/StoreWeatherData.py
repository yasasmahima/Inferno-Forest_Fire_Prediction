import os.path
import pickle
from datetime import timedelta

from predictionModels.GetData import API,URL,extract_weather_api,getTargetDate


weatherRecord1='weatherRecords_1.pkl'
weatherRecord2='weatherRecords_2.pkl'

if(os.path.isfile(weatherRecord2)):
    print("Successfully Added 1000 Records to the Files")

elif(os.path.isfile(weatherRecord1)):
    with open(weatherRecord1,'rc1')as file1:
        records=pickle.load(file1)

    targetDate=records[-1][0]+timedelta(days=1)

    records+=extract_weather_api(API,URL,targetDate,500)

    numberOfRecords=len(records)

    print('Number of Records Collected From Dark Weather API : ',numberOfRecords)

    with open(weatherRecord2,'rc2') as file2:
        pickle.dump(records,file2)


    print('Weather Records file 2 in recoreded in ',weatherRecord2)

else:

    targetDate=getTargetDate()
    weatherRecords=extract_weather_api(URL,API,targetDate,500)

    numberOfRecords=len(weatherRecords)

    print("Number of Records Collected : ",numberOfRecords)

    with open(weatherRecord1,'rc3') as file:
        pickle.dump(weatherRecords,file)

    print("weather Records in 1 st day Save in to : ",weatherRecord1)



