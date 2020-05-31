"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const dotenv_1 = __importDefault(require("dotenv"));
const morgan_1 = __importDefault(require("morgan"));
dotenv_1.default.config();
const express_1 = __importDefault(require("express"));
const helmet_1 = __importDefault(require("helmet"));
const body_parser_1 = __importDefault(require("body-parser"));
const get_1 = require("./routes/get");
const put_1 = require("./routes/put");
const PORT = process.env.PORT || 8080;
const app = express_1.default();
app.use(helmet_1.default());
app.use(morgan_1.default("combined"));
app.use(body_parser_1.default.json());
// app.get('/', getRouter);
app.use(get_1.router);
app.use(put_1.router);
app.use((req, res) => res.status(404).end());
app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
