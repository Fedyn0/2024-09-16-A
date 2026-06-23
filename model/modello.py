import copy

from database.DAO import DAO
import networkx as nx


from model import state

class Model:
    def __init__(self):
        self._bestCammino = None
        self._bestScore = 0
        self._grafo = nx.Graph()
        self._idMapState = {}
        self._idMapSighting = {}
        for sighting in DAO.get_all_sightings():
            self._idMapSighting[sighting.id] = sighting

    def getLimitiLatLong(self):
        limiti = DAO.getMinMaxLimit()
        minLat = limiti[0][0]
        maxLat = limiti[0][1]
        minLng = limiti[0][2]
        maxLng = limiti[0][3]
        return minLat, maxLat, minLng, maxLng

    def getAllShapes(self):
        return DAO.getAllShapes()

    def buildGraph(self, lat, long, shape):
        nodi = DAO.getAllNodes(lat, long, shape)
        self._grafo.add_nodes_from(nodi)
        for node in nodi:
            self._idMapState[node.id] = node

        print(len(nodi))

        archi = DAO.getAllEdges(lat, long, shape, self._idMapState)


        for u, v in archi:
            counterTot = 0
            counterU = 0
            counterV = 0
            for sighting in self._idMapSighting.values():
                if u.id.lower() == sighting.state.lower() and sighting.shape == shape:
                    counterU += sighting.duration
                if v.id.lower() == sighting.state.lower() and sighting.shape == shape:
                    counterV += sighting.duration
            counterTot += counterU + counterV
            self._grafo.add_edge(u, v, weight=counterTot)


    def getGraphDetails(self):
        return len(self._grafo.nodes), len(self._grafo.edges)

    def getTop5Edges(self):
        archi = list(self._grafo.edges(data = True))
        archi.sort(key = lambda x : x[2]["weight"], reverse = True)
        return archi[0:5]

    def getTop5Nodes(self):

        lista = list(self._grafo.degree())
        lista.sort(key = lambda x : x[1], reverse = True)
        return lista[0:5]

    def getCamminoOttimo(self):
        self._bestCammino =[]
        self._bestScore = 0

        parziale = []

        for node in self._grafo.nodes():
            parziale.append(node)
            self._ricorsione(parziale)
            parziale.pop()

        return self._bestCammino, self._bestScore

    def _ricorsione(self, parziale):
        #verifico se parziale è una soluzione valida,ed in caso la salvo
        if len(parziale) > 1:
            if self._getScore(parziale) > self._bestScore:
                self._bestCammino = copy.deepcopy(parziale)
                self._bestScore = self._getScore(parziale)


        #espando parziale e faccio ricorsione con backtracking
        for n in self._grafo.neighbors(parziale[-1]):
            if self._getDensita(parziale[-1]) < self._getDensita(n):
                parziale.append(n)
                self._ricorsione(parziale)
                parziale.pop()

    def _getScore(self, parziale):
        sumPesi = 0
        distanza = 0
        for i in range(0, len(parziale)-1):
            distanza += parziale[i].distance_HV(parziale[i+1])
            sumPesi += (self._grafo[parziale[i]][parziale[i+1]]["weight"])
        return sumPesi / distanza

    def _getDensita(self, node):
        densita = node.Population / node.Area
        return densita