"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.router = void 0;
const express_1 = require("express");
const mysql_conn_1 = require("../db/mysql_conn");
const ajv_1 = __importDefault(require("ajv")); // Another JSON Schema Validator
const validationMiddleware_1 = require("./validationMiddleware");
const router = express_1.Router();
exports.router = router;
const ajv = new ajv_1.default();
const validateVideoUpdate = ajv.compile({
    type: "object",
    required: ["type_of_content", "new_rating"],
    properties: {
        type_of_content: {
            type: "string",
            enum: ["movie", "episode"]
        },
        id: {
            type: "number",
            minimum: 0
        },
        new_rating: {
            type: "number",
            maximum: 10,
            minimum: 0
        }
    }
});
router.put("/media-rating", validationMiddleware_1.validationMiddleware(validateVideoUpdate), async (req, res) => {
    let updateFunction;
    if (req.body.type_of_content === "movie")
        updateFunction = mysql_conn_1.update.movieRating;
    else
        updateFunction = mysql_conn_1.update.episodeRating;
    const everything_ok = await updateFunction(req.body.id, req.body.new_rating);
    if (everything_ok)
        return res.status(200).end();
    return res.status(500).end();
});
