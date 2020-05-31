from tkinter import Frame, Label, LEFT, Button
from .GUIComponent import GUIComponent


class PaginationControls(Frame, GUIComponent):
    def __init__(self, master, page_back, page_next):
        super().__init__(master)

        self.__page_label = None

        self.__page = 0

        self.__page_back = page_back
        self.__page_next = page_next

        self.__page_back_button = None
        self.__page_next_button = None

        self.__n_max_pages = 0

    def init_components(self, label_text="Página: "):
        label = Label(self, text=label_text)
        label.pack(side=LEFT)

        self.__page_back_button = Button(self, text="<", command=self.__previous_page, state="disabled")
        self.__page_back_button.pack(side=LEFT)

        self.__page_label = Label(self, text=str(self.__page + 1))
        self.__page_label.pack(side=LEFT)

        self.__page_next_button = Button(self, text=">", command=self.__next_page, state="disabled")
        self.__page_next_button.pack(side=LEFT)

    def __previous_page(self):
        self.__page -= 1
        self.__page_label["text"] = self.__page + 1
        self.__page_back()

        self.set_buttons_status()

    def __next_page(self):
        self.__page += 1
        self.__page_label["text"] = self.__page + 1
        self.__page_next()

        self.set_buttons_status()

    def set_buttons_status(self, first_check=False):
        if first_check:
            self.__page_back_button["state"] = "disabled"
            if self.__n_max_pages <= 1:
                self.__page_next_button["state"] = "disabled"
            else:
                self.__page_next_button["state"] = "normal"
            return

        if self.__page >= self.__n_max_pages:
            self.__page_next_button["state"] = "disabled"
        elif self.__page < 1:
            self.__page_back_button["state"] = "disabled"
        else:
            if self.__page_next_button["state"] == "disabled":
                self.__page_next_button["state"] = "normal"
            if self.__page_back_button["state"] == "disabled":
                self.__page_back_button["state"] = "normal"

    def reset(self):
        self.__page = 0
        self.n_max_pages = 0

    @property
    def page(self):
        return self.__page

    @property
    def n_max_pages(self):
        return self.__n_max_pages

    @n_max_pages.setter
    def n_max_pages(self, n_max):
        self.__n_max_pages = n_max