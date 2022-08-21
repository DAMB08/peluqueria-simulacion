
from tkinter import *
from tkinter import messagebox, ttk

import matplotlib.pyplot as plt

from simulador_peluqueria import *


class Peluqueria():
    def __init__(self) -> None:
        self.principal = Tk()
        self.principal.title('SIMULADOR PELUQUERÍA')
        self.principal.geometry('900x500')
        self.mainWindow = ttk.Frame(self.principal, padding=20)
        self.mainWindow.grid()

        # variables de entrada de los Entry
        self.semilla = StringVar()
        self.cantidadPeluqueros = StringVar()
        self.tiempoMaximo = StringVar()
        self.tiempoMinimo = StringVar()
        self.tiempoLlegada = StringVar()
        self.totalClientes = StringVar()

        # lista de datos a utilizar
        self.listaClientes = []
        self.listaEsperaCliente = []
        self.listaLlegadaCliente = []
        self.listaDuracionServicio = []
        self.listaSalidaCliente = []
        self.componentes()

    def componentes(self):
        ttk.Label(self.mainWindow, text="Semilla").grid(column=0, row=0)
        ttk.Entry(self.mainWindow, textvariable=self.semilla).grid(
            column=1, row=0)
        ttk.Label(self.mainWindow, text="Cantidad Peluqueros").grid(
            column=0, row=1)
        ttk.Entry(self.mainWindow, textvariable=self.cantidadPeluqueros).grid(
            column=1, row=1)
        ttk.Label(self.mainWindow, text="Tiempo Máximo").grid(column=0, row=2)
        ttk.Entry(self.mainWindow, textvariable=self.tiempoMaximo).grid(
            column=1, row=2)
        ttk.Label(self.mainWindow, text="Tiempo Minímo").grid(column=0, row=3)
        ttk.Entry(self.mainWindow, textvariable=self.tiempoMinimo).grid(
            column=1, row=3)

        ttk.Label(self.mainWindow, text="Tiempo Llegadas").grid(
            column=2, row=1)
        ttk.Entry(self.mainWindow, textvariable=self.tiempoLlegada).grid(
            column=3, row=1)
        ttk.Label(self.mainWindow, text="Total Cliente").grid(column=2, row=2)
        ttk.Entry(self.mainWindow, textvariable=self.totalClientes).grid(
            column=3, row=2)

        # botones
        ttk.Button(self.mainWindow, text='Ejecutar Simulación',
                   command=self.obtenerDatos).grid(
            column=0, row=4)
        ttk.Button(self.mainWindow, text='Mostrar Gráficos',
                   command=self.generarGraficos,
                   ).grid(
            column=1, row=4)

    def obtenerDatos(self):
        if (self.semilla.get() and
                self.cantidadPeluqueros.get() and
                self.tiempoMaximo.get() and
                self.tiempoMinimo.get() and
                self.totalClientes.get() and
                self.tiempoLlegada.get()
                ):
            self.listaClientes = []
            crearEntorno(int(self.semilla.get()),
                         int(self.cantidadPeluqueros.get()),
                         int(self.tiempoMaximo.get()),
                         int(self.tiempoMinimo.get()),
                         int(self.totalClientes.get()),
                         int(self.tiempoLlegada.get())
                         )

            for index in range(int(self.totalClientes.get())):
                self.listaClientes.append('{0}'.format(index+1))

            print(self.listaClientes)
        else:
            messagebox.showwarning('AVISO', 'Debes ingresar los datos')

    def generarGraficos(self):

        self.listaEsperaCliente = obtenerTiempoEspera()
        self.listaLlegadaCliente = obtenerLlegadaCliente()
        self.listaDuracionServicio = obtenerDuracionServicio()
        self.listaSalidaCliente = obtenerSalidaCliente()

        if (len(self.listaEsperaCliente) == 0 and
           len(self.listaLlegadaCliente) == 0 and
           len(self.listaDuracionServicio) == 0 and
           len(self.listaSalidaCliente) == 0):

            messagebox.showwarning('AVISO', 'Debes ejecutar la simulación')
        else:
            # gráfica de la lista en espera
            plt.subplot(1, 2, 1)
            plt.bar(self.listaClientes, self.listaEsperaCliente)
            plt.title('Tiempos espera  de los clientes')
            plt.xlabel('Clientes')
            plt.ylabel('Tiempo(Minutos)')
            plt.grid()

            # gráfica de la lista de llegada
            plt.subplot(1, 2, 2)
            plt.bar(self.listaClientes, self.listaLlegadaCliente)
            plt.title('Tiempos llegada  de los clientes')
            plt.xlabel('Clientes')
            plt.ylabel('Tiempo(Minutos)')
            plt.grid()

            plt.show()

            plt.subplot(1, 2, 1)
            plt.bar(self.listaClientes, self.listaDuracionServicio)
            plt.title('Tiempos duración  del servicio')
            plt.xlabel('Clientes')
            plt.ylabel('Tiempo(Minutos)')
            plt.grid()

            # gráfica de la lista de los tiempos de salida de los clientes
            plt.subplot(1, 2, 2)
            plt.bar(self.listaClientes, self.listaSalidaCliente)
            plt.title('Tiempos salida  del cliente')
            plt.xlabel('Clientes')
            plt.ylabel('Tiempo(Minutos)')
            plt.grid()
            plt.show()

            # se limpian los datos
        self.listaEsperaCliente.clear()
        self.listaLlegadaCliente.clear()
        self.listaDuracionServicio.clear()
        self.listaSalidaCliente.clear()

    def limpiar(self):
        self.listaEsperaCliente.clear()
        self.listaLlegadaCliente.clear()
        self.listaDuracionServicio.clear()
        self.listaSalidaCliente.clear()

    def run(self):
        self.principal.mainloop()


pelu = Peluqueria()
pelu.run()
