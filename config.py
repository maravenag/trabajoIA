# -*- coding: utf-8 -*-
import os
from shutil import copyfile
#se hace un join entre el espacio de trabajo y el nombre del archivo a buscar
workspace = u""

dirname = os.path.dirname(__file__) if workspace != u"" else workspace

PLANARRAY = [u'school.plan', u'conference.plan', u'office.plan']
DOORS = os.path.abspath(os.path.join(dirname, u"doors.plan"))
SOLUTIONS = os.path.abspath(os.path.join(dirname, u"soluciones.plan"))
NETLOGOMODEL = os.path.abspath(os.path.join(dirname, u"escape4.nlogo"))
PLANFILE = os.path.abspath(os.path.join(dirname, u"plan.plan"))

def doorsFile(path):
	return os.path.abspath(os.path.join(dirname, u'_'.join([u"doors", path]) ))

def createPlanFile(file):
	copyfile(file,"plan.plan")
