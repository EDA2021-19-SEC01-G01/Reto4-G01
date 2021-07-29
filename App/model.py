﻿"""
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config
from DISClib.ADT.graph import gr
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as djk
from DISClib.Utils import error as error
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
assert config
import math

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos
def newAnalyzer():
    """ Inicializa el analizador

   stops: Tabla de hash para guardar los vertices del grafo
   connections: Grafo para representar las rutas entre países
   components: Almacena la informacion de los componentes conectados
   paths: Estructura que almancena los caminos de costo minimo desde un
           vertice determinado a todos los otros vértices del grafo
    """
    analyzer = {
                'landings': None,
                'connections': None,
                'countries': None,
                }

    analyzer['landings'] = mp.newMap(numelements=1280,maptype='PROBING',comparefunction=compareLandingIds)

    analyzer['connections'] = gr.newGraph(datastructure='ADJ_LIST',directed=True,size=3263,comparefunction=compareLandingIds)
        
    analyzer['countries'] = mp.newMap(numelements=237,maptype='PROBING',comparefunction=compareLandingIds)

    return analyzer

# Funciones para agregar informacion al catalogo
def addLandConnection(analyzer,way):
    """
    Adiciona las estaciones al grafo como vertices y arcos entre las
    estaciones adyacentes.

    Los vertices tienen por nombre el identificador de la estacion
    seguido de la ruta que sirve. 
    """

    origin = way["\ufefforigin"]
    dictorg = mp.get(analyzer['landings'],origin)['value']
    coord1 = (float(dictorg['latitude']),float(dictorg['longitude']))
    destination =way["destination"]
    dictdest = mp.get(analyzer['landings'],destination)['value']
    coord2 = (float(dictdest['latitude']),float(dictdest['longitude']))
    distance = points2distance(coord1,coord2)
    addLand(analyzer, origin)
    addLand(analyzer, destination)
    addConnection(analyzer, origin, destination,distance)

def addLand(analyzer, landid):
    """
    Adiciona una estación como un vertice del grafo
    """
    if not gr.containsVertex(analyzer['connections'],landid):
        gr.insertVertex(analyzer['connections'], landid)

def addConnection(analyzer, origin, destination,distance):
    """
    Adiciona un arco entre dos estaciones
    """
    edge = gr.getEdge(analyzer['connections'], origin, destination)
    if edge is None:
        gr.addEdge(analyzer['connections'], origin, destination,distance)

def addLanding(analyzer,line):
    if mp.contains(analyzer['landings'],line['landing_point_id']) == False:
        mp.put(analyzer['landings'],line['landing_point_id'],line)

def addCountry(analyzer,pais):
    mp.put(analyzer['countries'],pais['CountryName'],pais)

# Funciones de consulta

def points2distance(start,  end):
    """
    Calculate distance (in kilometers) between two points given as (long, latt) pairs
    based on Haversine formula (http://en.wikipedia.org/wiki/Haversine_formula).
    Implementation inspired by JavaScript implementation from http://www.movable-type.co.uk/scripts/latlong.html
    Accepts coordinates as tuples (deg, min, sec), but coordinates can be given in any form - e.g.
    can specify only minutes:
    (0, 3133.9333, 0) 
    is interpreted as 
    (52.0, 13.0, 55.998000000008687)
    which, not accidentally, is the lattitude of Warsaw, Poland.
    """
    start_long = math.radians(start[0])
    start_latt = math.radians(start[1])
    end_long = math.radians(end[0])
    end_latt = math.radians(end[1])
    d_latt = end_latt - start_latt
    d_long = end_long - start_long
    a = math.sin(d_latt/2)**2 + math.cos(start_latt) * math.cos(end_latt) * math.sin(d_long/2)**2
    c = 2 * math.asin(math.sqrt(a))
    return 6371 * c

# Funciones utilizadas para comparar elementos dentro de una lista

def compareLandingIds(landing, keyvalueland):
    """
    Compara dos cosas
    """
    landcode = keyvalueland['key']
    if (landing == landcode):
        return 0
    else:
        return 1


# Funciones de ordenamiento
