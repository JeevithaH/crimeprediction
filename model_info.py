import matplotlib.pyplot as plt
import seaborn as sns
import warnings

warnings.filterwarnings("ignore")
import io
import base64
import pandas as pd
import statsmodels.api as sm


def statevscrime(data):
    state_totals = data.groupby('STATE/UT')['TOTAL IPC CRIMES'].sum()
    # Create a bar chart
    plt.figure(figsize=(12, 8))
    plt.bar(state_totals.index, state_totals.values)
    plt.xticks(rotation=90)
    plt.xlabel('State/Union Territory')
    plt.ylabel('Total IPC Crimes')
    plt.title('Total IPC Crimes by State/Union Territory')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()

    return img_str


def crimetypevscount(data):
    crime_totals = data[['MURDER', 'RAPE', 'KIDNAPPING & ABDUCTION', 'ROBBERY', 'BURGLARY', 'THEFT']].sum()

    # Convert crime_totals into a DataFrame
    crime_totals_df = crime_totals.reset_index()
    crime_totals_df.columns = ['Crime Type', 'Total']

    plt.figure(figsize=(12, 8))
    sns.set_style("whitegrid")

    # Using barplot to create a pie chart-like visualization
    sns.barplot(x='Total', y='Crime Type', data=crime_totals_df, palette='viridis')

    plt.title('Proportion of Crimes by Type')
    plt.xlabel('Total Crimes')
    plt.ylabel('Crime Type')

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()

    return img_str


def yearvscrime(data):
    year = data['YEAR']
    total_crime = data['TOTAL IPC CRIMES']

    # Create a bar graph
    plt.figure(figsize=(6, 6))
    plt.bar(year, total_crime, color='blue')
    plt.xlabel('Year')
    plt.ylabel('Total Crime')
    plt.title('Total Crime vs. Year')
    plt.xticks(rotation=45)

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()

    return img_str


def forcastcrime():
    crime_df = pd.read_csv(r"D:\crime_03_16 (1)\crime_03_16\data\crime_2023.csv", parse_dates=['YEAR'], index_col=['YEAR'])

    # Resample data to yearly frequency
    crime_yearly = crime_df.resample('Y').sum()

    model = sm.tsa.ARIMA(crime_yearly['TOTAL IPC CRIMES'], order=(1, 1, 1))
    results = model.fit()

    # Resample data to yearly frequency
    crime_yearly = crime_df.resample('Y').sum()
    plt.figure(figsize=(6, 6))
    forecast = results.predict(start=len(crime_yearly), end=len(crime_yearly) + 4)
    plt.plot(crime_yearly.index, crime_yearly['TOTAL IPC CRIMES'], label='Actual')
    plt.plot(forecast.index, forecast, label='Forecast')
    plt.title('Actual vs Forecasted Total IPC Crimes')
    plt.xlabel('Year')
    plt.ylabel('Number of Cases')
    plt.legend()

    img_buffer = io.BytesIO()
    plt.savefig(img_buffer, format='png')
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode('utf-8')
    plt.close()

    return img_str
