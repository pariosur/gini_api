import requests
import pandas as pd
import plotly.express as px

class GiniIndexAPI:
    def __init__(self, country, start_year, end_year):
        self.base_url = 'https://api.worldbank.org/v2/country/'
        self.indicator_code = 'SI.POV.GINI'
        self.country = country
        self.start_year = start_year
        self.end_year = end_year

    def extract(self):
        url = f"{self.base_url}{self.country}/indicator/{self.indicator_code}?date={self.start_year}:{self.end_year}&format=json"
        response = requests.get(url)
        data = response.json()[1]

        if len(self.country) != 3:
            raise ValueError("Invalid country code. Please enter a 3 letter country code.")
        if self.start_year > self.end_year:
            raise ValueError("Invalid year range. Please make sure start year is before end year.")
        return data

    def transform(self, data):

        df = pd.DataFrame(data)
        df['date'] = pd.to_datetime(df['date'], format='%Y')
        df = df.set_index("date")
        df = df[["value"]]
        df.columns = ["Gini Index"]
        df.index.name = "Year"
        df.columns = [self.country]
        df = df[(df.index >= pd.to_datetime(str(self.start_year))) & (df.index <= pd.to_datetime(str(self.end_year)))]
        df = df.sort_index()
        df.interpolate(method='values', limit_direction='forward', inplace=True)
        return df

    def load(self, df):
        fig = px.line(df, title=f"Gini Index for {self.country} from {self.start_year} to {self.end_year}")
        fig.show()

    def run(self):

        data = self.extract()
        data = self.transform(data)
        self.load(data)
        self.plot()

if __name__ == "__main__":
    country = input("Enter the 3 letter country code: ")
    start_year = int(input("Enter the start year: "))
    end_year = int(input("Enter the end year: "))
    gini = GiniIndexAPI(country, start_year, end_year)
    gini.run()
