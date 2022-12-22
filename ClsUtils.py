
days ={"Lunes":1,"Martes":2,"Miercoles":3,"Jueves":4,"Viernes":5,"Sabado":6}
import pandas as pd
import numpy as np
import math

class ClsUtils:

    def getDays(text):
        return days[text]

    def getMinutes(text):
        tiempo = text.split(":")
        minutos = int(tiempo[0])*60+int(tiempo[1])
        return minutos

    def getDataByDay(df,day):
        return df[df['dia'] == day]

    def getDistance(x1, y1, x2, y2):
        return math.sqrt(math.pow(abs(x2 - x1), 2) + math.pow(abs(y2 - y1), 2))

    def sortMatrix(matrix):
        sorted_array = []
        if(len(matrix) == 0):
            return []
        while True:
            elemento = matrix.pop()
            elemento = sorted(list(set(elemento)))
            sorted_array.append(elemento)
            if(len(matrix) == 0):
                break
        sorted_array = sorted(sorted_array)
        return sorted_array

    def separarRutas(df_temp):
        rutas_array = []
        ruta_minima = min(df_temp.Ruta)
        ruta_maxima = max(df_temp.Ruta) + 1
        i = ruta_minima
        while i < ruta_maxima:
            new_df = pd.DataFrame(df_temp[df_temp["Ruta"] == i])
            new_df = new_df.drop(['dia'], axis = 1)
            new_df = new_df.drop(['Ruta'], axis = 1)
            rutas_array.append(np.array(new_df))
            i = i + 1
        return rutas_array 

    