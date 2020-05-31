from tkinter import Frame, Label, TOP, X
from .GUIComponent import GUIComponent


class Title(Frame, GUIComponent):
    def __init__(self, master):
        super().__init__(master)

    def init_components(self, *args, **kwargs):
        default_paddings = {
            "pady": 5
        }

        title = Label(self, text="Proyecto Integrador TC1030.311", font=("Helvetica", 18))
        name1 = Label(self, text="Benjamín Antonio Velasco Guzmán A01750156", font=("Verdana", 14, "bold"))
        name2 = Label(self, text="Cristián Aldo Sandoval Suárez A01751XX", font=("Verdana", 14, "bold"))

        title.pack(side=TOP, fill=X, **default_paddings)
        name1.pack(side=TOP, fill=X, **default_paddings)
        name2.pack(side=TOP, fill=X, **default_paddings)
