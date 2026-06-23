from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass


    @staticmethod
    def get_all_states():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from state s"""
            cursor.execute(query)

            for row in cursor:
                result.append(
                    State(**row))

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_all_sightings():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select * 
                    from sighting s 
                    order by `datetime` asc """
            cursor.execute(query)

            for row in cursor:
                result.append(Sighting(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllNodes(lat, lng, shape):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct st.*
                from state st, sighting si
                where st.id =  si.state
                and st.lat > %s and st.lng > %s
                and si.shape = %s"""

            cursor.execute(query, (lat, lng, shape))

            for row in cursor:
                result.append(State(**row))
            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getMinMaxLimit():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select min(s.latitude) as minLat, max(s.latitude) as maxLat, 
                              min(s.longitude) as minLng, max(s.longitude) as maxLng
                    from sighting s """

            cursor.execute(query,)

            for row in cursor:
                result.append((row["minLat"], row["maxLat"], row["minLng"], row["maxLng"]))
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllShapes():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct shape
                from sighting s 
                where shape != "" """

            cursor.execute(query,)

            for row in cursor:
                result.append(row["shape"])
            cursor.close()
            cnx.close()

        return result

    @staticmethod
    def getAllEdges(lat, lng, shape, idMapState):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """select distinct st1.id as st1, st2.id as st2
                from state st1, sighting si1,
                    state st2, sighting si2, neighbor n 
                where st1.id =  si1.state
                and st1.lat > %s and st1.lng > %s
                and si1.shape = %s
                and st2.id =  si2.state
                and st2.lat > %s and st2.lng > %s
                and si2.shape = %s
                and st1.id < st2.id
                and ((n.state1 = st1.id and n.state2 = st2.id)
                    or 
                    (n.state1 = st2.id and n.state2 = st1.id))"""

            cursor.execute(query, (lat, lng, shape, lat, lng, shape))

            for row in cursor:
                stato1 = idMapState[row["st1"]]
                stato2 = idMapState[row["st2"]]
                result.append((stato1, stato2))

            cursor.close()
            cnx.close()
        return result

