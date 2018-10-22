const fs = require("fs");
const path = require('path');
const http = require('http');
const qs = require('querystring');

function User(name, initialList) {
    this.name = name;
    this.list = initialList;
}

User.prototype.addList = function(text) {
    this.list.push(text);
}

User.prototype.remove = function(index) {
    // Removes the item at index -->
    this.list.splice(index, 1);
}

var users = {};

function loadFile(filePath, callback) {
    let readStream = fs.createReadStream(path.join(__dirname, filePath));
    readStream.on("error", (err) => {
        callback(err, null);
    });

    let data = "";

    readStream.on("data", (chunk) => {
        data += chunk.toString("utf8");
    });

    readStream.on("end", () => {
        callback(null, data);
    });
}

function serveIndex(req, res) {
    // console.log("Index!");
    let indexPath = path.join("public", "index.html");
    loadFile(indexPath, (err, data) => {
        if(err) throw err;
        res.writeHead(200, {'Content-Type': "text/html"});
        res.end(data);
    })
}

function serveStatic(req, res) {
    // console.log("Static: " + req.url);
    loadFile(path.join("static", req.url), (err, data) => {
        if(req.url.split("/")[1] === "javascript") {
            res.writeHead(200, {'Content-Type': 'text/javascript'});
        } else {
            res.writeHead(200, {'Content-Type': "text/css"});
        }

        res.end(data);
    });
}

function parseRequestData(req, res, callback) {
    let data = "";
    req.on("data", (chunk) => data += chunk.toString("utf8"));
    req.on("end", () => {
        callback(data);
    });
}

function login(req, res) {

    parseRequestData(req, res, (data) => {
        let parsedData = qs.parse(data);
        // console.log(parsedData);
        res.writeHead(200, {"Content-Type": "application/json"});
        if(!parsedData.username) {
            res.end(JSON.stringify({error: 'No username parameter!'}));
        } else {
            let clientName = parsedData.username;

            // Add user to users if it doesn't exist -->
            if(!users[clientName]) {
                users[clientName] = new User(clientName, []);
            }

            // Return user object -->
            res.end(JSON.stringify({'user': users[clientName]}));
        }
    });

    // let data = "";
    // req.on("data", (chunk) => data += chunk.toString("utf8"));
    // req.on("end", () => {
    // });
}

function remove(req, res) {
    let data = "";
    req.on("data", (chunk) => data += chunk.toString("utf8"));
    req.on("end", () => {
        let parsedData = qs.parse(data);
        res.writeHead(200, {'Content-Type': 'application/json'});
        // console.log(parsedData);

        if(!users[parsedData['user[name]']]) {
            res.end(JSON.stringify({error: 'No user data!'}));
        } else {
            let user = users[parsedData['user[name]']];
            let index = parsedData['index'];
            user.remove(index);
            // console.log(users);
            res.end(JSON.stringify({success: true, 'new_list': user.list}));
        }
    });
}

function add(req, res) {
    let data = "";
    req.on("data", (chunk) => data += chunk.toString("utf8"));
    req.on("end", () => {
        let parsedData = qs.parse(data);
        res.writeHead(200, {'Content-Type': "application/json"});
        let response = {};
        // If can't find user with username that is requested, send error.
        if(Object.keys(users).indexOf(parsedData['user[name]']) === -1) {
            response['error'] = "No user with that username!";
        } else {

            // Add new item to list -->
            let user = users[parsedData['user[name]']];
            let item = parsedData['item'];

            user.addList(item);
            response['new_list'] = user.list
        }

        res.end(JSON.stringify(response));
    })
}

function router(req, res) {
    var url = req.url;
    if(url === "/index" || url === "/") {
        serveIndex(req, res);
    } else if(url === "/login" && req.method === "POST") {
        login(req, res)
    } else if(url === "/remove" && req.method === "POST"){
        remove(req, res);
    } else if(url === "/add" && req.method === "POST") {
        add(req, res);
    } else {
        serveStatic(req, res);
    }
}

let server = http.createServer((req, res) => {
    router(req, res);
}).listen(3000, () => {
    console.log("Server started!");
});
