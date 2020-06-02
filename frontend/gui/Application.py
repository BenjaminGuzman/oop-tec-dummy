from tkinter import Tk, TOP, X, Y, BOTH
from .GUIComponent import GUIComponent
from .SearchBar import SearchBar
from queue import Queue
from request_handlers import Request
from .Title import Title
from .SearchResults import SearchResults
from .Media import Media


class Application(Tk, GUIComponent):
    def __init__(self):
        super().__init__()

        self.__genres = []

    def __request_genres(self):
        if len(self.__genres) > 0:
            return self.__genres

        status_queue = Queue()
        request = Request(status_queue, "genres")
        print("Obteniendo los géneros disponibles de {}".format(request.url))
        request.start()

        bad = False
        tmp_response = None
        while True: # this will block the main thread I know, but is the easy solution
            if not status_queue.empty():
                tmp_response = status_queue.get()
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
                    print("Géneros obtenidos, datos cargados, continuando\n")
                    break

        if bad:
            print("NOOOO, algo no salió bien, no se puede continuar")
            exit(1)

        json_response = status_queue.get()
        self.__genres = json_response["genres"] # the response contains: {genres: [array with genres]}
        return self.__genres

    # Override
    def init_components(self):
        self.__request_genres()

        title = Title(self)
        title.init_components()
        title.pack(side=TOP, fill=X)

        search_bar = SearchBar(self, self.__genres)
        search_bar.init_components()
        search_bar.pack(side=TOP, fill=X)

        search_results = SearchResults(self)
        search_results.init_components()
        search_results.pack(side=TOP, fill=BOTH, expand=True)

        search_bar.search_results = search_results

        for row in range(1):
            self.grid_rowconfigure(row, weight=1)
        self.grid_rowconfigure(2, weight=15)

        for col in range(0 + 1):
            self.grid_columnconfigure(col, weight=1)

        Media.init_defaults()
