from tkinter import Entry, END
from .GUIComponent import GUIComponent


def get_hex_color_as_number(hex_color_str):
    return hex_color_str.replace('#', "0x")


def dec_2_hex_color(dec_color):
    return hex(dec_color).replace("0x", '#')


class InputWithPlaceholder(Entry, GUIComponent):

    def __init__(self, master=None, placeholder="...", color_diff=0x333333, **kwargs):
        super().__init__(master, kwargs)

        original_color = get_hex_color_as_number(self["fg"])
        original_color = int(original_color, 16) # the color is hexadecimal, this returns it in base 10 but operations will work fine
        placeholder_color = original_color + color_diff if original_color < color_diff else original_color - color_diff # conditional to avoid negative values

        self.__placeholder = placeholder
        self.__placeholder_color = dec_2_hex_color(placeholder_color)
        self.__fg_color = self["fg"]
        self.__placeholder_active = True

        self.__put_placeholder()

    @property
    def placeholder_is_active(self):
        return self.__placeholder_active

    def init_components(self):
        self.bind("<FocusIn>", self.__on_focus_in)
        self.bind("<FocusOut>", self.__on_focus_out)

    def __put_placeholder(self):
        """
        Inserts the placeholder and also changes the foreground color to differentiate it from normal text
        """
        self.__placeholder_active = True
        self["fg"] = self.__placeholder_color
        self.insert(0, self.__placeholder)

    def __on_focus_in(self, *args):
        # remove the placeholder if what is in the text input is actually the placeholder
        if self.__placeholder_active: # if there is nothing in the input
            self.delete(0, END)
            self["fg"] = self.__fg_color

    def __on_focus_out(self, *args):
        # put the placeholder if there is nothing in the text input
        if not self.get():
            self.__put_placeholder()
        else:
            self.__placeholder_active = False