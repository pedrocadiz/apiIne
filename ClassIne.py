import datetime, requests
import matplotlib.pyplot as plt
import matplotlib.dates as plt_dates
import matplotlib.pyplot as plt_pyplot
from matplotlib.ticker import FormatStrFormatter
import statistics as sta
import numpy as np
from matplotlib.dates import date2num 

class IneApi:

    # Clase que ayuda a la descarga, transformacion y presentacion de los datos alojados en el INE (Tempus3).
    # Para obtener el codigo inicial se necesita ir a la pagina:
    # https://www.ine.es/dyngs/DataLab/manual.html?cid=66
    # SOLO funciona con series temporales, se necesita la variable Fecha o no funcionara.
        
    def __init__(self, codigo = "CP335", num_datos = 400):  
        # Inicializamos la clase, como predefinido se ha introducido el registro de Poblacion
        self.codigo = codigo
        self.num_datos = num_datos
        self.flag_regresion = False
        self.flag_prevision = False
           
    def download_raw_data(self):    
        # Descargamos los datos del INE
        url = f'http://servicios.ine.es/wstempus/js/ES/DATOS_SERIE/{self.codigo}?nult={self.num_datos}'
        respuesta = requests.get(url)
        self.raw = respuesta.json()
        
    def print_raw_data(self):
        # Por si se quiere inspeccionar el json directamente
        print(self.raw)
        
    def save_raw_data(self):
        # Guardar los datos brutos
        with open('raw_data.txt', 'w') as f: 
            f.write(str(self.raw))
            
    def load_raw_data(self,filename):
        # Cargar los datos brutos de un json
        print(filename)
        with open(filename, 'r') as f: 
            self.raw = f.read()
            
    def extract_data(self, campo = 'Valor'):
        # Extraemos los datos y las fechas requeridas, se divide entre 1000 porque solo nos interesa
        # el dia, no la hora.
        
        self.date = []
        self.data = []
        for x in self.raw['Data']:
            self.date.append(datetime.date.fromtimestamp(x['Fecha'] // 1000))
            self.data.append(x[campo])
      
    def basic_info(self):
        # Calculamos la media y la desviacion tipica
        self.st_dev = sta.stdev(self.data)
        self.mean = sta.mean(self.data)
        
    def get_st_dev(self):
        # getter de la desviacion tipica
        return self.st_dev
        
    def get_mean(self):
        # getter de la media
        return self.mean
        
    def polinomial_regression(self, grade = 1, points = 1000):
        # Ajustaremos los datos por minimos cuadrados al polinomio de grado <grade>
        self.grade = grade
        x = np.array(plt_dates.date2num(self.date))
        y = np.array(self.data)
        
        z = np.polyfit(x, y, self.grade)
        self.pol_y = np.poly1d(z)
        
        self.pol_x = np.linspace(x[0], x[-1], points)
        
        self.flag_regresion = True

    def prevision(self, days_into_future = 365):
        # A partir del polinomio calculado en polinomial_regression haremos una 
        # prediccion tan larga como <days_into_future> indique. Se realizara
        # una prediccion por dia.
        
        last_prediction = self.date[-1]+datetime.timedelta(days=days_into_future)
        self.pred_x = np.linspace(plt_dates.date2num(self.date[-1]),plt_dates.date2num(last_prediction),days_into_future)

        self.flag_prevision = True
        
    def plot_series(self):
        # Pintamos la info que tengamos
        fig, ax = plt.subplots()
        ax.yaxis.set_major_formatter(FormatStrFormatter('%0.0e'))
        plt.title(self.raw['Nombre'])

        if(self.flag_regresion == True):           
            if(self.flag_prevision == True):
                plt.plot(self.date, self.data, '.',self.pol_x,self.pol_y(self.pol_x),self.pred_x,self.pol_y(self.pred_x),'--')
                plt.legend(('Datos',f'Reg. pol. n = {self.grade}','Prediccion'),loc = 'lower right')
            else:
                plt.plot(self.date, self.data, '.',self.pol_x,self.pol_y(self.pol_x))
                plt.legend(('Datos',f'Reg. pol. n = {self.grade}'),loc = 'lower right')
        else:
            plt.plot(self.date, self.data, '.')
            
        plt.xlabel("Fecha")
        plt.ylabel("Datos")
        


        # Caja con informacion basica de la tabla
        props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
        ax.text( 0.05, 0.95, f'media = {self.mean:.2e}\n $\sigma$ = {self.st_dev:.2e}',transform=ax.transAxes, fontsize=8,verticalalignment='top',bbox=props)

        plt.show()

instancia = IneApi()

print(f'codigo = {instancia.codigo} num_datos = {instancia.num_datos}')

instancia.download_raw_data()
instancia.extract_data()
instancia.basic_info()
instancia.plot_series()

instancia.polinomial_regression(2)
instancia.prevision(365*5)
instancia.plot_series()




