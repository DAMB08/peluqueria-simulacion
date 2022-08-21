import math
import random

import simpy

# almacena los tiempos en espera de cada cliente
lista_tiempo_espera_total = []
# almacena en tiempo total del servicio de cada cliente
lista_duracion_servicio_total = []
# almacena en tiempo de llegada  de cada cliente
lista_tiempo_llegada_cliente = []
# almacena en tiempo que sale el cliente
lista_salida_cliente = []

tiempo_espera_total = 0.0  # tiempo de espera total
duracion_servicio_total = 0.0  # duración de servicio total
fin = 0.0  # minuto en el que finaliza


def crearEntorno(SEMILLA, CANTIDAD_PELUQUEROS, TIEMPO_CORTE_MAX,
                 TIEMPO_CORTE_MIN, TOTAL_CLIENTES, T_LLEGADAS):

    random.seed(SEMILLA)  # Cualquier valor
    entorno = simpy.Environment()  # Crea el objeto entorno de simulación
    # Crea los recursos para ejecutar la simulación
    personal = simpy.Resource(entorno, CANTIDAD_PELUQUEROS)
    correrSimulacion(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS,
                     TIEMPO_CORTE_MAX, TIEMPO_CORTE_MIN)


def correrSimulacion(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS, TIEMPO_CORTE_MAX,
                     TIEMPO_CORTE_MIN):
    # Invoca la función princial
    entorno.process(principal(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS,
                              TIEMPO_CORTE_MAX,
                              TIEMPO_CORTE_MIN))
    entorno.run()  # Inicia la simulación


def principal(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS, TIEMPO_CORTE_MAX,
              TIEMPO_CORTE_MIN):
    llegada = 0
    i = 0
    for i in range(TOTAL_CLIENTES):  # Para cantidad clientes
        R = random.random()
        llegada = -T_LLEGADAS * math.log(R)  # Distribución exponencial
        # Deja transcurrir un tiempo entre uno y otro
        yield entorno.timeout(llegada)
        i += 1
        entorno.process(cliente(entorno,  personal, TIEMPO_CORTE_MAX,
                                TIEMPO_CORTE_MIN))


def cortar(entorno, TIEMPO_CORTE_MAX, TIEMPO_CORTE_MIN):
    """Para poder acceder a la variable duracion_servicio_total 
    declarada anteriormente """

    global duracion_servicio_total
    R = random.random()  # Obtiene un número aleatorio y lo guarda en R
    tiempo = TIEMPO_CORTE_MAX - TIEMPO_CORTE_MIN
    tiempo_corte = TIEMPO_CORTE_MIN + (tiempo*R)  # Distribución uniforme
    lista_duracion_servicio_total.append(tiempo_corte)
    yield entorno.timeout(tiempo_corte)  # deja correr el tiempo en minutos
    # Acumula los tiempos de uso del cliente
    duracion_servicio_total = duracion_servicio_total + tiempo_corte


def cliente(entorno,  personal, TIEMPO_CORTE_MAX,
            TIEMPO_CORTE_MIN):
    global tiempo_espera_total
    global fin
    llega = entorno.now  # Guarda el minuto de llegada del cliente
    lista_tiempo_llegada_cliente.append(llega)
    with personal.request() as request:  # Espera su turno
        yield request  # Obtiene turno
        pasa = entorno.now  # Guarda el minuto cuando comienza a ser atendido
        espera = pasa - llega  # Calcula el tiempo que espero
        # Acumula los tiempos de espera
        tiempo_espera_total = tiempo_espera_total + espera
        lista_tiempo_espera_total.append(tiempo_espera_total)
        # Invoca la función cortar
        yield entorno.process(cortar(entorno,  TIEMPO_CORTE_MAX, TIEMPO_CORTE_MIN))
        deja_cortar = entorno.now  # Guarda el minuto en que termina el proceso cortar
        lista_salida_cliente.append(deja_cortar)
        # Conserva globalmente el último minuto de la simulación
        fin = deja_cortar


# retonar lista de datos
def obtenerTiempoEspera():
    return lista_tiempo_espera_total


def obtenerLlegadaCliente():
    return lista_tiempo_llegada_cliente


def obtenerDuracionServicio():
    return lista_duracion_servicio_total


def obtenerSalidaCliente():
    return lista_salida_cliente
