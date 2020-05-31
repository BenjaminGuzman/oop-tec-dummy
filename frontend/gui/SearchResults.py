from tkinter import Frame, Label, LEFT, RIGHT, BOTH
from .GUIComponent import GUIComponent
from .Episode import Episode
from .Movie import Movie
from .ScrollBarPanel import ScrollBarPanel
from exceptions import MissingProperty


class SearchResults(Frame, GUIComponent):
    def __init__(self, master):
        super().__init__(master)

        self.__cb_search_serie = None
        self.__movies_panel = None
        self.__episodes_panel = None

    def init_components(self, *args, **kwargs):
        self.__movies_panel = ScrollBarPanel(self, "Realiza una búsqueda")
        self.__episodes_panel = ScrollBarPanel(self, "Realiza una búsqueda")

        self.__movies_panel.init_components("Películas")
        self.__episodes_panel.init_components("Episodios")

        # self.__movies_panel.grid(row=0, column=0)
        # self.__episodes_panel.grid(row=0, column=1)

        # self.grid_columnconfigure(0, weight=1)
        # self.grid_columnconfigure(1, weight=1)
        self.__movies_panel.pack(side=LEFT, fill=BOTH, expand=True)
        self.__episodes_panel.pack(side=RIGHT, fill=BOTH, expand=True)

    def insert_episode_results(self, results):
        self.__insert_results(False, results)

    def insert_movie_results(self, results):
        self.__insert_results(True, results)

    def __insert_results(self, is_movie, results):
        cls = None
        panel = None
        callback_query_serie = None
        if is_movie:
            cls = Movie
            panel = self.__movies_panel
        else:
            cls = Episode
            callback_query_serie = self.query_serie
            panel = self.__episodes_panel

        if len(results) == 0:
            panel.show_message()
            panel.message("No hay resultados para esa búsqueda")
            panel.reset()
            return
        panel.hide_message()
        panel.reset()
        panel.add_items(cls, results, callback_query_serie)

    @property
    def cb_search_serie(self):
        return self.__cb_search_serie

    @cb_search_serie.setter
    def cb_search_serie(self, cb):
        self.__cb_search_serie = cb

    def query_serie(self, serie_id):
        if self.__cb_search_serie is None:
            raise MissingProperty("cb_search_serie", self)

        self.__cb_search_serie(serie_id)