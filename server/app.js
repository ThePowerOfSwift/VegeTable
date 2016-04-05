var express = require('express');
var app = express();
var path = require('path');
var bodyParser = require('body-parser');
var formidable = require('formidable');
var util = require('util');
var fs = require('fs-extra');
var qt = require('quickthumb');
var PythonShell = require('python-shell');
var port  = 3001;

app.use(bodyParser.urlencoded({ extended: false }));
//app.use(express.bodyParser({limit : '50mb'}));
//app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

// Use quickthumb
app.use(qt.static(__dirname + '/'));

app.post('/upload', function (req, res){
  var form = new formidable.IncomingForm();
  form.parse(req, function(err, fields, files) {
    res.writeHead(200, {'content-type': 'text/plain'});
    res.write('received upload:\n\n');
    res.end(util.inspect({fields: fields, files: files}));
  });

  form.on('end', function(fields, files) {
    /* Temporary location of our uploaded file */
    var temp_path = this.openedFiles[0].path;
    /* The file name of the uploaded file */
    var file_name = this.openedFiles[0].name;
    /* Location where we want to copy the uploaded file */
    var new_location = 'uploads/';

    fs.copy(temp_path, new_location + file_name, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("success!")
      }
    });

    var img_dir = new_location + file_name;
    var options = {
    // mode: 'text',
    // pythonPath: '/',
     //pythonOptions: ['-u'],
     //scriptPath: 'path/to/my/scripts',
     args: [img_dir]
    };

    PythonShell.run('my_script.py', options, function (err, results) { // options,
     if (err) throw err;
     // results is an array consisting of messages collected during execution
     console.log('%s', results);
   });


  });
});

// Show the upload form
app.get('/', function (req, res){
  res.writeHead(200, {'Content-Type': 'text/html' });
  var form = 'Success!<br><br>'+
              '<form action="/upload" enctype="multipart/form-data" method="post">' +
              '<input multiple="multiple" name="upload" type="file" /><br><br>' +
              '<input type="submit" value="Upload" /></form>';
  res.end(form);
  app.use(express.static(__dirname + '/'));
});

app.post('/text', function(req, res) {
    console.log(req.body);
    res.send("successfully sent"); //  console.log(JSON.stringify(req.body.params));
});

app.listen(port);
console.log('server started on port %s', port);
