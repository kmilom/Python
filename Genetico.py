import random
import matplotlib.pyplot as plt
import pandas as pd
import time
from collections import Counter

# Cargamos los datos del archivo de Excel
df = pd.read_excel('Mochila_capacidad_maxima_4kg.xlsx')

# Extraemos los pesos, valores y cantidades
identificadores = df['Id'].values
pesos = df['Peso_kg'].values
valores = df['Valor'].values
cantidades = df['Cantidad'].values

# Definimos peso máximo de la mochila
pesoMax = 4

# Parámetros del algoritmo
generaciones = 100
tasaCruzamiento = 0.99
tasaMutacion = 0.15
tamPoblacion = 20
tamElite = 4
convergencia = []
poblacion = []  # Variable global para almacenar la población final

# Generación de la población
def generarPoblacion(tam):
    poblacion = []
    for i in range(tam):
        cromosoma = [random.randint(0, cantidades[j]) for j in range(len(pesos))]
        poblacion.append(cromosoma)
    return poblacion

def calcularPeso(cromosoma):
    return sum([pesos[i] * cromosoma[i] for i in range(len(pesos))])

# Cálculo de la aptitud para cada cromosoma
def aptitud(cromosoma):
    pesoTotal = calcularPeso(cromosoma)
    valorTotal = sum([valores[i] * cromosoma[i] for i in range(len(valores))])
    if pesoTotal > pesoMax:
        return 0
    else:
        return valorTotal

# Restricción de peso para los cromosomas
def restringirPeso(cromosoma):
    pesoTotal = calcularPeso(cromosoma)
    while pesoTotal > pesoMax:
        indice = random.randint(0, len(cromosoma) - 1)
        if cromosoma[indice] > 0:
            cromosoma[indice] -= 1
            pesoTotal -= pesos[indice]

# Cruce de dos cromosomas padres
def cruce(padre1, padre2):
    hijo1 = [min(padre1[i], padre2[i]) for i in range(len(padre1))]
    hijo2 = [max(padre1[i], padre2[i]) for i in range(len(padre1))]
    return hijo1, hijo2

# Mutación de un cromosoma
def mutacion(cromosoma):
    for i in range(len(cromosoma)):
        if random.random() < tasaMutacion:
            cantidadDisponible = cantidades[i]
            cromosoma[i] = random.randint(0, cantidadDisponible)

# Selección de un cromosoma mediante torneo
def torneo(poblacion, tamTorneo):
    torneo = random.sample(poblacion, tamTorneo)
    mejorCromosoma = None
    mejorAptitud = -1
    for cromosoma in torneo:
        aptitudCromosoma = aptitud(cromosoma)
        if aptitudCromosoma > mejorAptitud:
            mejorCromosoma = cromosoma
            mejorAptitud = aptitudCromosoma
    return mejorCromosoma


def calcularConvergencia(convergencia):
    valorMax = max(convergencia)
    primerAparecion = convergencia.index(valorMax)
    return primerAparecion

# Algoritmo genético
def algoritmoGenetico(tamPoblacion, tasaMutacion, tasaCruzamiento, tamElite, generaciones):
    global poblacion  # Permitir acceso a la variable global
    
    poblacion = generarPoblacion(tamPoblacion)
    elite = []
    start = time.time()
    converge = False
    convergenciaMax = 0
    
    for i in range(generaciones):
        # Seleccionar padres para la reproducción
        padre1 = torneo(poblacion, 2)
        padre2 = torneo(poblacion, 2)
        
        # Cruzar y mutar a los padres para obtener hijos
        hijo1, hijo2 = cruce(padre1, padre2)
        mutacion(hijo1)
        mutacion(hijo2)
        restringirPeso(hijo1)
        restringirPeso(hijo2)
        
        # Actualizar la población con los hijos si son mejores que los peores individuos
        aptitudes = [aptitud(cromosoma) for cromosoma in poblacion]
        min_aptitud_index = aptitudes.index(min(aptitudes))
        
        if aptitud(hijo1) > aptitudes[min_aptitud_index]:
            poblacion[min_aptitud_index] = hijo1
            
        min_aptitud_index = aptitudes.index(min(aptitudes))
        if aptitud(hijo2) > aptitudes[min_aptitud_index]:
            poblacion[min_aptitud_index] = hijo2
        
        # Guardar élite
        elite.extend(sorted(poblacion, key=aptitud, reverse=True)[:tamElite])
        
        # Mantener solo los individuos únicos en élite
        elite = list(set(map(tuple, elite)))
        elite = [list(x) for x in elite]
        
        # Actualizar la población con élite
        poblacion = elite + poblacion[tamElite:]
        
        # Registro de convergencia
        convergencia.append(max(aptitudes))
        
        # Verificación de convergencia

        """if len(set(convergencia)) == 1:
            if not converge:
                convergenciaMax = i + 1
                converge = True
        else:
            converge = False"""
        
    return max(aptitudes), time.time() - start, convergencia

# Ejecutar el algoritmo genético
mejorAptitud, crono, listaConvergencia = algoritmoGenetico(tamPoblacion, tasaMutacion, tasaCruzamiento, tamElite, generaciones)

contador = Counter(listaConvergencia)


# Obtener la mejor mochila generada por el mejor cromosoma
aptitudes = [aptitud(cromosoma) for cromosoma in poblacion]
index_mejor = aptitudes.index(max(aptitudes))
mejorMochila = poblacion[index_mejor]

# Imprimir la mejor mochila
"""print("Mejor mochila:")
for i, gen in enumerate(mejor_mochila):
    if gen > 0:
        print(f"Objeto {identificadores[i]} - Peso: {pesos[i]} kg - Valor: {valores[i]} - Cantidad: {gen}")"""

# Mostrar resultados
print(f"Mejor aptitud encontrada: {mejorAptitud}")
print(f"Tiempo total de ejecución: {crono} s")
print(f"Iteración de convergencia: {calcularConvergencia(convergencia)}")
print("Mejor mochila:", mejorMochila)
print("Peso:", calcularPeso(mejorMochila))

# Graficar la convergencia
plt.plot(convergencia)
plt.title("Convergence chart")
plt.xlabel("Generation")
plt.ylabel("Fitness")
plt.show()
