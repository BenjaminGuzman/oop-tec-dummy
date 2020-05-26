import express from "express";
import helmet from "helmet";
import dotenv from "dotenv";
import bodyParser from "body-parser";

dotenv.config();

const PORT = process.env.PORT || 8080;

const app = express();

app.use(helmet());
app.use(bodyParser.json());

app.listen(PORT, () => {
    console.log(`Server running on port ${PORT}`);
});
