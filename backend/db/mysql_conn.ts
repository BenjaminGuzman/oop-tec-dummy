import { createPool, format as sqlEscape } from "mysql";

const pool = createPool({
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
const executeProcedure = (sql_proc_string: string):Promise<object | null> => {
    return new Promise<object | null>(resolve => {
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
        let result: object | null;

        try {
            result = await executeProcedure("CALL selectGenres()");
        } catch (e) {
            result = null;
        }
        return result;
    },
    moviesWithRatingAndGenre: async (rating:number, genre:number) => {
        const sql_query = sqlEscape("CALL selectMoviesByRatingAndGenre(?, ?)", [rating, genre]);

        let result: object | null;
        try {
            result = await executeProcedure(sql_query);
        } catch (e) {
            result = null;
        }
        return result;
    },
    episodesWithRatingAndGenre: async (rating:number, genre:number) => {
        const sql_query = sqlEscape("CALL selectEpisodesByRatingAndGenre(?, ?)", [rating, genre]);

        let result: object | null;
        try {
            result = await executeProcedure(sql_query);
        } catch (e) {
            result = null;
        }
        return result;
    },
    episodesFromSerie: async (serie_id:number) => {
        const sql_query = sqlEscape("CALL selectSerieEpisodes(?)", [serie_id]);

        let result: object | null;
        try {
            result = await executeProcedure(sql_query);
        } catch (e) {
            result = null;
        }
        return result;
    }
}

const update = {
    movieRating: async (movie_id: number, new_rating: number) => {
        const sql_query = sqlEscape("CALL updateMovieRating(?, ?)", [movie_id, new_rating]);

        // no output is expected
        // let's hope that everything was updated correctly
        try {
            await executeProcedure(sql_query);
        } catch(e) {
            return false;
        }
        return true;
    },
    episodeRating: async (episode_id: number, new_rating: number) => {
        const sql_query = sqlEscape("CALL updateEpisodeRating(?, ?)", [episode_id, new_rating]);

        try {
            await executeProcedure(sql_query);
        } catch (e) {
            return false;
        }
        return true;
    }
};

export {select, update};
