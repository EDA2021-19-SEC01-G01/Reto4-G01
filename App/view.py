"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
from DISClib.ADT import list as lt
from DISClib.ADT import graph as gr
from DISClib.ADT import map as mp
from DISClib.ADT import stack
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

def printMenu():
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- ")
    print("0- Salir")

catalog = None

"""
Menu principal
"""
while True:
    printMenu()
    inputs = input('Seleccione una opción para continuar\n')
    if int(inputs) == 1:
        print("Cargando información de los archivos ....")
        catalog = controller.newAnalyzer()
        catalog = controller.loadData(catalog)
        print (f"La cantidad de landing points es: {gr.numVertices(catalog['connections'])}")
        print (f"La cantidad de conexiones entre landing points es: {gr.numEdges(catalog['connections'])}")
        print (f"La cantidad de países es: {mp.size(catalog['countries'])}")

    elif int(inputs) == 2:
        pass

    elif int(inputs) == 3:
        pais1 = input("Ingrese el país 1: ")
        pais2 = input("Ingrese el país 2: ")
        rta = controller.requerimiento2(catalog,pais1,pais2)
        totalDist = 0
        while stack.isEmpty(rta) == False:
            escala = stack.pop(rta)
            print (f"{escala['vertexA']} -> {escala['vertexA']}. Distancia: {escala['weight']} km")
            totalDist += escala['weight']
        print (f"\nLa distancia total es de {totalDist} km")

    else:
        sys.exit(0)
sys.exit(0)
