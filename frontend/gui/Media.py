from tkinter import Frame, Label, font, LEFT, RIGHT, Y, BOTH, Button
from PIL import ImageTk, Image
from .GUIComponent import GUIComponent
from exceptions import MissingProperty
from abc import ABC, abstractmethod


class Media(Frame, GUIComponent, ABC):
    @classmethod
    def init_defaults(cls):
        cls.MUST_HAVE_PROPS = ["rating", "duration", "name"]
        cls.TITLE_FONT = font.Font(family="Verdana", size=12, weight="bold")
        cls.RATING_FONT = font.Font(family="Times New Roman", size=16, weight="bold")

        # No image for the moment, let's just choose a dummy image
        cls._MOVIE_IMAGE = ImageTk.PhotoImage(Image.open("gui/dua.jpg"))
        cls._EPISODE_IMAGE = ImageTk.PhotoImage(Image.open("gui/jester.png"))
        cls._EDIT_IMAGE = ImageTk.PhotoImage(Image.open("gui/edit-w.png"))

    def __init__(self, master, properties, *args):
        super().__init__(master, borderwidth=2, relief="solid")

        if Media.MUST_HAVE_PROPS is None:
            raise MissingProperty("<<static>> MUST_HAVE_PROPS", "<<class>> Media")

        for prop in Media.MUST_HAVE_PROPS:
            if prop not in properties:
                raise ValueError("The properties parameter should have a \"{}\" property".format(prop))

        self._props = properties
        self._info_panel = None
        self.__rating_label = None

    def init_components(self, cover_movie=True, *args, **kwargs):
        # the media panel will be divided into three panels
        # one with the picture
        # one with the basic info
        # one with the rating

        cover_img = Media._MOVIE_IMAGE if cover_movie else Media._EPISODE_IMAGE

        cover_label = Label(self, image=cover_img)
        cover_label.pack(side=LEFT)

        self._info_panel = Frame(self)
        self._put_info(self._props["name"], font_type=Media.TITLE_FONT, row=0, column=0, sticky='w')
        self._put_info("{} min.".format(self._props["duration"] / 60), row=1, column=0, sticky='w')
        self._info_panel.pack(side=LEFT)

        edit_button = Button(self, image=Media._EDIT_IMAGE, background="black", command=self._on_click_edit)
        edit_button.pack(side=RIGHT, padx=5, pady=5)

        self.__rating_label = Label(self, text=self._props["rating"], font=Media.RATING_FONT)
        self.__rating_label.pack(side=RIGHT, padx=5)

    def _put_info(self, text, font_type=("Verdana", 12), **grid_kwargs):
        info_label = Label(self._info_panel, text=text, font=font_type)
        info_label.grid(**grid_kwargs)

    def _update_rating(self, new_rating):
        self.__rating_label["text"] = new_rating

    @abstractmethod
    def _on_click_edit(self):
        pass