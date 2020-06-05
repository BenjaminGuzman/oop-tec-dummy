from tkinter import Frame, Label, Button, OptionMenu, StringVar, HORIZONTAL, messagebox, Spinbox, END
from tkinter.ttk import Progressbar
from .GUIComponent import GUIComponent
from .InputWithPlaceholder import InputWithPlaceholder
from request_handlers import Request
from queue import Queue
from exceptions import MissingProperty
import re


class SearchBar(Frame, GUIComponent):
    REGEX_RATING = re.compile(r"^[0-9](\.[0-9])?$")

    def __init__(self, master, genres):
        super().__init__(master)

        self.__media_choice = StringVar()
        self.__rating_choice = None
        self.__genre_choice = StringVar()
        self.__search = None

        self.__progressbar = None

        self.__search_serie_input = None

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
        self.__rating_choice = Spinbox(self, from_=0, to=10, increment=0.5)
        self.__rating_choice.grid(row=1, column=2, **default_kwargs)

        # genre dropdown initialization
        opts_dropdown = list(self.__genres.keys())
        self.__genre_choice.set(opts_dropdown[-1])
        genre_dropdown = OptionMenu(self, self.__genre_choice, *opts_dropdown)
        genre_dropdown.grid(row=1, column=3, **default_kwargs)

        # search button initialization
        search_button = Button(self, text="Buscar", command=self.__on_click_search)
        search_button.grid(row=1, column=4, **default_kwargs)

        # NOW THE FOURTH ROW, CONTAINING THE SEARCH BY SERIE
        # (the third row is for the progressbar only)
        search_serie_label = Label(self, text="Buscar episodios de la serie con ID:")
        search_serie_label.grid(row=3, column=0, **default_kwargs)

        self.__search_serie_input = InputWithPlaceholder(master=self, placeholder="ID de la serie \"tt#####\"", width=40)
        self.__search_serie_input.init_components()
        self.__search_serie_input.grid(row=3, column=1, **default_kwargs)

        search_serie_button = Button(self, text="Buscar episodios", command=self.__on_click_search_episodes)
        search_serie_button.grid(row=3, column=2, **default_kwargs)

    def __on_click_search(self):
        # Get selected values
        media_choice = self.__media_choice.get()
        search = '' if self.__search.placeholder_is_active else self.__search.get().strip()
        rating_choice = self.__rating_choice.get()
        genre_choice = self.__genre_choice.get()

        # check if rating is valid
        if not SearchBar.REGEX_RATING.match(rating_choice):
            messagebox.showerror("Rating no válido", "El rating debe tener un formato de #.#, y debe estar entre 0 y 10")
            return

        if len(search) > 100:
            messagebox.showerror("Búsqueda muy larga", "Por favor limite su búsqueda a 100 caracteres")
            return

        rating_choice = float(rating_choice)

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

        self.__search_results.clear_all()
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

    def __on_click_search_episodes(self, *args):
        serie_id = self.__search_serie_input.get().strip()
        serie_id = serie_id.replace("tt", '')

        if not serie_id.isnumeric():
            messagebox.showerror("ID de la serie no válido", "Ingrese un ID correcto, puede ser un número o las letras \"tt\" seguidas del ID")
            return

        serie_id = int(serie_id)

        payload = {
            "serie_id": serie_id
        }

        status_queue = Queue()
        request = Request(status_queue, "episodes", body=payload)
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
        self.__search_results.clear_all()

        response = {
            "movies": [],
            "episodes": response["episodes"]
        }
        self.__show_response(response, "movies")
        self.__show_response(response, "episodes")

    def __update_serie_search(self, serie_id):
        self.__search_serie_input.delete(0, END)
        self.__search_serie_input.insert(0, serie_id)
        self.__on_click_search_episodes(None)

    @property
    def search_results(self):
        return self.__search_results is not None

    @search_results.setter
    def search_results(self, search_result_obj):
        if self.__search_results is not None:
            raise ValueError("search_results already has a value")
        self.__search_results = search_result_obj
        self.__search_results.cb_search_serie = self.__update_serie_search
