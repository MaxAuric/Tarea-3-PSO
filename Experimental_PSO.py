import matplotlib.pyplot as plt
import random
import math
import time
import csv  # Para exportar la tabla de rendimiento a CSV

# Parámetros para la prueba de rendimiento
tamanos_startups = [10, 50, 100, 500, 1000, 3000, 5000, 10000] 
resultados_tiempos = []  # Almacenar los tiempos de ejecución

# Función para generar parámetros del problema de forma aleatoria
def generar_parametros_problema(num_startups, capital_inicial):
    nombres_startups = [f'Startup {i+1}' for i in range(num_startups)]
    random.shuffle(nombres_startups)
    costos = [random.randint(10, 1000) for _ in range(num_startups)]
    rois = [round(random.uniform(0.1, 1), 2) for _ in range(num_startups)]
    limites = [(0, capital_inicial // costos[i]) for i in range(len(costos))]
    return nombres_startups, costos, rois, limites

# Suma de los ROIs ponderados por la cantidad invertida
def fncTotalROI(x, rois):
    total_roi = sum(x[i] * rois[i] for i in range(len(x)))
    return total_roi

# Penalización por superar el capital disponible
def fncPenalizarCosto(x, costos, capital_inicial):
    total_costo = sum(x[i] * costos[i] for i in range(len(x)))
    return total_costo - capital_inicial if total_costo > capital_inicial else 0

# Función objetivo
def fncMax(x, costos, rois, capital_inicial):
    return fncTotalROI(x, rois) - fncPenalizarCosto(x, costos, capital_inicial)

class Particula:
    def __init__(self, valores_iniciales):
        self.posicion = [valores_iniciales[i] for i in range(len(valores_iniciales))]
        self.velocidad = [random.uniform(-1, 1) for _ in range(len(valores_iniciales))]
        self.mejor_posicion = list(self.posicion)
        self.mejor_valor = -1

    def evaluar(self, funcion, costos, rois, capital_inicial):
        self.valor_actual = funcion(self.posicion, costos, rois, capital_inicial)
        if self.valor_actual > self.mejor_valor:
            self.mejor_valor = self.valor_actual
            self.mejor_posicion = list(self.posicion)

    def actualizar_velocidad(self, mejor_posicion_global, w=0.9, c1=0.6, c2=0.6):
        for i in range(len(self.posicion)):
            r1, r2 = random.random(), random.random()
            cognitivo = c1 * r1 * (self.mejor_posicion[i] - self.posicion[i])
            social = c2 * r2 * (mejor_posicion_global[i] - self.posicion[i])
            self.velocidad[i] = w * self.velocidad[i] + cognitivo + social

    def actualizar_posicion(self, limites):
        for i in range(len(self.posicion)):
            self.posicion[i] += self.velocidad[i]
            self.posicion[i] = max(limites[i][0], min(self.posicion[i], limites[i][1]))

class PSO:
    def __init__(self, funcion, valores_iniciales, limites, costos, rois, capital_inicial, num_particulas, max_iteraciones):
        self.mejor_valor_global = -1
        self.mejor_posicion_global = []
        self.particulas = [Particula(valores_iniciales) for _ in range(num_particulas)]
        for iteracion in range(max_iteraciones):
            for particula in self.particulas:
                particula.evaluar(funcion, costos, rois, capital_inicial)
                if particula.valor_actual > self.mejor_valor_global:
                    self.mejor_valor_global = particula.valor_actual
                    self.mejor_posicion_global = list(particula.posicion)
            for particula in self.particulas:
                particula.actualizar_velocidad(self.mejor_posicion_global)
                particula.actualizar_posicion(limites)

# PRUEBA DE RENDIMIENTO
for tamano in tamanos_startups:
    print(f"\nEjecutando PSO con {tamano} startups...")

    # Generar los parámetros del problema
    nombres_startups, costos, rois, limites = generar_parametros_problema(tamano, capital_inicial=10000)
    valores_iniciales = [0] * len(nombres_startups)

    # Medir el tiempo de ejecución
    tiempo_inicio = time.perf_counter()
    pso = PSO(fncMax, valores_iniciales, limites, costos, rois, capital_inicial=10000, num_particulas=5, max_iteraciones=5)
    tiempo_fin = time.perf_counter()
    tiempo_total = tiempo_fin - tiempo_inicio

    print(f"Tiempo de ejecución: {tiempo_total:.4f} segundos")
    resultados_tiempos.append([tamano, tiempo_total])

# Exportar los resultados a CSV
with open('rendimiento_pso.csv', 'w', newline='') as archivo_csv:
    escritor_csv = csv.writer(archivo_csv)
    escritor_csv.writerow(['Tamaño de startups', 'Tiempo de ejecución (segundos)'])
    escritor_csv.writerows(resultados_tiempos)

# Graficar los resultados de la prueba de rendimiento
tamanos, tiempos = zip(*resultados_tiempos)
plt.plot(tamanos, tiempos, marker='o')
plt.xlabel('Tamaño de las startups')
plt.ylabel('Tiempo de ejecución (segundos)')
plt.title('Prueba de rendimiento PSO')
plt.grid(True)
plt.show()
