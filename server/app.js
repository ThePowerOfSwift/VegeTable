var express = require('express');
var app = express();
var path = require('path');
var bodyParser = require('body-parser');
var port  = 3001;

app.use(bodyParser.urlencoded({ extended: false }))

// viewed at http://localhost:3001
app.get('/', function(req, res) {
    /* Send over the index html file */
    res.sendFile(path.join(__dirname + '/index.html'));

    /* Grab data beyond the basic directory */
    app.use(express.static(__dirname + '/'));
});

app.post('/text', function(req, res) {
    console.log(req.body.data);
    res.send("successfully sent");
});


app.listen(port);
console.log('server started on port %s', port);
