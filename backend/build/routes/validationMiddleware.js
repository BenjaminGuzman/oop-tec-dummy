"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.validationMiddleware = void 0;
const validationMiddleware = (validationFn) => {
    return (req, res, next) => {
        const is_body_valid = validationFn(req.body);
        if (!is_body_valid)
            return res.status(400).send({ error: "invalid body" });
        return next();
    };
};
exports.validationMiddleware = validationMiddleware;
