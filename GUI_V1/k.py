import pandas as pd
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as Canvas

Canvas.

df = pd.DataFrame(columns=['wpt','lat','lon','ele'])
df = df.append({'wpt': "1", 'lat': 2, 'lon':2, 'ele':0},ignore_index=True)
df = df.append({'wpt': "1", 'lat': 2, 'lon':2, 'ele':0},ignore_index=True)
df = df.append({'wpt': "3", 'lat': 2, 'lon':2, 'ele':0},ignore_index=True)

print(df)
print(df.index)
df.set_index('wpt',inplace=True)
print(df)
data= df[["lat"]]
print(data.values.tolist())