from tkinter import RIGHT, Button, messagebox, LEFT
from tkinter import simpledialog
from .Media import Media
from queue import Queue
from request_handlers import Request


class Episode(Media):
    def __init__(self, master, props, *cb_query_serie):
        super().__init__(master, props)

        self.__cb_query_serie = cb_query_serie[0][0]
        # props unique of an episode:
        # serie_id
        # serie_name
        # n_episode
        # n_season

    def init_components(self, cover_movie=True, *args, **kwargs):
        super().init_components(cover_movie=False)

        super()._put_info("Serie: {}".format(self._props["serie_name"]), row=2, column=0, sticky='w')
        super()._put_info("Episodio: {}".format(self._props["n_episode"]), row=3, column=0, sticky='w')
        super()._put_info("Temporada: {}".format(self._props["n_season"]), row=4, column=0, sticky='w')

        show_all_episodes_button = Button(self, text="Ver serie", command=self.__show_all_episodes)
        show_all_episodes_button.pack(side=LEFT, padx=5, pady=5)

    def _on_click_edit(self):
        new_rating = simpledialog.askfloat("Calificar episodio", "Nueva calificación para {}:".format(self._props["name"]))
        if new_rating is None: # None None is returned when the user clicks cancel
            return

        payload = {
            "type_of_content": "episode",
            "id": self._props["id"],
            "new_rating": new_rating
        }

        status_queue = Queue()

        request = Request(status_queue, "media-rating", method="PUT", body=payload)
        print("Updating", payload)
        request.start()

        error = False
        while True:
            if not status_queue.empty():
                tmp_response = status_queue.get()
                if tmp_response == "ok":
                    break
                if tmp_response == "error":
                    error = True
                    break

        if error:
            messagebox.showerror("Error al actualizar", "Ocurrió un desafortunado error al cambiar la calificación de {}".format(self._props["name"]))
            return

        self._props["rating"] = new_rating
        super()._update_rating(new_rating)

    def __show_all_episodes(self):
        self.__cb_query_serie(self._props["serie_id"])
