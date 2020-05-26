USE OOPTecDummy;
CREATE PROCEDURE insertSerieGenre(
    serie_id_param INT UNSIGNED,
    genre_param VARCHAR(50)
)
BEGIN
    DECLARE genre_id_var TINYINT UNSIGNED;

    SELECT id INTO genre_id_var FROM Genre_Catalog WHERE genre = genre_param;

    INSERT INTO SerieGenres_Master(serie_id, genre_id) VALUE (serie_id_param, genre_id_var);
END;