from tkinter import Tk
from .GUIComponent import GUIComponent
from .SearchBar import SearchBar
from queue import Queue
from request_handlers.Request import Request
from json import loads as json_loads


class Application(Tk, GUIComponent):
    def __init__(self):
        super().__init__(baseName="OOPTecDummy")

        self.__response_queue = Queue()
        self.__genres = []

    def __request_genres(self):
        if len(self.__genres) > 0:
            return self.__genres

        request = Request(self.__response_queue, "genres")
        print("Obteniendo los géneros disponibles de {}".format(request.url))
        request.start()

        bad = False
        tmp_response = None
        while True: # this will block the main thread I know, but is the easy solution
            if not self.__response_queue.empty():
                tmp_response = self.__response_queue.get()
                if tmp_response == "sent":
                    print("Cargando...")
                elif tmp_response == "received":
                    print("Datos recibidos, cargando...")
                elif tmp_response == "error":
                    print("Algo salió bastante BASTANTE mal")
                    print("Verifica tu conexión a internet")
                    print("O, que el servidor esté prendido y a la escucha")
                    break
                elif tmp_response == "ok":
                    print("Datos cargados, continuando")
                    break

        if bad:
            print("NOOOO, algo no salió bien, no se puede continuar")
            exit(1)

        json_response = self.__response_queue.get()
        self.__genres = json_response["genres"] # the response contains: {genres: [array with genres]}
        return self.__genres

    # Override
    def init_components(self):
        self.__request_genres()

        search_bar = SearchBar(self, self.__genres)
        search_bar.init_components()
        search_bar.grid(row=0, column=0)

        self.grid_columnconfigure(0, weight=1)
