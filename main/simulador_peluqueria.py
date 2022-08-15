import math
import random

import simpy

"""
SEMILLA = 30
CANTIDAD_PELUQUEROS = 5
TIEMPO_CORTE_MIN = 15
TIEMPO_CORTE_MAX = 30
T_LLEGADAS = 20
TIEMPO_SIMULACION = 120
TOTAL_CLIENTES = 20
    """

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
    # Crea los recursos (peluqueros)
    personal = simpy.Resource(entorno, CANTIDAD_PELUQUEROS)
    correrSimulacion(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS,
                     TIEMPO_CORTE_MAX, TIEMPO_CORTE_MIN)


def cortar(cliente, entorno, TIEMPO_CORTE_MAX, TIEMPO_CORTE_MIN):
    """Para poder acceder a la variable duracion_servicio_total 
    declarada anteriormente """

    global duracion_servicio_total
    R = random.random()  # Obtiene un número aleatorio y lo guarda en R
    tiempo = TIEMPO_CORTE_MAX - TIEMPO_CORTE_MIN
    tiempo_corte = TIEMPO_CORTE_MIN + (tiempo*R)  # Distribucion uniforme
    lista_duracion_servicio_total.append(tiempo_corte)
    yield entorno.timeout(tiempo_corte)  # deja correr el tiempo en minutos
    print(" \o/ Corte listo a %s en %.2f minutos" % (cliente, tiempo_corte))
    # Acumula los tiempos de uso de la i
    duracion_servicio_total = duracion_servicio_total + tiempo_corte


def cliente(entorno, cliente, personal, TIEMPO_CORTE_MAX,
            TIEMPO_CORTE_MIN):
    global tiempo_espera_total
    global fin
    llega = entorno.now  # Guarda el minuto de llegada del cliente
    lista_tiempo_llegada_cliente.append(llega)
    print("---> %s llego a peluqueria en minuto %.2f" % (cliente, llega))
    with personal.request() as request:  # Espera su turno
        yield request  # Obtiene turno
        pasa = entorno.now  # Guarda el minuto cuando comienza a ser atendido
        espera = pasa - llega  # Calcula el tiempo que espero
        # Acumula los tiempos de espera
        tiempo_espera_total = tiempo_espera_total + espera
        lista_tiempo_espera_total.append(tiempo_espera_total)
        print("**** %s pasa con peluquero en minuto %.2f habiendo esperado %.2f" %
              (cliente, pasa, espera))
        # Invoca al proceso cortar
        yield entorno.process(cortar(cliente, entorno,  TIEMPO_CORTE_MAX, TIEMPO_CORTE_MIN))
        deja_cortar = entorno.now  # Guarda el minuto en que termina el proceso cortar
        lista_salida_cliente.append(deja_cortar)
        print("<--- %s deja peluqueria en minuto %.2f" %
              (cliente, deja_cortar))
        fin = deja_cortar  # Conserva globalmente el ultimo minuto de la simulacion


def principal(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS, TIEMPO_CORTE_MAX,
              TIEMPO_CORTE_MIN):
    llegada = 0
    i = 0
    for i in range(TOTAL_CLIENTES):  # Para n clientes
        R = random.random()
        llegada = -T_LLEGADAS * math.log(R)  # Distribución exponencial
        # Deja transcurrir un tiempo entre uno y otro
        yield entorno.timeout(llegada)
        i += 1
        entorno.process(cliente(entorno, 'Cliente %d' % i, personal, TIEMPO_CORTE_MAX,
                                TIEMPO_CORTE_MIN))


def correrSimulacion(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS, TIEMPO_CORTE_MAX,
                     TIEMPO_CORTE_MIN):
    # Invoca el proceso princial
    entorno.process(principal(entorno, personal, TOTAL_CLIENTES, T_LLEGADAS,
                              TIEMPO_CORTE_MAX,
                              TIEMPO_CORTE_MIN))
    entorno.run()  # Inicia la simulacion

# retonar lista de datos


def obtenerTiempoEspera():
    return lista_tiempo_espera_total


def obtenerLlegadaCliente():
    return lista_tiempo_llegada_cliente


def obtenerDuracionServicio():
    return lista_duracion_servicio_total


def obtenerSalidaCliente():
    return lista_salida_cliente


"""print('lista en espera:\n', lista_tiempo_espera_total)
print('tiempo llegada cliente\n', lista_tiempo_llegada_cliente)
print('duracion del servicio\n', lista_duracion_servicio_total)
print('salida cliente\n', lista_salida_cliente)
"""
