const express = require('express');
const http = require('http');
var app = express();
app.use(express.static(__dirname + "/public/"));

app.get("/", function(req, res) {
    res.sendFile(__dirname + "/index.html");
});
var server = http.createServer(app);
server.listen(3000, () => {
    console.log(3000);
});
