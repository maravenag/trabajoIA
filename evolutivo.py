# -*- coding: utf-8 -*-

import random
import sys
import numpy as np
from config import DOORS, SOLUTIONS, NETLOGOMODEL
from py4j.java_gateway import JavaGateway


class Posicion():

    def __init__(self, x, y, tipo):
        self.x = x
        self.y = y
        self.tipo = tipo

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def obtenerVecinos(self, posiciones):
        # A partir de un punto dado, determina cuales son los vecinos.
        vecinos = []
        for p in posiciones:
            if self.x + 1 == p.x and self.y == p.y:
                vecinos.append(p)
            if self.x - 1 == p.x and self.y == p.y:
                vecinos.append(p)
            if self.y - 1 == p.y and self.x == p.x:
                vecinos.append(p)
            if self.y + 1 == p.y and self.x == p.x:
                vecinos.append(p)
        return vecinos


class Individuo():

    def __init__(self, genes):
        self.fitness = 0
        self.genes = []
        # almacenamos los genes en una lista simple de numeros
        for g in range(0, 10):
            self.genes.append(genes[g])

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def evaluar(self, bridge):
        # Esta funcion es la que deberia calcular el fitness del individuo
        # donde el fitness esta dado por el valor de ticks de la simulacion

        generarDoors(self.genes)
        bridge.command("load-fixed-plan-file")
        bridge.command("load-fixed-door-file")
        bridge.command("generate-population")
        bridge.command("repeat 200 [ go ]")
        self.fitness = bridge.report("ticks")


def obtenerPosiciones(file):
    posiciones = []
    with open(file, 'r') as f:
        for line in f:
            line = line.replace("\n", "")
            line = line.split(' ')
            m = Posicion(int(line[0]), int(line[1]), int(line[2]))
            posiciones.append(m)
    return posiciones


def obtenerGenes(posiciones):
    genes = []
    for punto in posiciones:
        if punto.tipo == 64:
            if validarPunto(punto, posiciones):
                genes.append(punto)
    return genes


def generarArchivo(genes):
    doors = open(DOORS, "w")
    for x in range(0, 5):
        punto = genes[random.randrange(0, len(genes))]
        doors.write("{0} {1} \n".format(punto.x, punto.y))
    doors.close()
    print "Generado puertas"

    sol = open(SOLUTIONS, "w")
    for x in range(0, len(genes)):
        punto = genes[x]
        sol.write("{0} {1} \n".format(punto.x, punto.y))
    sol.close()
    print "Generado soluciones"


def validarPunto(punto, posiciones):
    # retorna si un punto es valido como como posible puerta
    vecinos = punto.obtenerVecinos(posiciones)

    if len(vecinos) < 4:
        # descartamos los puntos que estan en los bordes
        return False
    else:
        # Muro izquierdo
        if vecinos[1].tipo == 2 and vecinos[2].tipo == 0:
            return True
        # Muros inferiores
        elif vecinos[3].tipo == 2 and vecinos[0].tipo == 0:
            return True
        # Muros superiores
        elif vecinos[0].tipo == 2 and vecinos[3].tipo == 0:
            return True
        # Muros derechos
        elif vecinos[1].tipo == 0 and vecinos[2].tipo == 2:
            return True
        # Cualquier otro caso.
        else:
            return False


def generarPoblacion(genes, poblacion):
    # retorna una lista de Individuos
    individuos = []
    for x in range(0, poblacion):
        genes_individuo = asignarGenes(genes)
        individuo = Individuo(genes_individuo)
        individuos.append(individuo)
    return individuos


def asignarGenes(genes):
    # retorna los genes del individuo, y verifica que los genes no se repitan.
    rango = len(genes)
    genes_individuo = []
    n_genes = 0

    lista_genes = []
    lista_genes.append(genes[random.randrange(0, rango)])
    for x in range(0, 4):
        continua = True
        while continua:
            gen = genes[random.randrange(0, rango)]
            if gen in lista_genes:
                continua = True
            else:
                lista_genes.append(gen)
                continua = False
    for x in range(0, len(lista_genes)):
        genes_individuo.append(lista_genes[x].x)
        genes_individuo.append(lista_genes[x].y)
    return genes_individuo


def ordenarIndividuos(individuos):
    # Ordenamos los individuos y luego asignamos la categoria
    # Para luego seleccionarlos en la ruleta.
    individuos = sorted(
        individuos, key=lambda individuo: individuo.fitness, reverse=False)
    return individuos


