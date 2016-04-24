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

var net = require('net');

var pyHOST = '127.0.0.1';
var pyPORT = 9999;
var client = new net.Socket();

app.use(bodyParser.urlencoded({ extended: false }));
//app.use(express.bodyParser({limit : '50mb'}));
//app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

// Use quickthumb
app.use(qt.static(__dirname + '/'));

// This is where the image is sent to
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
    var new_location = __dirname+'/uploads/';

    fs.copy(temp_path, new_location + file_name, function(err) {
      if (err) {
        console.error(err);
      } else {
        console.log("File Uploaded!")
        client.connect(pyPORT, pyHOST, function() {

          console.log('CONNECTED TO: ' + pyHOST + ':' + pyPORT);
          // Write a message to the socket as soon as the client is connected, the server will receive it as message from the client 
          client.write(img_dir);

        });
      }
    });

    var img_dir = new_location + file_name;
    var options = {args: [img_dir]};

   //  // Run the image processing here.
   //  PythonShell.run('../VegeTable/image_recognition/VegeTable_Neural_Network_Matching_Apple.py', options, function (err, results) { // options,
   //   if (err) throw err;
   //   // results is an array consisting of messages collected during execution
   //   console.log('%s', results);
   // });
    

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

// Add a 'data' event handler for the client socket
// data is what the server sent to this socket
client.on('data', function(data) {
    
    console.log('Match Result: ' + data);
    // Close the client socket completely
    client.destroy();
    
});

// Add a 'close' event handler for the client socket
client.on('close', function() {
    console.log('Connection closed');
});

var getNetworkIP = (function () {
    var ignoreRE = /^(127\.0\.0\.1|::1|fe80(:1)?::1(%.*)?)$/i;

    var exec = require('child_process').exec;
    var cached;    
    var command;
    var filterRE;

    switch (process.platform) {
    // TODO: implement for OSs without ifconfig command
    case 'darwin':
         command = 'ifconfig';
         filterRE = /\binet\s+([^\s]+)/g;
         // filterRE = /\binet6\s+([^\s]+)/g; // IPv6
         break;
    default:
         command = 'ifconfig';
         filterRE = /\binet\b[^:]+:\s*([^\s]+)/g;
         // filterRE = /\binet6[^:]+:\s*([^\s]+)/g; // IPv6
         break;
    }

    return function (callback, bypassCache) {
         // get cached value
        if (cached && !bypassCache) {
            callback(null, cached);
            return;
        }
        // system call
        exec(command, function (error, stdout, sterr) {
            var ips = [];
            // extract IPs
            var matches = stdout.match(filterRE);
            // JS has no lookbehind REs, so we need a trick
            for (var i = 0; i < matches.length; i++) {
                ips.push(matches[i].replace(filterRE, '$1'));
            }

            // filter BS
            for (var i = 0, l = ips.length; i < l; i++) {
                if (!ignoreRE.test(ips[i])) {
                    //if (!error) {
                        cached = ips[i];
                    //}
                    callback(error, ips[i]);
                    return;
                }
            }
            // nothing found
            callback(error, null);
        });
    };
})();

app.listen(port);
getNetworkIP(function (error, ip) {
    console.log('server started on %s:%s',ip,port);
    if (error) {
        console.log('error:', error);
    }
}, false);



