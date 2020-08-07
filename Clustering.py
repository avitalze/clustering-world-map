# from pandas import read_excel
import pandas as pd
import numpy as np
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from matplotlib.ticker import StrMethodFormatter

class Clustering:

    def __init__(self,pathFromUser)-> None:
        # tempFilePath=r'C:\Users\avital\Downloads\Dataset‪.xlsx'
        self.filePath=pathFromUser
        #self.df=None



    def preProcess(self):
        df = pd.read_excel(self.filePath)
        print(df.dtypes)
        print("---------------------------------------")
        print(df.isnull().sum(axis=0))
        # cleanData
        df= self.cleanData(df)
        print("---------------------------------------")
        print(df.isnull().sum(axis=0))
        # Standardization
        df= self.standardization(df)
        # Groupby[‘country’] and  Drop([‘year’])
        # dfByStates = df.groupby('country')['Life Ladder', 'Log GDP per capita'].mean().round(2)

        df_agg = (df.groupby('country').agg({'Life Ladder': 'mean', 'Log GDP per capita': 'mean', 'Social support': 'mean'
                                                ,'Healthy life expectancy at birth': 'mean','Freedom to make life choices': 'mean','Generosity': 'mean'
                                             ,'Perceptions of corruption': 'mean','Positive affect': 'mean','Negative affect': 'mean',
                                             'Confidence in national government': 'mean','Democratic Quality': 'mean','Delivery Quality': 'mean'
                                                ,'Standard deviation of ladder by country-year': 'mean','Standard deviation/Mean of ladder by country-year': 'mean'}))
        #print(dfByStates)
        print(df_agg)

        return df_agg

    def cleanData(self,df):
        # fill empty values
        for i in df.columns:
            isNumber = np.issubdtype(df[i].dtype, np.number)
            emptyCells = df[i].isnull().sum(axis=0)
            if (isNumber and emptyCells > 0):
                df[i] = df[i].fillna(df[i].mean())
                print(df[i].mean())
        return df


    def standardization(self, df):
        for coll in df:
            print(df[coll].head())
            if(coll != "country" and coll != "year"):
                collMean = df[coll].mean()
                collStd = df[coll].std()
                culc = lambda x: (x - collMean) / collStd
                df[coll] = df[coll].apply(culc)
                print("************************")
                print(df[coll].head())

                # hist = df.hist(bins=3)
                # hist.
                # # df[coll].hist(bins=50)

        return df




