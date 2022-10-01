const express = require('express');

const app = express();

app.get("/", (request, response) => {
    console.log("get request for home route");
    response.sendFile(__dirname + "/index.html");
    console.log("sent index.html");
});

app.post("/add", (request, response) => {
    console.log("12 request.params: ", request.params);
    response.redirect(307, "/");
    console.log("redirected to home route");
});

const port = process.env.PORT || 3000;
app.listen(port, () => console.log("nftspaces express app listening on port " + port));