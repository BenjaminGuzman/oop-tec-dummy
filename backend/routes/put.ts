import { Router, Request, Response } from "express";
import { update } from "../db/mysql_conn";
import Ajv from "ajv"; // Another JSON Schema Validator
import { validationMiddleware } from "./validationMiddleware";

const router:Router = Router();
const ajv = new Ajv();

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

router.put("/media-rating", validationMiddleware(validateVideoUpdate), async (req: Request, res: Response) => {
    let updateFunction: (id:number, new_rating:number) => Promise<boolean>;

    if (req.body.type_of_content === "movie")
        updateFunction = update.movieRating;
    else
        updateFunction = update.episodeRating;

    const everything_ok = await updateFunction(req.body.id, req.body.new_rating);
    if (everything_ok)
        return res.status(200).end();

    return res.status(500).end();
});

export {router};
