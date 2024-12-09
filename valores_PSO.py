import matplotlib.pyplot as plt
import random
import math

# Parámetros del problema
nombres_startups = ['Startup 1', 'Startup 2', 'Startup 3']
costos = [9000, 4000, 7000]  # Costos de inversión (c1, c2, ..., cn)
rois = [15000, 11000, 10000]  # Retorno de la inversión (ROI) proyectado para cada startup
capital_inicial = 15000  # Capital inicial disponible
r_values = [0.8, 0.92, 0.53, 0.34, 0.41, 0.72, 0.27, 0.84, 0.96, 0.5, 0.67, 0.91, 0.4, 0.14, 0.28, 0.72, 0.44, 0.38, 0.86, 0.77, 0.9, 0.4, 0.29, 0.47, 0.34, 0.58, 0.75, 0.94, 0.5, 0.48, 0.95, 0.44, 0.98, 0.77, 0.54, 0.74, 0.45, 0.91, 0.12, 0.25, 0.48, 0.95, 0.23, 0.57, 0.17, 0.3, 0.75, 0.17, 0.36, 0.38, 0.1, 0.32, 0.81, 0.6, 0.06, 0.45, 0.11, 0.07, 0.82, 0.72, 0.73, 0.41, 0.7, 0.23, 0.41, 0.77, 0.1, 0.67, 0.64, 0.1, 0.87, 0.99, 0.72, 0.34, 0.88, 0.07, 0.19, 0.66, 0.12, 0.58, 0.76, 0.8, 0.04, 0.99, 0.82, 0.92, 0.11, 0.77, 0.74, 0.37, 0.65, 0.23, 0.93, 0.35, 0.91, 0.85, 0.73, 0.79, 0.88, 0.85, 0.53, 0.36, 0.4, 0.8, 0.64, 0.5, 0.37, 0.76, 0.41, 0.22, 0.12, 0.5, 0.1, 0.16, 0.89, 0.51, 0.67, 0.19, 0.4, 0.44, 0.28, 0.53, 0.42, 0.44, 0.8, 0.57, 0.49, 0.64, 0.51, 0.84, 0.72, 0.24, 0.87, 0.79, 0.15, 0.67, 0.68, 0.29, 0.55, 0.53, 0.76, 0.26, 0.63, 0.09, 0.13, 0.72, 0.38, 0.6, 0.49, 0.47, 0.13, 0.17, 0.52, 0.25, 0.89, 0.35, 0.58, 0.6, 0.2, 0.87, 0.66, 0.66, 0.74, 0.33, 0.04, 0.78, 0.52, 0.55, 0.2, 0.57, 0.7, 0.29, 0.6, 0.37, 0.13, 0.42, 0.04, 0.54, 0.74, 0.35,0.53, 0.36, 0.4, 0.8, 0.64, 0.5, 0.37, 0.76, 0.41, 0.22, 0.12, 0.5, 0.1, 0.16, 0.89, 0.51, 0.67, 0.19, 0.4, 0.44, 0.28, 0.53, 0.42, 0.44, 0.8, 0.57, 0.49, 0.64, 0.51, 0.84, 0.72, 0.24, 0.87, 0.79, 0.15, 0.67, 0.68, 0.29, 0.55, 0.53, 0.76, 0.26, 0.63, 0.09, 0.13, 0.72, 0.38, 0.6, 0.49, 0.47, 0.13, 0.17, 0.52, 0.25, 0.89, 0.35, 0.58, 0.6, 0.2, 0.87, 0.66, 0.66, 0.74, 0.33, 0.04, 0.78, 0.52, 0.55, 0.2, 0.57, 0.7, 0.29, 0.6, 0.37, 0.13, 0.42, 0.04, 0.54, 0.74, 0.35]

# Función objetivo: Maximizar el ROI total
def fncMax(x):
    return fncTotalROI(x) - fncPenalizarCosto(x)

# Suma de los ROIs ponderados por la cantidad invertida
def fncTotalROI(x):
    total_roi = 0
    for i in range(len(x)):
        total_roi += x[i] * rois[i]  # Cantidad de inversión * ROI
    return total_roi

# Penalización por superar el capital disponible
def fncPenalizarCosto(x):
    total_costo = 0
    for i in range(len(x)):
        total_costo += x[i] * costos[i]  # Cantidad de inversión * costo de la startup
    if total_costo > capital_inicial:
        return total_costo - capital_inicial  # Penalización por superar el capital
    else:
        return 0

