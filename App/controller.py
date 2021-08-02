"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
import model
import csv
from DISClib.ADT import map as mp


"""
El controlador se encarga de mediar entre la vista y el modelo.
"""

# Inicialización del Catálogo de libros
def newAnalyzer():
    return model.newAnalyzer()
# Funciones para la carga de datos
def loadData(catalog):
    countriesName = cf.data_dir + 'countries.csv'
    countriesFile = csv.DictReader(open(countriesName, encoding="utf-8"),
                                delimiter=",")
    connectName = cf.data_dir + 'connections.csv'
    connectFile = csv.DictReader(open(connectName, encoding="utf-8"),
                                delimiter=",")
    landingsName = cf.data_dir + 'landing_points.csv'
    landingsFile = csv.DictReader(open(landingsName, encoding="utf-8"),
                                delimiter=",")
    counter = 0
    for line in landingsFile:
        model.addLanding(catalog,line)
        if counter ==0:
            print(f"La información del primer landing point es: {line}")
        counter += 1
    for con in connectFile:
        model.addLandConnection(catalog,con)
    for pais in countriesFile:
        lastName = pais['CountryName']
        model.addCountry(catalog,pais)
    lastCountryInfo = mp.get(catalog['countries'],lastName)['value']
    model.connectedComponents(catalog)
    print (f"Para el último país cargado, la población es {lastCountryInfo['Population']}, y los usuarios son {lastCountryInfo['Internet users']}")
    return catalog
# Funciones de ordenamiento

# Funciones de consulta sobre el catálogo

def requerimiento2 (analyzer,pais1,pais2):
    return model.requerimiento2(analyzer,pais1,pais2)
def req1(landing1,landing2,analyzer):
    return model.req1(landing1,landing2,analyzer)
def requerimiento3 (analyzer):
    return model.requerimiento3(analyzer)