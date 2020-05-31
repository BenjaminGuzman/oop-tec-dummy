from tkinter import Scrollbar, VERTICAL, Label, TOP, Y, LEFT, BOTH, Frame, X, Canvas, RIGHT, BOTTOM
from .GUIComponent import GUIComponent
from .PaginationControls import PaginationControls
from math import ceil


class ScrollBarPanel(Frame, GUIComponent):
    __ITEMS_PER_PAGE = 5

    def __init__(self, master, default_text, **kwargs):
        super().__init__(master, kwargs)

        self.__canvas = None # the canvas that will be inside this frame
        self.__frame = None # the frame that will be embebed in the canvas

        self.__scrollbar = None
        self.__default_text = default_text
        self.__default_label = Label(self, text=default_text)
        self.__message_hidden = False
        self.__pagination_control = None

        self.__items = []
        self.__curr_items_obj = [Dummy(), Dummy(), Dummy(), Dummy(), Dummy()]
        self.__prev_idx_show = -1
        self.__next_idx_show = 0

        self.__items_class = None

    def init_components(self, title):
        self.__canvas = Canvas(self)
        self.__frame = Frame(self.__canvas)

        title_label = Label(self, text=title, font=("Helvetica", 15, "bold"))
        title_label.pack(side=TOP, fill=Y)

        self.__default_label.pack(side=TOP, fill=Y, pady=3)

        self.__pagination_control = PaginationControls(self, self.__page_back, self.__page_next)
        self.__pagination_control.init_components()
        self.__pagination_control.pack(side=TOP, fill=Y, pady=5)

        self.__scrollbar = Scrollbar(self.__canvas, orient=VERTICAL, command=self.__canvas.yview)

        # we must tell the canvas how large the frame will be, so that it knows how much it can scroll
        # this should also resize the scrollbar when the frame updates
        self.__frame.bind("<Configure>", self.__update_scrollbar)

        self.__canvas.create_window((0, 0), window=self.__frame, anchor="nw")
        self.__canvas.configure(yscrollcommand=self.__scrollbar.set)

        self.__canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.__scrollbar.pack(side=RIGHT, fill=Y)

    def show_message(self):
        if self.__message_hidden:
            self.__default_label.pack()

    def hide_message(self):
        if not self.__message_hidden:
            self.__default_label.pack_forget()

    def message_reset(self):
        self.__default_label["text"] = self.__default_text

    def message(self, msg):
        self.__default_label["text"] = msg

    def reset(self):
        self.__items = []
        self.__pagination_control.reset()
        self.__prev_idx_show = -1
        self.__next_idx_show = 0

    def add_items(self, cls, results):
        self.__items = results
        self.__items_class = cls # cls is Media type
        self.__pagination_control.n_max_pages = ceil(len(results) / ScrollBarPanel.__ITEMS_PER_PAGE)
        self.__pagination_control.set_buttons_status(first_check=True)
        self.__display_page()

    # Note: there is a "problem" with pagination
    # when you click all all the pages, and see all al the episodes
    # if the number of episodes % 5 != 0, an offset will be generated (from 1 to 4)
    # and when you go back to the page 1, that offset will appear, so you'll see just 1 or 4 episodes in the page
    def __display_page(self, reverse=False):
        for obj in self.__curr_items_obj:
            obj.destroy()

        range_idxs = None

        if reverse:
            end_idx = self.__prev_idx_show - ScrollBarPanel.__ITEMS_PER_PAGE
            if end_idx <= -1:
                end_idx = -1
                self.__next_idx_show = ScrollBarPanel.__ITEMS_PER_PAGE
            else:
                self.__next_idx_show = end_idx
            range_idxs = range(self.__prev_idx_show, end_idx, -1)
            self.__prev_idx_show = 0 if end_idx < -1 else end_idx

        else:
            end_idx = self.__next_idx_show + ScrollBarPanel.__ITEMS_PER_PAGE
            if end_idx > len(self.__items):
                end_idx = len(self.__items)
            range_idxs = range(self.__next_idx_show, end_idx)
            self.__prev_idx_show = self.__next_idx_show - 1
            self.__next_idx_show = end_idx

        j = 0
        for i in range_idxs:
            obj = self.__items_class(self.__frame, self.__items[i])
            obj.init_components()
            obj.pack(side=TOP, fill=BOTH, expand=True)
            self.__curr_items_obj[j] = obj
            j += 1

    def __update_scrollbar(self, event):
        self.__canvas.configure(scrollregion=self.__canvas.bbox("all"))

    def __page_back(self):
        self.__display_page(reverse=True)

    def __page_next(self):
        self.__display_page()


class Dummy():
    def destroy(self):
        pass