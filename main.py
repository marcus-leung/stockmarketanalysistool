from data import DataGetter
from visual import showPlot
import pandas as pd

stock = 'AAPL'

d = DataGetter(stock)
json_content = d.getJSON()
showPlot(json_content)