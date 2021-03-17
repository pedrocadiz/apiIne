import datetime, requests
import matplotlib.pyplot as plt
import matplotlib.dates as plt_dates
import matplotlib.pyplot as plt_pyplot
from matplotlib.ticker import FormatStrFormatter
import statistics as sta
import numpy as np
from matplotlib.dates import date2num 

# Este archivo es igual que classIne.py pero en formato script

# Introducir datos de la tabla
codigo = "CP335"
num_datos = 400

# Recuperacion datos del INE

url_plantilla = f'http://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{codigo}?nult={num_datos}'
respuesta = requests.get(url_plantilla)
raw = respuesta.json()


# Extracción de datos
print(raw['Nombre'])
date = []
data = []
for x in raw['Data']:
    date.append(datetime.date.fromtimestamp(x['Fecha'] // 1000))
    data.append(x['Valor'])

# Operaciones con los datos

# basicas
st_dev = sta.stdev(data)
mean = sta.mean(data)

# regresiones

x = np.array(plt_dates.date2num(date))
y = np.array(data)

z1 = np.polyfit(x, y, 1)
z4 = np.polyfit(x, y, 4)
z5 = np.polyfit(x, y, 3)

p1 = np.poly1d(z1)
p4 = np.poly1d(z4)

p5 = np.poly1d(z5)

xp = np.linspace(x[0], x[-1], 10000)



# Mostramos la info
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FormatStrFormatter('%0.0e'))
plt.title(raw['Nombre'])
plt.plot(date, data, '.', xp, p1(xp), xp, p4(xp))
plt.xlabel("Fecha")
plt.ylabel("Datos")
plt.legend(('Datos','Reg. lineal','Reg. n = 4'),loc = 'lower right')

# Caja con informacion basica de la tabla
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text( 0.05, 0.95, f'media = {mean:.2e}\n $\sigma$ = {st_dev:.2e}',transform=ax.transAxes, fontsize=8,
        verticalalignment='top',bbox=props)

#plt.axis([0, 6, 0, 20])
plt.show()


# Prevision

days_into_future = 3650
last_prediction = date[-1]+datetime.timedelta(days=days_into_future)
prediction_days = np.linspace(plt_dates.date2num(date[-1]),plt_dates.date2num(last_prediction),days_into_future)


# Mostramos la info
fig, ax = plt.subplots()
ax.yaxis.set_major_formatter(FormatStrFormatter('%0.0e'))
plt.title(raw['Nombre'])
plt.plot(date, data, '.', xp, p5(xp), prediction_days,p5(prediction_days),'--')
plt.xlabel("Fecha")
plt.ylabel("Datos")
plt.legend(('Datos','Reg. lineal','Reg. n = 4'),loc = 'lower right')

# Caja con informacion basica de la tabla
props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
ax.text( 0.05, 0.95, f'media = {mean:.2e}\n $\sigma$ = {st_dev:.2e}',transform=ax.transAxes, fontsize=8,
        verticalalignment='top',bbox=props)

#plt.axis([0, 6, 0, 20])
plt.show()
