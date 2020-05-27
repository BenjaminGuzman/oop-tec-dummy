"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.router = void 0;
const express_1 = require("express");
const mysql_conn_1 = require("../db/mysql_conn");
const validationMiddleware_1 = require("./validationMiddleware");
const ajv_1 = __importDefault(require("ajv")); // Another JSON Schema Validator
const router = express_1.Router();
exports.router = router;
const ajv = new ajv_1.default();
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
        min_rating: {
            type: "number",
            maximum: 10,
            minimum: 0
        },
        genre: {
            type: "number",
            minimum: 0
        }
    }
});
const validateEpisodesQuery = ajv.compile({
    type: "object",
    required: ["serie_id"],
    properties: {
        serie_id: {
            type: "number",
            minimum: 0
        }
    }
});
/**
 * Endpoint to query all the registered genres in the database
 */
router.get("/genres", async (req, res) => {
    return res.send({
        genres: await mysql_conn_1.select.genres()
    });
});
/**
 * Endpoint to query either movies, episodes or both
 * by a minimum ranking and a genre
 * the only required param is type_of content
 * The min_ranking, and genre are optional, default 0
 */
router.get("/media", validationMiddleware_1.validationMiddleware(validateVideoQuery), async (req, res) => {
    if (!req.body.min_rating) // 0 min_ranking will be still 0
        req.body.min_rating = 0;
    if (!req.body.genre) // 0 genre wil be still 0
        req.body.genre = 0;
    let results;
    const content_type = req.body.type_of_content;
    if (content_type === "movie")
        results = {
            movies: await mysql_conn_1.select.moviesWithRatingAndGenre(req.body.min_rating, req.body.genre)
        };
    else if (content_type === "episode")
        results = {
            episodes: await mysql_conn_1.select.episodesWithRatingAndGenre(req.body.min_rating, req.body.genre)
        };
    else {
        const movie_promise = mysql_conn_1.select.moviesWithRatingAndGenre(req.body.min_rating, req.body.genre);
        const episodes_promise = mysql_conn_1.select.episodesWithRatingAndGenre(req.body.min_rating, req.body.genre);
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
router.get("/episodes", validationMiddleware_1.validationMiddleware(validateEpisodesQuery), async (req, res) => {
    return res.send({
        episodes: await mysql_conn_1.select.episodesFromSerie(req.body.serie_id)
    });
});
