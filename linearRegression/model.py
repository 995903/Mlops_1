import pandas as pd
from pandas import DataFrame
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import pickle

df = pd.read_csv("3.2 cost_revenue_clean.csv.csv")

x = DataFrame(df, columns=['production_budget_usd'])
y = DataFrame(df, columns=['worldwide_gross_usd'])

regression = LinearRegression()
regression.fit(x, y)
pickle.dump(regression,open("model.pkl", 'wb'))
