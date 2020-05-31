USE OOPTecDummy;

DELIMITER //

# WE SHOULD BE USING OFFSETS AND LIMITS FOR THIS, BUT, IT'S JUST A DUMMY APP
# SO IT'S WORTHLESS

# SELECTS
DROP PROCEDURE IF EXISTS selectGenres;
CREATE PROCEDURE selectGenres()
BEGIN
    SELECT id, genre FROM Genre_Catalog;
END//

DROP PROCEDURE IF EXISTS selectSerieEpisodes;
CREATE PROCEDURE selectSerieEpisodes(
    IN serie_id_param INT UNSIGNED
)
BEGIN
    IF serie_id_param <> 0 THEN
        SELECT id, serie_id, n_episode, n_season, rating, duration, name, cover FROM Episode_Detail WHERE serie_id = serie_id_param;
    ELSE
        SELECT id, serie_id, n_episode, n_season, rating, duration, name, cover FROM Episode_Detail;
    END IF;

END//

DROP PROCEDURE IF EXISTS selectMoviesByRatingAndGenre;
CREATE PROCEDURE selectMoviesByRatingAndGenre(
    IN movie_rating_param DECIMAL(3, 1),
    IN genre_id_param TINYINT UNSIGNED
)
BEGIN
    IF genre_id_param <> 0 THEN
        SELECT id, rating, duration, year, name, cover FROM Movie_Detail
            INNER JOIN MovieGenres_Master MGM ON Movie_Detail.id = MGM.movie_id AND MGM.genre_id = genre_id_param AND Movie_Detail.rating >= movie_rating_param ORDER BY rating DESC;
    ELSE
        SELECT id, rating, duration, year, name, cover FROM Movie_Detail WHERE rating >= movie_rating_param ORDER BY rating DESC;
    END IF;
END//

DROP PROCEDURE IF EXISTS selectMoviesByRatingAndGenreLike;
CREATE PROCEDURE selectMoviesByRatingAndGenreLike(
    IN movie_rating_param DECIMAL(3, 1),
    IN genre_id_param TINYINT UNSIGNED,
    IN search_param VARCHAR(100)
)
BEGIN
    IF genre_id_param <> 0 THEN
        SELECT id, rating, duration, year, name, cover FROM Movie_Detail
            INNER JOIN MovieGenres_Master MGM ON Movie_Detail.id = MGM.movie_id AND MGM.genre_id = genre_id_param AND Movie_Detail.rating >= movie_rating_param AND Movie_Detail.name LIKE search_param ORDER BY rating DESC;
    ELSE
        SELECT id, rating, duration, year, name, cover FROM Movie_Detail WHERE rating >= movie_rating_param AND name LIKE search_param ORDER BY rating DESC;
    END IF;
END//

DROP PROCEDURE IF EXISTS selectEpisodesByRatingAndGenre;
CREATE PROCEDURE selectEpisodesByRatingAndGenre(
    IN episode_rating_param DECIMAL(3, 1),
    IN genre_id_param TINYINT UNSIGNED
)
BEGIN
    IF genre_id_param <> 0 THEN
        SELECT Episode_Detail.id, Episode_Detail.serie_id, n_episode, n_season, Episode_Detail.rating, duration, Episode_Detail.name, Episode_Detail.cover FROM Episode_Detail
            INNER JOIN Serie_Detail SD ON Episode_Detail.serie_id = SD.id AND Episode_Detail.rating >= episode_rating_param
            INNER JOIN SerieGenres_Master SGM ON SGM.serie_id = SD.id AND SGM.genre_id = genre_id_param ORDER BY rating DESC;
    ELSE
        SELECT id, serie_id, n_episode, n_season, rating, duration, name, cover FROM Episode_Detail WHERE rating >= episode_rating_param ORDER BY rating DESC;
    END IF;
END//

DROP PROCEDURE IF EXISTS selectEpisodesByRatingAndGenreLike;
CREATE PROCEDURE selectEpisodesByRatingAndGenreLike(
    IN episode_rating_param DECIMAL(3, 1),
    IN genre_id_param TINYINT UNSIGNED,
    IN search_param VARCHAR(100)
)
BEGIN
    IF genre_id_param <> 0 THEN
        SELECT Episode_Detail.id, Episode_Detail.serie_id, n_episode, n_season, Episode_Detail.rating, duration, Episode_Detail.name, Episode_Detail.cover FROM Episode_Detail
            INNER JOIN Serie_Detail SD ON Episode_Detail.serie_id = SD.id AND Episode_Detail.rating >= episode_rating_param
            INNER JOIN SerieGenres_Master SGM ON SGM.serie_id = SD.id AND SGM.genre_id = genre_id_param AND Episode_Detail.name LIKE search_param ORDER BY rating DESC;
    ELSE
        SELECT id, serie_id, n_episode, n_season, rating, duration, name, cover FROM Episode_Detail WHERE rating >= episode_rating_param AND name LIKE search_param ORDER BY rating DESC;
    END IF;
END//

# UPDATES
DROP PROCEDURE IF EXISTS updateMovieRating;
CREATE PROCEDURE updateMovieRating(
    IN movie_id_param INT UNSIGNED,
    IN rating_param DECIMAL(3, 1)
)
BEGIN
    UPDATE Movie_Detail SET rating = rating_param WHERE id = movie_id_param;
    # probably here should be something to return the number of rows updated
END//

DROP PROCEDURE IF EXISTS updateEpisodeRating;
CREATE PROCEDURE updateEpisodeRating(
    IN episode_id_param INT UNSIGNED,
    IN rating_param DECIMAL(3, 1)
)
BEGIN
    UPDATE Episode_Detail SET rating = rating_param WHERE id = episode_id_param;
END//

DROP PROCEDURE IF EXISTS insertSerieGenre;
CREATE PROCEDURE insertSerieGenre(
    IN serie_id_param INT UNSIGNED,
    IN genre_param VARCHAR(50)
)
BEGIN
    DECLARE genre_id_var TINYINT UNSIGNED;

    SELECT id INTO genre_id_var FROM Genre_Catalog WHERE genre = genre_param;

    INSERT INTO SerieGenres_Master(serie_id, genre_id) VALUE (serie_id_param, genre_id_var);
END//

DELIMITER ;