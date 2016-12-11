# -*- coding: utf-8 -*-

import os
import sys
import evolutivo as ev
from py4j.java_gateway import JavaGateway
from config import NETLOGOMODEL, \
                    PLANFILE, \
                    PLANARRAY, \
                    createPlanFile

if __name__ == "__main__":
    try:
        numero_pruebas = int(sys.argv[1])
        print u"Total de evaluaciones a realizar por plan: ", sys.argv[1]
    except:
        numero_pruebas = 10
        print u"El número de pruebas a realizar será el por defecto (10 rondas)"
    gw = JavaGateway()  # New gateway connection
    bridge = gw.entry_point  # The actual NetLogoBridge object
    bridge.openModel(NETLOGOMODEL)
    for plan in PLANARRAY:
        print "ejecutando pruebas para ", plan
        createPlanFile(plan)
        posiciones = ev.obtenerPosiciones(PLANFILE)
        # en genes se guardan todas las posibles puertas
        genes = ev.obtenerGenes(posiciones)
        # generarArchivo(genes)

        individuos = ev.generarPoblacion(genes, 100)

        # aca especificamos el numero de generaciones
        for x in range(0, numero_pruebas):
            print "generacion: {0}".format(x)
            for individuo in individuos:
                # Ahora se supone que hay que evaluar cada uno de los
                # individuos para determinar el fitness de cada uno
                individuo.evaluar(bridge)

            individuos = ev.seleccionarIndividuos(individuos)
            mejor = individuos[0]
            print "mejor     : {0}".format(mejor.fitness)

            individuos = ev.reproducirIndividuos(individuos,bridge)

            individuos = ev.mutarIndividuos(individuos, genes, bridge)

        ev.generarDoors(mejor.genes, plan)