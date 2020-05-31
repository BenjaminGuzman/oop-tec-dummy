import dotenv from "dotenv";
import morgan from "morgan";
dotenv.config();

import express from "express";
import helmet from "helmet";
import bodyParser from "body-parser";
import {router as getRouter} from "./routes/get";
import {router as updateRouter} from "./routes/put";

const PORT = process.env.PORT || 8080;

const app = express();

app.use(helmet());
app.use(morgan("combined"));
app.use(bodyParser.json());

// app.get('/', getRouter);
app.use(getRouter);
app.use(updateRouter);

app.use((req, res) => res.status(404).end());

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
