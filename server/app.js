var express = require('express');
var app = express();
var path = require('path');
var bodyParser = require('body-parser');
var formidable = require('formidable');
var util = require('util');
var fs = require('fs-extra');
var qt = require('quickthumb');
var PythonShell = require('python-shell');
var AWS = require('aws-sdk');
var port  = 3001;

// Open Connection to DB
// Set your region for future requests.
//AWS.config.region = 'us-east-1';
AWS.config.update({region: "us-east-1",endpoint: "https://dynamodb.us-east-1.amazonaws.com"});
var docClient = new AWS.DynamoDB.DocumentClient();
var table = "FruitsAndVegetables";

app.use(bodyParser.urlencoded({ extended: false }));
//app.use(express.bodyParser({limit : '50mb'}));
//app.use(bodyParser.urlencoded({limit: '50mb', extended: true}));

// Use quickthumb
app.use(qt.static(__dirname + '/'));

// This is where the image is sent to
app.post('/upload', function (req, res){
  var form = new formidable.IncomingForm();
  form.parse(req, function(err, fields, files) {
    /*res.writeHead(200, {'content-type': 'text/plain'});
    res.write('received upload:\n\n');
    res.end(util.inspect({fields: fields, files: files}));*/
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
    var options = {args: [img_dir]};

    // Run the image processing here.
    PythonShell.run('my_script.py', options, function (err, results) { // options,
     if (err) throw err;
     var string_results = JSON.stringify(results);
     // results is an array consisting of messages collected during execution
     console.log('%s', string_results);

     // Add database connection here
     var FoodName = "Apple"; // This would technically be the results
     var params = {
         TableName: table,
         Key: {
           "FoodName":FoodName
         }
     };

     docClient.get(params, function(err, data) {
         if (err) {
             console.error("Unable to read item. Error JSON:", JSON.stringify(err, null, 2));
         } else {
             console.log("GetItem succeeded:", JSON.stringify(data, null, 2)); //This "data" variable is the one that needs to be sent back to the server
         }
     });

     // HERE HERE - Set the "string_result <= "data" variable from above"

     string_results = "{'Count':1,'Items':[{'Niacin':{'N':'0.091'},'Vitamin_B12_unit':{'S':'ug'},'Vitamin_A_RAE_unit':{'S':'ug'},'Sodium':{'N':'1'},'Monosaturated_Fat':{'N':'0.007'},'Thiamin':{'N':'0.017'},'Sugar':{'N':'10.39'},'Water_unit':{'S':'g'},'Carbohydrate_unit':{'S':'g'},'Iron_unit':{'S':'mg'},'Trans_Fat':{'N':'0'},'Sodium_unit':{'S':'mg'},'Saturated_Fat':{'N':'0.028'},'Vitamin_E':{'N':'0.18'},'Fiber':{'N':'2.4'},'Magnesium_unit':{'S':'mg'},'Saturated_Fat_unit':{'S':'g'},'Potassium':{'S':'mg'},'Protein_unit':{'S':'g'},'Water':{'N':'85.56'},'Energy_unit':{'S':'kcal'},'Cholesterol_unit':{'S':'mg'},'Vitamin_B6':{'N':'0.041'},'Fiber_unit':{'S':'g'},'Phosphorus':{'S':'mg'},'Zinc':{'N':'0.04'},'Folate_unit':{'S':'ug'},'Vitamin_C_unit':{'S':'mg'},'Vitamin_B12':{'N':'0'},'Calcium':{'N':'6'},'Vitamin_K_unit':{'S':'ug'},'Magnesium':{'N':'5'},'Iron':{'N':'0.12'},'Cholesterol':{'N':'0'},'Sugar_unit':{'S':'g'},'Fat_unit':{'S':'g'},'Fat':{'N':'0.17'},'Niacin_unit':{'S':'mg'},'FoodName':{'S':'Apple'},'Thiamin_unit':{'S':'mg'},'Monosaturated_Fat_unit':{'S':'g'},'Vitamin_K':{'N':'2.2'},'Polyunsaturated_Fat_unit':{'S':'g'},'Vitamin_C':{'N':'4.6'},'Energy':{'N':'52'},'Calcium_unit':{'S':'mg'},'Trans_Fat_unit':{'S':'g'},'Vitamin_D':{'S':'ug'},'Polyunsaturated_Fat':{'N':'0.051'},'Carbohydrate':{'N':'13.81'},'Zinc_unit':{'S':'mg'},'Vitamin_B6_unit':{'S':'mg'},'Vitamin_A_RAE':{'N':'3'},'Vitamin_E_unit':{'S':'mg'},'Protein':{'N':'0.26'},'Folate':{'N':'3'}}],'ScannedCount':1,'ConsumedCapacity':null}";



    res.writeHead(200, {'content-type': 'text/plain'}); // respond to IOS with result of the identification
    res.end(string_results);

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
