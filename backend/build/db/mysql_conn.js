"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.update = exports.select = void 0;
const mysql_1 = require("mysql");
const pool = mysql_1.createPool({
    host: process.env.DB_HOST,
    user: process.env.DB_USER,
    password: process.env.DB_PASSWORD,
    database: process.env.DB_NAME
});
// WE SHOULD BE USING OFFSETS AND LIMITS FOR THIS, BUT, IT'S JUST A DUMMY APP
// SO IT'S WORTHLESS
/**
 * Executes sql_proc_string using a connection from the pool,
 * @param sql_proc_string the sql query, such as CALL procedure(param1, param2)
 * THIS FUNCTION DOES NOT ESCAPES the parameters, so the sql_proc_string param
 * should be ALREADY ESCAPED
 */
const executeProcedure = (sql_proc_string) => {
    console.log(sql_proc_string);
    return new Promise(resolve => {
        pool.getConnection((err, conn) => {
            if (err) {
                console.error(new Error("Something went very wrong when retrieving a connection from the pool!!"));
                console.error(err);
                return resolve(null);
            }
            conn.query(sql_proc_string, (err, results) => {
                conn.release();
                if (err) {
                    console.error(new Error("Something went very wrong when querying something!!"));
                    console.error(err);
                    return resolve(null);
                }
                return resolve(results[0]);
            });
        });
    });
};
const select = {
    genres: async () => {
        let result;
        try {
            result = await executeProcedure("CALL selectGenres()");
        }
        catch (e) {
            result = null;
        }
        return result;
    },
    moviesWithRatingGenreLike: async (rating, genre, search) => {
        let sql_query;
        if (!search)
            sql_query = mysql_1.format("CALL selectMoviesByRatingAndGenre(?, ?)", [rating, genre]);
        else
            sql_query = mysql_1.format("CALL selectMoviesByRatingAndGenreLike(?, ?, ?)", [rating, genre, `${search}%`]);
        let result;
        try {
            result = await executeProcedure(sql_query);
        }
        catch (e) {
            result = null;
        }
        return result;
    },
    episodesWithRatingGenreLike: async (rating, genre, search) => {
        let sql_query;
        if (!search)
            sql_query = mysql_1.format("CALL selectEpisodesByRatingAndGenre(?, ?)", [rating, genre]);
        else
            sql_query = mysql_1.format("CALL selectEpisodesByRatingAndGenreLike(?, ?, ?)", [rating, genre, `${search}%`]);
        let result;
        try {
            result = await executeProcedure(sql_query);
        }
        catch (e) {
            result = null;
        }
        return result;
    },
    episodesFromSerie: async (serie_id) => {
        const sql_query = mysql_1.format("CALL selectSerieEpisodes(?)", [serie_id]);
        let result;
        try {
            result = await executeProcedure(sql_query);
        }
        catch (e) {
            result = null;
        }
        return result;
    }
};
exports.select = select;
const update = {
    movieRating: async (movie_id, new_rating) => {
        const sql_query = mysql_1.format("CALL updateMovieRating(?, ?)", [movie_id, new_rating]);
        // no output is expected
        // let's hope that everything was updated correctly
        try {
            await executeProcedure(sql_query);
        }
        catch (e) {
            return false;
        }
        return true;
    },
    episodeRating: async (episode_id, new_rating) => {
        const sql_query = mysql_1.format("CALL updateEpisodeRating(?, ?)", [episode_id, new_rating]);
        try {
            await executeProcedure(sql_query);
        }
        catch (e) {
            return false;
        }
        return true;
    }
};
exports.update = update;
