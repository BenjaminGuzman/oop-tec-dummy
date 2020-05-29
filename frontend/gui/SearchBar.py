from tkinter import PanedWindow, Label, Button, OptionMenu, StringVar
from .GUIComponent import GUIComponent
from .InputWithPlaceholder import InputWithPlaceholder


class SearchBar(PanedWindow, GUIComponent):
    def __init__(self, master, genres):
        super().__init__(master)

        self.__media_choice = StringVar()
        self.__rating_choice = StringVar()
        self.__genre_choice = StringVar()
        self.__search = None

        # genres has the following structure:
        # [{'id': 4, 'genre': 'Action'}, {'id': 1, 'genre': 'Adventure'},...]
        # but it's more useful the following structure
        # {'Action': 4, 'Adventure': 1}
        self.__genres = {}
        for genre in genres:
            self.__genres[genre["genre"]] = genre["id"]
        self.__genres["Todos"] = 0

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

    # Override, overload
    def init_components(self):
        self.__init_labels()
        self.__init_interactive_widgets()

    def __init_labels(self):
        default_kwargs = {
            "sticky": 's',
            "padx": 5,
            "pady": 3
        }
        content_type_label = Label(self, text="Tipo de contenido")
        search_label = Label(self, text='')
        rating_label = Label(self, text="Rating")
        genre_label = Label(self, text="Género")

        content_type_label.grid(row=0, column=0, **default_kwargs)
        #search_label.grid(row=0, column=1, **default_kwargs)
        rating_label.grid(row=0, column=2, **default_kwargs)
        genre_label.grid(row=0, column=3, **default_kwargs)

    def __init_interactive_widgets(self):
        default_kwargs = {
            "sticky": 'n',
            "padx": 7,
            "pady": 5
        }
        # Type of media dropdown initialization
        opts_dropdown = ["Película", "Serie", "Episodio", "Episodio o Película"]
        self.__media_choice.set(opts_dropdown[-1])
        media_dropdown = OptionMenu(self, self.__media_choice, *opts_dropdown)
        media_dropdown.grid(row=1, column=0, **default_kwargs)

        # Search input initialization
        self.__search = InputWithPlaceholder(master=self, placeholder="Encuentra lo que buscas...", width=40)
        self.__search.init_components()
        self.__search.grid(row=1, column=1, **default_kwargs)

        # minimum rating initialization
        opts_dropdown = [str(i / 10) for i in range(0, 50 + 5, 5)]
        self.__rating_choice.set(opts_dropdown[-1])
        rating_dropdown = OptionMenu(self, self.__rating_choice, *opts_dropdown)
        rating_dropdown.grid(row=1, column=2, **default_kwargs)

        # genre dropdown initialization
        opts_dropdown = list(self.__genres.keys())
        self.__genre_choice.set(opts_dropdown[-1])
        genre_dropdown = OptionMenu(self, self.__genre_choice, *opts_dropdown)
        genre_dropdown.grid(row=1, column=3, **default_kwargs)

        # search button initialization
        search_button = Button(self, text="Buscar", command=self.__on_click_search)
        search_button.grid(row=1, column=4, **default_kwargs)

    def __on_click_search(self):
        # TODO: implement
        # get the selected values
        # and send request to the api
        pass
