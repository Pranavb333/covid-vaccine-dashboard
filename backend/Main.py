#!/usr/bin/env python
# coding: utf-8

import json
import pandas as pd

class BaseCalculator:
        
    def get_daily(self, time_series):
        daily = []
        for idx in range(0,time_series.shape[0]-1):
            daily.append(time_series.iloc[idx+1]-time_series.iloc[idx])
        daily.insert(0, 0)
        
        return pd.DataFrame(daily)
    
    def fetch_population_data(self):
        df = pd.read_csv("Population.csv")
        df.index = df.State
        df.drop(["State"], axis=1, inplace=True)
        
        return df

class VaccineCalculator(BaseCalculator):
    def __init__(self):
        self.data = self.fetch_vaccine_data()
        self.population = self.fetch_population_data()
    
    def fetch_vaccine_data(self):
        df = pd.read_csv("http://api.covid19india.org/csv/latest/vaccine_doses_statewise.csv")
        df = df.transpose()
        new_header = df.iloc[0] 
        df.columns = new_header
        df.drop(df.head(1).index, inplace=True)
        df.drop(["Miscellaneous"], axis=1, inplace=True)
        df.rename(columns={'Total':'India'}, inplace=True)

        return df
    
    def get_herd_immunity_days(self, state, coverage=75, rolling_avg_days=14):
        state_data = self.data[state]
        population = int(self.population.loc[state])
        daily_doses = self.get_daily(state_data)
        
        daily_doses['MA'] = daily_doses.rolling(window=rolling_avg_days).mean()
        doses_given = int(state_data.iloc[state_data.shape[0]-1])
        vaccination_rate = daily_doses["MA"].iloc[-1]
        
        herd_population = population * (coverage/100)
        total_does_needed = herd_population*2
        doses_remaining = total_does_needed - doses_given
        
        return int(round(doses_remaining/vaccination_rate))

class DailyCasesCalculator(BaseCalculator):
    
    def __init__(self):
        self.data = self.fetch_case_data()
        self.population = self.fetch_population_data()
    
    def fetch_case_data(self):
        df = pd.read_csv('https://api.covid19india.org/csv/latest/states.csv')
        
        return df
    
    def get_daily_cases(self, state):
        df = self.data.loc[self.data['State']==state]
        daily_cases = self.get_daily(df['Confirmed'])
        
        return daily_cases
    
    def get_daily_tests(self, state):
        df = self.data.loc[self.data['State']==state]
        daily_tests = self.get_daily(df['Tested'])
        
        return daily_tests
    
    def get_current_cases_avg_100k(self, state):
        population = int(self.population.loc[state])
        daily_cases = self.get_daily_cases(state)
        ma = daily_cases.rolling(window=7).mean()
        
        daily_cases_avg = float(ma.iloc[-1])
        avg_100k = (daily_cases_avg/population) * 100000
        
        return round(avg_100k,1)
    
    def get_avg_pos_rate(self, state):
        daily_tests = self.get_daily_tests(state)
        daily_cases = self.get_daily_cases(state)
        
        avg_tests = daily_tests.rolling(window=7).sum()
        avg_cases = daily_cases.rolling(window=7).sum()
        
        pos_rate = (avg_cases.iloc[-1] / avg_tests.iloc[-1])*100

        if float(pos_rate) == float('inf'):
          return 'Not Avalilable'
        
        return round(float(pos_rate), 1)

vaccineCal = VaccineCalculator()
caseCal = DailyCasesCalculator()

states = vaccineCal.population.index.to_list()

data = []
for state in states:
    days = vaccineCal.get_herd_immunity_days(state, coverage=75, rolling_avg_days=14)
    cases = caseCal.get_current_cases_avg_100k(state)
    pos_rate = caseCal.get_avg_pos_rate(state)
    data.append({"Place":state, "Days":days, "Avg Cases":cases, "Avg Positivity Rate":pos_rate})

with open('data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
