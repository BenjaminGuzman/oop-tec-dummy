from .Media import Media
from request_handlers import Request
from queue import Queue
from tkinter import simpledialog, messagebox


class Movie(Media):

    def __init__(self, master, props, *args):
        super().__init__(master, props)

    def init_components(self, cover_movie=True, *args, **kwargs):
        super().init_components(cover_movie=True)

    def _on_click_edit(self):
        new_rating = simpledialog.askfloat("Calificar película", "Nueva calificación para {}:".format(self._props["name"]))
        if new_rating is None:  # None None is returned when the user clicks cancel
            return

        payload = {
            "type_of_content": "movie",
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