const express = require("express");
const bodyParser = require("body-parser");

const app = express();
app.use(bodyParser.urlencoded({extended: true}));

app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});

app.get("/mint", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});

app.listen(process.env.PORT || 6969, function(){
    console.log("Server is running on port 3000");
});