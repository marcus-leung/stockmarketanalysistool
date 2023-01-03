from data import DataGetter
import pandas as pd

stock = 'TSLA'

d = DataGetter(stock, interval='60', high=True, low=True)
d.showPlot()