import sys
import random
import numpy as np

class Posicion:
	def __init__(self,x,y,tipo):
		self.x = x
		self.y = y
		self.tipo = tipo

	def imprimir(self):
		print "x:{0} y:{1} tipo:{2}".format(self.x, self.y, self.tipo)
	
	def obtenerVecinos(self, posiciones):
		#A partir de un punto dado, determina cuales son los vecinos.
		vecinos = []
		for p in posiciones:
			if self.x + 1 == p.x and self.y == p.y:
				vecinos.append(p)
			if self.x - 1 == p.x and self.y ==p.y:
				vecinos.append(p)
			if self.y - 1 == p.y and self.x == p.x:
				vecinos.append(p)
			if self.y +1 == p.y and self.x == p.x:
				vecinos.append(p)
		return vecinos

class Individuo:
	def __init__(self,genes):
		self.fitness = 0
		self.genes = []
		#almacenamos los genes en una lista simple de numeros
		for g in range(0,10):
			self.genes.append(genes[g])
	
	def evaluar(self):
		#Esta funcion es la que deberia calcular el fitness del individuo
		#donde el fitness esta dado por el valor de ticks de la simulacion
		self.fitness = random.randrange(30,300)

def obtenerPosiciones(file):

	posiciones = []
	with open(file,'r') as f:
		for line in f:
			line = line.replace("\n","")
			line = line.split(' ')
			m = Posicion(int(line[0]),int(line[1]),int(line[2]))
			posiciones.append(m)
	return posiciones

def obtenerGenes(posiciones):
	genes = []
	for punto in posiciones:
		if  punto.tipo == 64:
			if(validarPunto(punto, posiciones) == True):
				genes.append(punto)
	return genes

def generarArchivo(genes):

	doors = open("doors.plan","w")
	for x in range(0,5):
		punto = genes[random.randrange(0,len(genes))]
		doors.write("{0} {1} \n".format(punto.x,punto.y))
	doors.close()
	print "Generado doors.plan"

	sol = open("soluciones.plan","w")
	for x in range(0, len(genes)):
		punto = genes[x]
		sol.write("{0} {1} \n".format(punto.x,punto.y))
	sol.close()
	print "Generado soluciones.plan"

def validarPunto(punto, posiciones):
	#retorna si un punto es valido como como posible puerta
	vecinos = punto.obtenerVecinos(posiciones)

	if len(vecinos) < 4:
		#descartamos los puntos que estan en los bordes
		return False
	else:
		#Muro izquierdo
		if (vecinos[1].tipo == 2 and vecinos[2].tipo == 0):
			return True
		#Muros inferiores
		elif (vecinos[3].tipo == 2 and vecinos[0].tipo == 0):
			return True
		#Muros superiores
		elif (vecinos[0].tipo == 2 and vecinos[3].tipo == 0):
			return True
		#Muros derechos
		elif (vecinos[1].tipo == 0 and vecinos[2].tipo == 2):
			return True
		#Cualquier otro caso.
		else:
			return False

def generarPoblacion(genes, poblacion):
	#retorna una lista de Individuos
	individuos = []
	rango = len(genes)
	for x in range(0,poblacion):
		genes_individuo =[]
		for y in range(0,5):
			gen = genes[random.randrange(0,rango)]
			genes_individuo.append(gen.x)
			genes_individuo.append(gen.y)
		individuo = Individuo(genes_individuo) 
		individuos.append(individuo)
	return individuos

def ordenarIndividuos(individuos):
	#Ordenamos los individuos y luego asignamos la categoria
	#Para luego seleccionarlos en la ruleta.
	individuos = sorted(individuos, key=lambda individuo: individuo.fitness, reverse = False) 
	return individuos

def seleccionarIndividuos(individuos):
	#Aca hay que seleccionar el metodo de seleccion de los individuos
	#Seleccionar los n mejores individuos que pasaran al crossover.
	individuos = ordenarIndividuos(individuos)
	seleccionados = []
	#Seleccionamos siempre al mejor de cada generacion
	seleccionados.append(individuos[0])
	
	weights = [0.5,0.25,0.15,0.1]
	for x in range(1,30):
		choices = [random.randrange(1,50),random.randrange(51,75),random.randrange(76,90),random.randrange(90,100)]
		rnd = np.random.choice(choices, p=weights)
		#falta aun verificar que no se repita el individuo (?)
		seleccionados.append(individuos[rnd])
	return seleccionados

def recombinacion_un_punto(padre,madre):
	pos = random.randrange(0,5) #randrange (0, n-1)
	if(pos == 0):
		pos = 2
	else:
		pos = 2*pos
	
	genes_hijo1 = []
	for x in range(0,pos):
		genes_hijo1.append(padre.genes[x])

	for x in range(pos,10):
		genes_hijo1.append(madre.genes[x])

	genes_hijo2 = []
	for x in range(0,pos):
		genes_hijo2.append(madre.genes[x])

	for x in range(pos,10):
		genes_hijo2.append(padre.genes[x])
	hijos = []
	hijo1 = Individuo(genes_hijo1)
	hijo2 = Individuo(genes_hijo2)
	hijos.append(hijo1)
	hijos.append(hijo2)
	return hijos


def reproducirIndividuos(individuos):
	#Hay un 75% de probabilidades que un individuo se reproduzca
	nueva_poblacion = individuos
	choices = ["RP","NP"]
	weights = [0.25,0.75]
	n_individuos = len(nueva_poblacion)
	
	while(n_individuos < 99):
		
		rnd = np.random.choice(choices, p=weights)
		#tomamos un padre y madre aleatorio
		padre = nueva_poblacion[random.randrange(0,n_individuos-1)]
		madre = nueva_poblacion[random.randrange(0,n_individuos-1)]

		if (rnd == "RP"):
			hijos = recombinacion_un_punto(padre,madre)
			nueva_poblacion.append(hijos[0])
			nueva_poblacion.append(hijos[1])
			n_individuos = n_individuos + 2
		else:
			pass

	return nueva_poblacion

def mutarIndividuos(individuos):
	#Mutar con probabilidad de 0.01 algun gen de un individuo
	choices = ["MUTAR","NOMUTAR"]
	weights = [0.05,0.95]
	for i in individuos:
		rnd = np.random.choice(choices, p=weights)
		if (rnd == "MUTAR"):
			print "MU"
		else:
			print "NOMU"


def generarDoors(genes):
	#modificado por qe ahora debe funcionar con una lista simple
	doors = open("doors.plan","w")
	for x in range(0,10):
		doors.write("{0} ".format(genes[x]))
		if x in [1,3,5,7,9]:
			doors.write("\n")
	doors.close()
	print "Generado: doors.plan"

if __name__ == "__main__":

	posiciones = obtenerPosiciones(sys.argv[1])
	genes = obtenerGenes(posiciones)
	#generarArchivo(genes)
	individuos = generarPoblacion(genes,100)
	
	for individuo in individuos:
		#Ahora se supone que hay que evaluar cada uno de los individuos para determinar el fitness de cada uno
		individuo.evaluar()
		#print individuo.fitness
	
	individuos = seleccionarIndividuos(individuos)
	individuos = reproducirIndividuos(individuos)
	#for i in individuos:
	#	print i.genes
	mutarIndividuos(individuos)