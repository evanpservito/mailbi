const dotenv = require("dotenv");
const twilio = require("twilio");

exports.handler = async (event, context, callback) => {
  const client = new twilio(
    process.env.VITE_TWILIO_ACCOUNT_SID,
    process.env.VITE_TWILIO_AUTH_TOKEN
  );

  await client.messages
    .create({
      body: event.queryStringParameters.message,
      to: event.queryStringParameters.recipient,
      from: process.env.VITE_TWILIO_PHONE_NUMBER,
    })
    .then((result) => {
      return callback(null, {
        statusCode: 200,
      });
    })
    .catch((error) => {
      return callback(error, {
        statusCode: 500,
      });
    });
};
