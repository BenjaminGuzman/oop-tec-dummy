USE OOPTecDummy;

CREATE TRIGGER after_episode_update
    AFTER UPDATE ON Episode_Detail
    FOR EACH ROW
BEGIN
    UPDATE Serie_Detail SET rating = (SELECT AVG(rating) FROM Episode_Detail WHERE serie_id = OLD.serie_id)
        WHERE id = OLD.serie_id;
END;

CREATE TRIGGER after_episode_insert
    AFTER UPDATE ON Episode_Detail
    FOR EACH ROW
BEGIN
    UPDATE Serie_Detail SET rating = (SELECT AVG(rating) FROM Episode_Detail WHERE serie_id = OLD.serie_id)
        WHERE id = OLD.serie_id;
END;