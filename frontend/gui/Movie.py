from .Media import Media


class Movie(Media):

    def __init__(self, master, props):
        super().__init__(master, props)

    def init_components(self, cover_movie=True, *args, **kwargs):
        super().init_components(cover_movie=True)