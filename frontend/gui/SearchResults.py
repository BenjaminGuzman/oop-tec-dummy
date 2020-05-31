from tkinter import Frame, Label, LEFT, RIGHT, BOTH
from .GUIComponent import GUIComponent
from .Episode import Episode
from .Movie import Movie
from .ScrollBarPanel import ScrollBarPanel


class SearchResults(Frame, GUIComponent):
    def __init__(self, master):
        super().__init__(master)

        self.__movies_panel = None
        self.__episodes_panel = None

    def init_components(self, *args, **kwargs):
        self.__movies_panel = ScrollBarPanel(self, "Realiza una búsqueda", background="red")
        self.__episodes_panel = ScrollBarPanel(self, "Realiza una búsqueda", background="green")

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
        if is_movie:
            cls = Movie
            panel = self.__movies_panel
        else:
            cls = Episode
            panel = self.__episodes_panel

        if len(results) == 0:
            panel.show_message()
            panel.message("No hay resultados para esa búsqueda")
            return
        panel.hide_message()
        panel.reset()
        panel.add_items(cls, results)

"""
class SearchResults(PanedWindow, GUIComponent):
    def __init__(self, master):
        super().__init__(master, background="red")
        self.__curr_row = 0

        self.__temporary_label = Label(self, text="Realiza una búsqueda")
        self.__temporary_label.grid(row=0, column=0, padx=10, pady=10)

        self.__temporary_label_hidden = False

    def insert_episode_results(self, results):
        episode_label = Label(self, text="Episodios", font=("Helvetica", 15, "bold"))
        episode_label.grid(row=self.__curr_row, column=0, sticky='n')
        self.__curr_row += 1

        self.__insert_results(Episode, results)

    def insert_movie_results(self, results):
        movie_label = Label(self, text="Películas", font=("Helvetica", 15, "bold"))
        movie_label.grid(row=self.__curr_row, column=0, sticky='n')
        self.__curr_row += 1

        self.__insert_results(Movie, results)

    def __insert_results(self, cls, results):
        self.__temporary_label.pack_forget()
        self.__temporary_label_hidden = True
        for result in results:
            res_obj = cls(self, result)
            res_obj.init_components()
            res_obj.grid(row=self.__curr_row, column=0, sticky='n')
            self.__curr_row += 1

        self.grid_columnconfigure(0, weight=1)

    @property
    def temporary_label(self):
        return self.__temporary_label["text"]

    @temporary_label.setter
    def temporary_label(self, value):
        self.__temporary_label["text"] = value
        if self.__temporary_label_hidden:
            self.__temporary_label.grid(row=0, column=0, padx=10, pady=10)
        self.__temporary_label_hidden = False

    def init_components(self, *args, **kwargs):
        scrollbar = Scrollbar(self)
        scrollbar.grid(row=0, column=1, sticky='e')
        self.grid_columnconfigure(1, weight=15)
        self.grid_rowconfigure(0, weight=15)
"""