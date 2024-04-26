import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path
from datetime import datetime
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.stattools import adfuller
from pmdarima import auto_arima
import warnings
warnings.filterwarnings("ignore")

#open and read data from .csv file to pandas dataframe
def load_clean_df():
    path = Path.cwd().parent.parent
    file = str(path) + "/data_cleanup/cleaned_data.csv"
    return pd.read_csv(file)

#filtering data --- currently need only guests that showed up
def only_checkout_df(df):
    return df[df["status_rezervacije"] == "Check-Out"]

def date_time_convert(df):
    df["datum_dolaska"] = pd.to_datetime(df["datum_dolaska"])
    df["datum_kreiranja_rezervacije"] = pd.to_datetime(df["datum_kreiranja_rezervacije"])
    df["datum_otkazivanja_rezervacije"] = pd.to_datetime(df["datum_otkazivanja_rezervacije"])
    df["datum_odjave"] = pd.to_datetime(df["datum_odjave"])
    return df

def new_occupancy_df(df):
    df["ukupan_broj_gostiju"] = df['broj_odraslih_gostiju'] + df['broj_djece_gostiju']
    dates = []
    for index, row in df.iterrows():
        delta = (row['datum_odjave'] - row['datum_dolaska']).days
        for i in range(delta):
            dates.append((row['datum_dolaska'] + pd.Timedelta(days = i), row['ukupan_broj_gostiju']))
    occupancy_df = pd.DataFrame(dates, columns=['datum', 'broj_gostiju']).groupby('datum')['broj_gostiju'].sum().reset_index()
    occupancy_df.index = occupancy_df["datum"]
    del occupancy_df["datum"]
    print(occupancy_df.head())
    return occupancy_df
    
        
    
    

def main():
    init_df = load_clean_df()
    checkout_df = only_checkout_df(date_time_convert(init_df))
    occupancy_df = new_occupancy_df(checkout_df)
    plt.figure(figsize=(35, 7))  # Prilagodite veličinu prema potrebi
    plt.plot(occupancy_df['datum'], occupancy_df['broj_gostiju'], color='pink')
    plt.title('Ukupan broj gostiju u hotelu na dan')
    plt.xlabel('Datum')
    plt.ylabel('Ukupan broj gostiju')
    plt.xticks(rotation=45)  # Rotira oznake na x-osi za bolju čitljivost
    plt.tight_layout()  # Prilagodba layouta za sprečavanje preklapanja
    plt.show()
    
    
    
    
if __name__ == "__main__":
    main()