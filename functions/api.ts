const dotenv = require("dotenv");
const express = require("express");
const cors = require("cors");
const twilio = require("twilio");
const serverless = require("serverless-http");

// TODO: CHANGE TO ENV
const client = new twilio(
  process.env.VITE_TWILIO_ACCOUNT_SID,
  process.env.VITE_TWILIO_AUTH_TOKEN
);

const app = express();
app.use(cors());
const router = express.Router();

router.get("/", (res) => {
  res.send("Hello");
});

router.get("/send-text", (req, res) => {
  const { recipient, message } = req.query;
  client.messages
    .create({
      body: message,
      to: recipient,
      from: process.env.VITE_TWILIO_PHONE_NUMBER,
    })
    .then((message) => console.log("Message sent successfully."))
    .err("Error");
});
app.use("/api/", router);
// app.listen(3001, () => console.log("Running on port 3001"));
module.exports.handler = serverless(app);