class Particula:
    def __init__(self, valores_iniciales):
        self.posicion = []  # Posición de la partícula
        self.velocidad = []  # Velocidad de la partícula
        self.mejor_posicion = []  # Mejor posición individual
        self.mejor_valor = -1  # Mejor valor individual
        self.valor_actual = -1  # Valor de la posición actual

        for i in range(len(valores_iniciales)):
            self.velocidad.append(random.uniform(-1, 1))
            self.posicion.append(valores_iniciales[i])

    def evaluar(self, funcion):
        self.valor_actual = funcion(self.posicion)
        if self.valor_actual > self.mejor_valor or self.mejor_valor == -1:
            self.mejor_posicion = list(self.posicion)
            self.mejor_valor = self.valor_actual

    def actualizar_velocidad(self, mejor_posicion_global, w=0.9, c1=0.6, c2=0.6):
        for i in range(len(self.posicion)):
            if i + 1 < len(r_values):
                r1 = r_values[i]
                r2 = r_values[i + 1]
                #r1_index = i % len(r_values)
                #r2_index = (i + 1) % len(r_values)
                #r1 = r_values[r1_index]
                #r2 = r_values[r2_index]
                
                componente_cognitiva = c1 * r1 * (self.mejor_posicion[i] - self.posicion[i])
                componente_social = c2 * r2 * (mejor_posicion_global[i] - self.posicion[i])
                
                self.velocidad[i] = w * self.velocidad[i] + componente_cognitiva + componente_social

    def actualizar_posicion(self, limites):
        for i in range(len(self.posicion)):
            max_salto = (limites[i][1] - limites[i][0])
            if self.velocidad[i] < -max_salto:
                self.velocidad[i] = -max_salto
            elif self.velocidad[i] > max_salto:
                self.velocidad[i] = max_salto

            self.posicion[i] = self.posicion[i] + self.velocidad[i]

            if self.posicion[i] > limites[i][1]:
                self.posicion[i] = limites[i][1]
            elif self.posicion[i] < limites[i][0]:
                self.posicion[i] = limites[i][0]
            else:
                self.posicion[i] = round(self.posicion[i])

class PSO:
    def __init__(self, funcion, valores_iniciales, limites, num_particulas, max_iteraciones):
        self.mejor_valor_global = -1
        self.mejor_posicion_global = []
        self.historico_roi = []

        self.particulas = [Particula(valores_iniciales) for _ in range(num_particulas)]

        for iteracion in range(max_iteraciones):
            for particula in self.particulas:
                particula.evaluar(funcion)
                if particula.valor_actual > self.mejor_valor_global or self.mejor_valor_global == -1:
                    self.mejor_posicion_global = list(particula.posicion)
                    self.mejor_valor_global = particula.valor_actual

            for particula in self.particulas:
                particula.actualizar_velocidad(self.mejor_posicion_global)
                particula.actualizar_posicion(limites)

            total_roi = fncTotalROI(self.mejor_posicion_global)
            self.historico_roi.append(total_roi)
            print(f"Iteración {iteracion+1}: Mejor ROI = {total_roi}")

    def mostrar_resultados(self):
        print("\nRESULTADOS:")
        total_costo = 0
        total_roi = 0
        for i in range(len(self.mejor_posicion_global)):
            cantidad_invertida = self.mejor_posicion_global[i]
            print(f"{nombres_startups[i]}: {cantidad_invertida} unidades invertidas")
            total_costo += cantidad_invertida * costos[i]
            total_roi += cantidad_invertida * rois[i]
        print(f"Total invertido: {total_costo} de un máximo de {capital_inicial}")
        print(f"ROI total: {total_roi}\n")

    def graficar_resultados(self, nombre_archivo=""):
        plt.plot(self.historico_roi)
        plt.xlabel('Iteración')
        plt.ylabel('ROI Total')
        plt.title('Evolución del ROI Total')
        plt.grid(True)

        if nombre_archivo:
            plt.savefig(nombre_archivo + ".png")
        plt.show()
        plt.close()

# Parámetros iniciales
valores_iniciales = [0] * len(nombres_startups)
limites = [(0, capital_inicial // costos[i]) for i in range(len(costos))]  # Limitar la inversión por startup

print('[Startup: límite inferior - límite superior]')
for i in range(len(nombres_startups)):
    print(f"{nombres_startups[i]}: {limites[i][0]} - {limites[i][1]}")
print(f"\nTotal de {len(nombres_startups)} startups disponibles.\n")

# Crear y ejecutar el PSO
pso = PSO(fncMax, valores_iniciales, limites, num_particulas=5, max_iteraciones=5)
pso.mostrar_resultados()
pso.graficar_resultados(nombre_archivo='resultado_pso')