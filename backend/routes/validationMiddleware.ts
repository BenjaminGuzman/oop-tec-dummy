import { Request, Response, NextFunction } from "express";
import {ValidateFunction} from "ajv";

const validationMiddleware = (validationFn: ValidateFunction) => {
    return (req: Request, res: Response, next: NextFunction) => {
        const is_body_valid = validationFn(req.body);
        if (!is_body_valid)
            return res.status(400).send({error: "invalid body"});
        return next();
    }
};

export {validationMiddleware};
