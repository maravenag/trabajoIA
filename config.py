# -*- coding: utf-8 -*-
import os
#se hace un join entre el espacio de trabajo y el nombre del archivo a buscar
workspace = u""

dirname = os.path.dirname(__file__) if workspace != u"" else workspace

DOORS = os.path.abspath(os.path.join(dirname, u"doors.plan"))
SOLUTIONS = os.path.abspath(os.path.join(dirname, u"soluciones.plan"))
NETLOGOMODEL = os.path.abspath(os.path.join(dirname, u"escape4.nlogo"))