def seleccionarIndividuos(individuos):
    # Aca hay que seleccionar el metodo de seleccion de los individuos
    # Seleccionar los n mejores individuos que pasaran al crossover.
    individuos = ordenarIndividuos(individuos)
    seleccionados = []
    # Seleccionamos siempre al mejor de cada generacion
    seleccionados.append(individuos[0])

    weights = [0.5, 0.25, 0.15, 0.1]
    for x in range(1, 30):
        sigue = True
        while sigue:
            choices = [random.randrange(1, 50), random.randrange(
                51, 75), random.randrange(76, 90), random.randrange(90, 100)]
            rnd = np.random.choice(choices, p=weights)
            seleccionado = individuos[rnd]
            if seleccionado in seleccionados:
                sigue = True
            else:
                seleccionados.append(individuos[rnd])
                sigue = False
    return seleccionados


def cruzar(padre, madre):
    # Cruzamos dos individuos, falta verificar que no se repitan los genes.
    continua = True
    while continua: #<--- este while es inutil, nunca pasa de 1 iteración, esa es la idea o no D:?
        pos = random.randrange(0, 5)  # randrange (0, n-1)
        if pos == 0:
            pos = 2
        else:
            pos = 2 * pos

        genes_hijo1 = []
        for x in range(0, pos):
            genes_hijo1.append(padre.genes[x])

        for x in range(pos, 10):
            genes_hijo1.append(madre.genes[x])

        genes_hijo2 = []
        for x in range(0, pos):
            genes_hijo2.append(madre.genes[x])

        for x in range(pos, 10):
            genes_hijo2.append(padre.genes[x])
        continua = False

    hijos = []
    hijo1 = Individuo(genes_hijo1)
    hijo2 = Individuo(genes_hijo2)
    hijos.append(hijo1)
    hijos.append(hijo2)
    return hijos


def reproducirIndividuos(individuos):
    # Hay un 75% de probabilidades que un individuo se reproduzca
    nueva_poblacion = individuos
    choices = ["RP", "NP"]
    weights = [0.25, 0.75]
    n_individuos = len(nueva_poblacion)

    while n_individuos < 99:

        rnd = np.random.choice(choices, p=weights)
        # tomamos un padre y madre aleatorio
        padre = nueva_poblacion[random.randrange(0, n_individuos - 1)]
        madre = nueva_poblacion[random.randrange(0, n_individuos - 1)]

        if rnd == "RP":
            hijos = cruzar(padre, madre)
            nueva_poblacion.append(hijos[0])
            nueva_poblacion.append(hijos[1])
            n_individuos = n_individuos + 2
        else:
            pass

    return nueva_poblacion


def mutarIndividuos(individuos, genes):
    # Mutar con probabilidad de 0.01 algun gen de un individuo
    choices = ["M", "N"]
    weights = [0.05, 0.95]
    mutados = []
    for i in individuos:
        rnd = np.random.choice(choices, p=weights)
        if rnd == "M":
            pos = random.randrange(0, 5)  # randrange (0, n-1)
            continua = True
            while continua:
                iguales = 0
                gen = genes[random.randrange(0, len(genes))]
                for x in range(0, 5):
                    if gen.x != i.genes[2 * x] and gen.y != i.genes[(2 * x) + 1]:
                        iguales = iguales
                    else:
                        iguales = iguales + 1

                if iguales == 0:
                    continua = False
                    i.genes[2 * pos] = gen.x
                    i.genes[2 * pos + 1] = gen.y
                else:
                    continua = True

            mutados.append(i)
        else:
            mutados.append(i)

    return mutados


def generarDoors(genes):
    # modificado por qe ahora debe funcionar con una lista simple
    doors = open(DOORS, "w")
    for x in range(0, 10):
        doors.write("{0} ".format(genes[x]))
        if x in [1, 3, 5, 7, 9]:
            doors.write("\n")
    doors.close()


if __name__ == "__main__":

    gw = JavaGateway()  # New gateway connection
    bridge = gw.entry_point  # The actual NetLogoBridge object
    bridge.openModel(NETLOGOMODEL)

    posiciones = obtenerPosiciones(sys.argv[1])
    # en genes se guardan todas las posibles puertas
    genes = obtenerGenes(posiciones)
    # generarArchivo(genes)

    individuos = generarPoblacion(genes, 200)

    # aca especificamos el numero de generaciones
    for x in range(0, 6):
        print "generacion: {0}".format(x)
        for individuo in individuos:
            # Ahora se supone que hay que evaluar cada uno de los
            # individuos para determinar el fitness de cada uno
            # conectando la wea de netlogo
            individuo.evaluar(bridge)
        individuos = seleccionarIndividuos(individuos)

        individuos2 = ordenarIndividuos(individuos)
        print individuos2[0].fitness

        individuos = reproducirIndividuos(individuos)

        individuos = mutarIndividuos(individuos, genes)

    generarDoors(individuos[0].genes)
