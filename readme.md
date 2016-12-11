Para ejecutar la tarea de deben seguir los siguientes pasos:


1) Instalar la librería numpy de python mediante `sudo pip install numpy`


2) En la terminar ejecutar el archivo bridge.jar mediante java -jar bridge.jar


3) Cuando el programa bridge.jar indique "SERVER RUNNING", se puede ejecutar la aplicación de 2 formas.
    3.1) Se puede ejecutar el script fulltest.py de la siguiente manera `python fulltest.py <numero de ciclos>` situado en la carpeta correspondiente ne la línea de comandos.
    3.2) Se puede ejecutar el script fulltest.py de la siguiente manera `python evolutivo.py <numero de ciclos> <numero de plan>` situado en la carpeta correspondiente ne la línea de comandos.
    3.3) `<numero de ciclos>` Equivale al total de generaciones que se quieren crear para llegar a una solución final

        `<numero de plan>` Equivale al plan al cual se quiere utilizar, ubicados dentro del arreglo `[u'school.plan', u'conference.plan', u'office.plan']`

Para que funcione correctamente el archivo escape4.nlogo y el archivo .plan deben estar en el mismo directorio que el programa bridge.jar y evolutivo.py