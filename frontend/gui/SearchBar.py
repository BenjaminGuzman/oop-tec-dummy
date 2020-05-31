from tkinter import Frame, Label, Button, OptionMenu, StringVar, HORIZONTAL, messagebox
from tkinter.ttk import Progressbar
from .GUIComponent import GUIComponent
from .InputWithPlaceholder import InputWithPlaceholder
from request_handlers import Request
from queue import Queue
from exceptions import MissingProperty


class SearchBar(Frame, GUIComponent):
    def __init__(self, master, genres):
        super().__init__(master)

        self.__media_choice = StringVar()
        self.__rating_choice = StringVar()
        self.__genre_choice = StringVar()
        self.__search = None

        self.__progressbar = None

        # genres has the following structure:
        # [{'id': 4, 'genre': 'Action'}, {'id': 1, 'genre': 'Adventure'},...]
        # but it's more useful the following structure
        # {'Action': 4, 'Adventure': 1}
        self.__genres = {}
        for genre in genres:
            self.__genres[genre["genre"]] = genre["id"]
        self.__genres["Todos"] = 0

        self.__search_results = None

        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_columnconfigure(2, weight=1)
        self.grid_columnconfigure(3, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)

    # Override
    def init_components(self):
        self.__init_labels()
        self.__init_interactive_widgets()
        self.__progressbar = Progressbar(self, orient=HORIZONTAL, length=100, mode="determinate")

    def __init_labels(self):
        default_kwargs = {
            "sticky": 's',
            "padx": 5,
            "pady": 3
        }
        content_type_label = Label(self, text="Tipo de contenido")
        rating_label = Label(self, text="Rating mínimo")
        genre_label = Label(self, text="Género")

        content_type_label.grid(row=0, column=0, **default_kwargs)
        rating_label.grid(row=0, column=2, **default_kwargs)
        genre_label.grid(row=0, column=3, **default_kwargs)

    def __init_interactive_widgets(self):
        default_kwargs = {
            "sticky": 'n',
            "padx": 7,
            "pady": 5
        }
        # Type of media dropdown initialization
        opts_dropdown = ["Película", "Episodio", "Episodio o Película"]
        self.__media_choice.set(opts_dropdown[-1])
        media_dropdown = OptionMenu(self, self.__media_choice, *opts_dropdown)
        media_dropdown.grid(row=1, column=0, **default_kwargs)

        # Search input initialization
        self.__search = InputWithPlaceholder(master=self, placeholder="Encuentra lo que buscas...", width=40)
        self.__search.init_components()
        self.__search.grid(row=1, column=1, **default_kwargs)

        # minimum rating initialization
        opts_dropdown = [str(i / 10) for i in range(0, 100 + 5, 5)]
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
        # Get selected values
        media_choice = self.__media_choice.get()
        search = '' if self.__search.placeholder_is_active else self.__search.get().strip()
        rating_choice = float(self.__rating_choice.get())
        genre_choice = self.__genre_choice.get()

        # Prepare payload
        if media_choice == "Episodio o Película":
            media_choice = "video"
        elif media_choice == "Película":
            media_choice = "movie"
        else:
            media_choice = "episode"

        genre_idx = self.__genres[genre_choice]

        payload = {
            "type_of_content": media_choice,
            "search": search,
            "min_rating": rating_choice,
            "genre": genre_idx
        }

        # Send payload
        status_queue = Queue()
        request = Request(status_queue, "media", body=payload)
        print("Searching", payload)
        request.start()

        error = False
        self.__progressbar.grid(row=2, column=0, sticky='n', pady=3)
        self.__progressbar["value"] = 25
        while True:
            if not status_queue.empty():
                tmp_response = status_queue.get()
                if tmp_response == "sent":
                    self.__progressbar["value"] = 50
                elif tmp_response == "received":
                    self.__progressbar["value"] = 75
                elif tmp_response == "ok":
                    self.__progressbar["value"] = 100
                    break
                elif tmp_response == "error":
                    error = True
                    break

        self.__progressbar.grid_remove()

        if error:
            messagebox.showerror("Error", "Algo malo ha sucedido al realizar la búsqueda")
            return

        response = status_queue.get()

        if self.__search_results is None:
            raise MissingProperty("search_results", self)

        if media_choice == "movie":
            self.__show_response(response, "movies")
        elif media_choice == "episode":
            self.__show_response(response, "episodes")
        else:
            self.__show_response(response, "movies")
            self.__show_response(response, "episodes")

    def __show_response(self, response, content_type):
        res = response[content_type]
        if content_type == "movies":
            self.__search_results.insert_movie_results(res)
        else:
            self.__search_results.insert_episode_results(res)

    @property
    def search_results(self):
        return self.__search_results is not None

    @search_results.setter
    def search_results(self, search_result_obj):
        if self.__search_results is not None:
            raise ValueError("search_results already has a value")
        self.__search_results = search_result_obj
