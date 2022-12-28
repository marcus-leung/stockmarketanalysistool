from data import DataGetter
import pandas as pd

stock = 'TSLA'

d = DataGetter(stock, interval='DAILY')
d.showPlot()