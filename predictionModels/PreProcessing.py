# Pre Processing Data Set

import pickle
import pandas as pd
from predictionModels.GetData import derive_nth_day_feature,attributes


with open('records_processed.pkl','rb')as fp:
    processedRecords=pickle.load(fp)

dataFrame=pd.DataFrame(processedRecords,columns=attributes).set_index('date')

for attribute in attributes:
    if(attribute!='date'):
        for I in range(1,4):
            derive_nth_day_feature(dataFrame,attribute,I)


# Remove Attributes like mean,max,and min temperature from the original List


attributes_remove=[
    
]




