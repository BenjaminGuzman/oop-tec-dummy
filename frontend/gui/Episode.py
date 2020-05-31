from .Media import Media


class Episode(Media):
    def __init__(self, master, props):
        super().__init__(master, props)

        # props unique of an episode:
        # serie_id
        # n_episode
        # n_season


    def init_components(self, cover_movie=True, *args, **kwargs):
        super().init_components(cover_movie=False)