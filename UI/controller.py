import flet as ft
from UI.view import View
from model.modello import Model


class Controller:
    def __init__(self, view: View, model: Model):
        # the view, with the graphical elements of the UI
        self._view: View = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._inputLat = None
        self._inputLng = None

    def fillDDShape(self):

        shapes = self._model.getAllShapes()
        for i in shapes:
            self._view.ddshape.options.append(
                ft.dropdown.Option(i)
            )
        self._view.update_page()

    def handle_graph(self, e):

        if self._view.txt_latitude.value == "":
            self._view.create_alert("Selezionare un valore minimo di latitudine")
            self._view.update_page()
            return

        if self._view.txt_longitude.value == "":
            self._view.create_alert("Selezionare un valore minimo di longitudine")
            self._view.update_page()
            return

        if self._view.ddshape.value is None:
            self._view.create_alert("Selezionare una shape dal menu 'shapes'")
            self._view.update_page()
            return

        minLat, maxLat, minLng, maxLng = self._model.getLimitiLatLong()

        try:
            self._inputLat = float(self._view.txt_latitude.value)
            self._inputLng = float(self._view.txt_longitude.value)
        except ValueError:
            self._view.create_alert("E' necessario inserire un valore intero o decimale "
                                    "nei campi latitudine e longitudine")
            self._view.update_page()
            return

        if self._inputLat < minLat or self._inputLat > maxLat:
            self._view.create_alert(f"La latitudine deve essere compresa tra {minLat} e {maxLat}")
            self._view.update_page()
            return

        if self._inputLng < minLng or self._inputLng > maxLng:
            self._view.create_alert(f"La longitudine deve essere compresa tra {minLng} e {maxLng}")
            self._view.update_page()
            return

        self._model.buildGraph(self._inputLat, self._inputLng, self._view.ddshape.value)
        self._view.btn_path.disabled = False

        nNodi, nArchi = self._model.getGraphDetails()
        self._view.txt_result1.controls.append(
            ft.Text(f"Numero di vertici: {nNodi}\nNumero di archi: {nArchi}")
        )
        self._view.update_page()

        top5Degree = self._model.getTop5Nodes()

        if top5Degree:
            self._view.txt_result1.controls.append(
                ft.Text("I 5 nodi di grado maggiore sono:")
            )
            for n in top5Degree:
                self._view.txt_result1.controls.append(
                    ft.Text(f"{n[0]} --> degree: {n[1]}")
                )

            self._view.update_page()

        top5Edges = self._model.getTop5Edges()

        if top5Edges:
            self._view.txt_result1.controls.append(
                ft.Text("I 5 archi di peso maggiore sono:")
            )
            for n in top5Edges:
                self._view.txt_result1.controls.append(
                    ft.Text(f"{n[0]} <--> {n[1]} | peso = {n[2]["weight"]}")
                )

            self._view.update_page()

    def handle_path(self, e):
        cammino, punteggio = self._model.getCamminoOttimo()

        for i in cammino:
            self._view.txt_result2.controls.append(
                ft.Text(f"{i}")
            )
        self._view.txt_result2.controls.append(
            ft.Text(f"Punteggio: {punteggio}")
        )
        self._view.update_page()



