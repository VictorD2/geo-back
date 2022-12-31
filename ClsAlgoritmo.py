import pandas as pd
from ClsUtils import ClsUtils
from fastdtw import fastdtw
from scipy.spatial.distance import euclidean

days ={"Lunes":1,"Martes":2,"Miercoles":3,"Jueves":4,"Viernes":5,"Sabado":6}

class ClsAlgoritmo:
    
    df_datos=[]
    def __init__(self):
        print("Iniciando")
      
    def recoleccion(self,file):
        df_datos = pd.read_csv(file,  names=['latitud', 'longitud', 'hora', 'dia',"id_user"], sep=', ', engine='python')
        ClsAlgoritmo.df_datos=df_datos.drop(['id_user'], axis=1)

    def identificarRutas(self,df_temp):
        rutas = []
        ruta = 0
        UMBRAL_DISTANCIA = 0.000738128715050
        estado_anterior = False
        for i in range(len(df_temp)):
            try:
                x1 = df_temp.iloc[i, 0]
                y1 = df_temp.iloc[i, 1]
                x2 = df_temp.iloc[i + 1, 0]
                y2 = df_temp.iloc[i + 1, 1]
                distance = ClsUtils.getDistance(x1, y1, x2, y2)
                rutas.append(ruta)
                if((distance >= UMBRAL_DISTANCIA) != estado_anterior):
                    estado_anterior = distance >= UMBRAL_DISTANCIA
                    ruta = ruta + 1
                
                time1 = df_temp.iloc[i, 2]
                time2 = df_temp.iloc[i + 1, 2]
                if(abs(time1-time2) > 500):
                    ruta = ruta + 1
            except:
                rutas.append(ruta)
        rutas[0] = rutas[1]
        df_temp["Ruta"] = rutas
        return df_temp

    def preprocesamiento(self,df_temp):
        df_temp["hora"] = df_temp.hora.apply(ClsUtils.getMinutes)
        return df_temp

    def asignarSimilitud(self,df_temp, similares):
        df_temp["RutaSimilar"] = df_temp.Ruta
        contador_rutas = max(df_temp.Ruta) + 1
        for i in similares:
            df_temp["RutaSimilar"] = df_temp.RutaSimilar.apply(lambda x: x if x not in i else contador_rutas)
            contador_rutas = contador_rutas + 1
        return df_temp

    def findSimilar(self, df_temp):
        array_similares = []
        rutas = ClsUtils.separarRutas(df_temp)
        UMBRAL_SIMILAR = 1000
        tamanio = range(len(rutas))
        for i in tamanio:
            for j in tamanio:
            # Para que no se compare con rutas anteriormente comparadas
                if(i <= j):
                    continue
                
                if(len(rutas[i]) == 0 or len(rutas[j]) == 0):
                    continue
                # Buscando similitud con DTW
                distance, path = fastdtw(rutas[i], rutas[j], dist=euclidean)
                if(distance == 0):
                    continue

                if(distance < UMBRAL_SIMILAR):
                    array_similares.append([i,j])
        
        # Ordenamos
        array_similares = ClsUtils.sortMatrix(array_similares)
        array_agrupados = []

        if(len(array_similares) == 0):
            return array_agrupados
        i = 0

        # Agrupamos todos los elementos entre ellos
        while True:
            # Quitamos el primer elemento
            elemento = array_similares.pop(i)
            j = 0
            while True:
                if(j >= len(array_similares)):
                    break
                # Buscamos rutas similares en los demas elementos
                if(array_similares[j][0] in elemento or array_similares[j][1] in elemento):
                    # Encontrado, quitado y agregado al primer elemento quitado
                    comparador = array_similares.pop(j)
                    elemento = elemento + comparador
                else:
                    # Al no encontrar similares buscamos en la siguiente posicion
                    j = j + 1
                    if(j >= len(array_similares)):
                        break
            # Una vez unido se agregan a un arreglo
            array_agrupados.append(elemento)      
            if (len(array_similares) == 0):
                break
        return ClsUtils.sortMatrix(array_agrupados) 

    def getDatos(self,file):
        dfs=[]
        self.recoleccion(file)
        # Separando por dias
        for i in days:
            print("Día: {}".format(i))
            df_day = ClsUtils.getDataByDay(ClsAlgoritmo.df_datos,i)
            if(len(df_day) == 0):
                continue
            df_day= df_day.reset_index()
            df_day=df_day.drop(['index'], axis=1)
            print("Pre procesamiento")
            df_day = self.preprocesamiento(df_day)
            print("Identificando Rutas")
            df_day = self.identificarRutas(df_day)
            print("Encontrando Rutas Similares")
            similares = self.findSimilar(df_day)
            print(similares)
            print("Asignando Rutas Similares")
            df_day = self.asignarSimilitud(df_day, similares)
            print("Agregando al array")
            dfs.append(df_day.to_json(orient = "table"))    
        return dfs
