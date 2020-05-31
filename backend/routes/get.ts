import { Router, Request, Response } from "express";
import { select } from "../db/mysql_conn";
import {validationMiddleware} from "./validationMiddleware";
import Ajv from "ajv"; // Another JSON Schema Validator

const router:Router = Router();
const ajv = new Ajv();

// json schema validator for the req.body object in the
// /media endpoint
const validateVideoQuery = ajv.compile({
    type: "object",
    required: ["type_of_content"],
    properties: {
        type_of_content: {
            type: "string",
            enum: ["movie", "episode", "video"] // video is either movie and episode
        },
        search: {
            type: "string",
            maxLength: 100
        },
        min_rating: { // default 0
            type: "number",
            maximum: 10,
            minimum: 0
        },
        genre: { // undefined -> query all genres
            type: "number",
            minimum: 0
        }
    }
});

const validateEpisodesQuery = ajv.compile({
    type: "object",
    required: ["serie_id"],
    properties: {
        serie_id: { // if 0 all episodes will be queried
            type: "number",
            minimum: 0
        }
    }
});

/**
 * Endpoint to query all the registered genres in the database
 */
router.get("/genres", async (req: Request, res: Response) => {
    return res.send({
        genres: await select.genres()
    });
});

/**
 * Endpoint to query either movies, episodes or both
 * by a minimum ranking and a genre
 * the only required param is type_of content
 * The min_ranking, and genre are optional, default 0
 */
router.get("/media", validationMiddleware(validateVideoQuery), async (req: Request, res: Response) => {
    if (!req.body.min_rating) // 0 min_ranking will be still 0
        req.body.min_rating = 0;

    if (!req.body.genre) // 0 genre wil be still 0
        req.body.genre = 0;

    let results;
    const content_type = req.body.type_of_content;
    if (content_type === "movie")
        results = {
            movies: await select.moviesWithRatingGenreLike(req.body.min_rating, req.body.genre, req.body.search)
        };
    else if (content_type === "episode")
        results = {
            episodes: await select.episodesWithRatingGenreLike(req.body.min_rating, req.body.genre, req.body.search)
        };
    else {
        const movie_promise = select.moviesWithRatingGenreLike(req.body.min_rating, req.body.genre, req.body.search);
        const episodes_promise = select.episodesWithRatingGenreLike(req.body.min_rating, req.body.genre, req.body.search);
        const values = await Promise.all([movie_promise, episodes_promise]);
        results = {
            movies: values[0],
            episodes: values[1]
        };
    }

    return res.send(results);
});

/**
 * Get all the episodes from a given serie, with the param serie_id
 */
router.get("/episodes", validationMiddleware(validateEpisodesQuery), async (req: Request, res: Response) => {
    return res.send({
        episodes: await select.episodesFromSerie(req.body.serie_id)
    });
});

export { router };
