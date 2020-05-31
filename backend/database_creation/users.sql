USE OOPTecDummy;

DROP USER IF EXISTS ooptecdummy_sys@'192.168.1.%';
CREATE USER ooptecdummy_sys@'192.168.1.%' IDENTIFIED BY 'h3ll0 world th1$ 1$ th3 pa$$world for the $y$t3m u$3r so, you SHOULD NOT be reading this!!';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.selectGenres TO ooptecdummy_sys@'192.168.1.%';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.selectSerieEpisodes TO ooptecdummy_sys@'192.168.1.%';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.selectMoviesByRatingAndGenre TO ooptecdummy_sys@'192.168.1.%';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.selectMoviesByRatingAndGenreLike TO ooptecdummy_sys@'192.168.1.%';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.selectEpisodesByRatingAndGenre TO ooptecdummy_sys@'192.168.1.%';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.selectEpisodesByRatingAndGenreLike TO ooptecdummy_sys@'192.168.1.%';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.updateMovieRating TO ooptecdummy_sys@'192.168.1.%';
GRANT EXECUTE ON PROCEDURE OOPTecDummy.updateEpisodeRating TO ooptecdummy_sys@'192.168.1.%';