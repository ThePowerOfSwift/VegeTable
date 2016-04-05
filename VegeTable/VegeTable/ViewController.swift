//
//  ViewController.swift
//  VegeTable
//
//  Created by Brian Tan on 2/23/16.
//  Copyright © 2016 Brian Tan. All rights reserved.
//
//  tutorial for setting up camera was found at : http://drivecurrent.com/using-swift-and-avfoundation-to-create-a-custom-camera-view-for-an-ios-app/

import UIKit
import AVFoundation

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

   var dataReady = true    //dummy bool that the pic analysis method will return
   var riderid = 0

   @IBOutlet weak var takenImage: UIImageView!
   @IBOutlet weak var previewView: PreviewView!
   @IBOutlet weak var snapPhotoButton: UIButton!
   @IBOutlet weak var retakePhotoButton: UIButton!
   
   //Will make the time and battery bar appear white in app
   override func  preferredStatusBarStyle()-> UIStatusBarStyle {
    return UIStatusBarStyle.LightContent
   }
   
   //captureSession will hold the image taken from the camera and output it in a still image format
   var captureSession: AVCaptureSession?                 //this object will orchestrate input from camera and its output image
   var stillImageOutput: AVCaptureStillImageOutput?      //this object is the output the captureSession will be associated with
   var previewLayer: AVCaptureVideoPreviewLayer?         //this object will be the camera's preview and be visible on the screen
   
   override func viewDidLoad() {
      super.viewDidLoad()
      takenImage.hidden = true
      // Do any additional setup after loading the view, typically from a nib.
   }

   override func didReceiveMemoryWarning() {
      super.didReceiveMemoryWarning()
      // Dispose of any resources that can be recreated.
   }

   override func viewWillAppear(animated: Bool) {
      super.viewWillAppear(animated);
      //Question to consider, can this code be put in the viewDidLoad? Because everytime we return from the nutrition screen, this all happens all over again. Is this inefficient?
      //Also, could I make this "previewView" a custom UIView and put all this code in there? Not sure if possible or necessary
      
      //captureSession is created here
      captureSession = AVCaptureSession()
      
      //this gives our captureSession a preset fit for high resolution image taking
      captureSession!.sessionPreset = AVCaptureSessionPresetPhoto
      
      //setting up our capturing device as the rear camera
      let backCamera = AVCaptureDevice.defaultDeviceWithMediaType(AVMediaTypeVideo)
      
      //setting up a variable to be our camera input
      //before this input var was declared, our program only had reference to a device , the rear camera
      //but now, with an input our program has a reference to a capture session
      var error: NSError?
      var input: AVCaptureDeviceInput!
      do {
         input = try AVCaptureDeviceInput(device: backCamera)     //try to set input here, and catch any errors
      } catch let error1 as NSError {
            error = error1
            input = nil
      }
      
      //if there is no error in setting up out rear camera input, then link input with our captureSession
      if error == nil && captureSession!.canAddInput(input) {
            captureSession!.addInput(input)
            stillImageOutput = AVCaptureStillImageOutput()
         
            //setting up our output requires a data format, so we set out image to be a .jpeg file
            stillImageOutput!.outputSettings = [AVVideoCodecKey: AVVideoCodecJPEG]
         
            if captureSession!.canAddOutput(stillImageOutput) {
                //if possible add our rear camera output to our captureSession, now we have an input AND output associated with our cameraSession
                captureSession!.addOutput(stillImageOutput)
               
                //like snapchat, when you move the camera around, you expect to see a preview
                //we will have a previewLayer var which has a preview of our camera associated with our captureSession
                previewLayer = AVCaptureVideoPreviewLayer(session: captureSession)
                //setting videoGravity will make the image resize to fit in its container
                previewLayer!.videoGravity = AVLayerVideoGravityResize
                previewLayer!.connection?.videoOrientation = AVCaptureVideoOrientation.Portrait
                //here we add our previewLayer to the view on our screen
                previewView.layer.addSublayer(previewLayer!)
                captureSession!.startRunning()
            }
      }
   }
   
   override func viewDidAppear(animated: Bool) {
      super.viewDidAppear(animated)
      //set the bounds of the previewLayer to equal the same as the view on our screen
      previewLayer!.frame = previewView.bounds      
   }
    
   @IBAction func didPressTakePhoto(sender: UIButton) {
      //here we create a videoConnectiono object from the first connection in the array of connections on the stillImageOutput
      if let videoConnection = stillImageOutput!.connectionWithMediaType(AVMediaTypeVideo) {
         videoConnection.videoOrientation = AVCaptureVideoOrientation.Portrait
         
            //captureStillImageAsynchronouslyFromConnection function asynchronously calls it’s completion handler with the captured data in the sampleBuffer object
            stillImageOutput?.captureStillImageAsynchronouslyFromConnection(videoConnection, completionHandler: {(sampleBuffer, error) in
            //sampleBuffer is the data that contains our image and can be useful in a number of different ways
            //for our purposes we just need to format it in a way so it can be displayed in our ImageView
            if (sampleBuffer != nil) {
               //sampleBuffer is changed into JPEG format
               let imageData = AVCaptureStillImageOutput.jpegStillImageNSDataRepresentation(sampleBuffer)

               //All Code after this makes app act like SnapChat, where the taken image stay on the screen.
               //a data provider is created with the JPEG formatted image
               let dataProvider = CGDataProviderCreateWithCFData(imageData)
               let cgImageRef = CGImageCreateWithJPEGDataProvider(dataProvider, nil, true, CGColorRenderingIntent.RenderingIntentDefault)
               //let cgImageRef = CGImageCreateWithPNGDataProvider(dataProvider, nil, true, CGColorRenderingIntent.RenderingIntentDefault)
               //then the data provider is used to create a core graphics item to make a UIImage
               let image = UIImage(CGImage: cgImageRef!, scale: 1.0, orientation: UIImageOrientation.Right)
               //now finally, the UIImage is displayed on the imageView on our screen
               self.takenImage.image = image
               self.hidePreviewImage(true)
               
               //Setting the Nutrition Page picture the one we took, we dont actually want this when we are finalized
               //Image sending implementation based off of the tutorial found at: http://swiftdeveloperblog.com/image-upload-example/
                func generateBoundaryString() -> String {
                    return "Boundary-\(NSUUID().UUIDString)"
                }
                
                func createBodyWithParameters(parameters: [String: String]?, filePathKey: String?, imageDataKey: NSData, boundary: String) -> NSData {
                    let body = NSMutableData();
                    
                    if parameters != nil {
                        for (key, value) in parameters! {
                            body.appendString("--\(boundary)\r\n")
                            body.appendString("Content-Disposition: form-data; name=\"\(key)\"\r\n\r\n")
                            body.appendString("\(value)\r\n")
                        }
                    }
                    
                    // create random image name
                    var part1 = String(Int(arc4random_uniform(2147483648) + 1))
                    var part2 = String(Int(arc4random_uniform(2147483648) + 1))
                    let filename = part1 + part2 + ".jpg"
                    
                    let mimetype = "image/jpg"
                    
                    body.appendString("--\(boundary)\r\n")
                    body.appendString("Content-Disposition: form-data; name=\"\(filePathKey!)\"; filename=\"\(filename)\"\r\n")
                    body.appendString("Content-Type: \(mimetype)\r\n\r\n")
                    body.appendData(imageDataKey)
                    body.appendString("\r\n")
                    
                    
                    
                    body.appendString("--\(boundary)--\r\n")
                    
                    return body
                }
                
                
                let my_ip = "155.41.96.55"
                let myUrl = NSURL(string: "http://" + my_ip + ":3001/upload");
                let request = NSMutableURLRequest(URL:myUrl!);
                request.HTTPMethod = "POST";
                
                let param = [
                    "title"  : "test.jpeg"
                ]
                
                let boundary = generateBoundaryString()
                
                request.setValue("multipart/form-data; boundary=\(boundary)", forHTTPHeaderField: "Content-Type")
                
                
                let imageData1 = UIImageJPEGRepresentation(image, 1)
                
                if(imageData1==nil)  { return; }
                
                request.HTTPBody = createBodyWithParameters(param, filePathKey: "file", imageDataKey: imageData1!, boundary: boundary)
                
                let task = NSURLSession.sharedSession().dataTaskWithRequest(request) {
                    data, response, error in
                    
                    if error != nil {
                        print("error=\(error)")
                        return
                    }
                    
                    // You can print out response object
                    print("******* response = \(response)")
                    
                    // Print out reponse body
                    let responseString = NSString(data: data!, encoding: NSUTF8StringEncoding)
                    print("****** response data = \(responseString!)")
                    
                    var err: NSError?
                    do {
                        if let json = try NSJSONSerialization.JSONObjectWithData(data!, options: .MutableContainers) as? NSDictionary {
                            // Success block...
                        }
                    } catch {
                        print(error)
                    }
                    /*
                    if let parseJSON = json {
                    var firstNameValue = parseJSON["firstName"] as? String
                    println("firstNameValue: \(firstNameValue)")
                    }
                    */
                    
                }
                
                task.resume()

                
                
               
                
                
              // WORKING HTTP
               /*
               let send_string = "newDatafromIOS"
               let request = NSMutableURLRequest(URL: NSURL(string: "http://155.41.83.16:3001/text")!)
                request.HTTPMethod = "POST"
                let postString = "data=" + send_string
                request.HTTPBody = postString.dataUsingEncoding(NSUTF8StringEncoding)
                let task = NSURLSession.sharedSession().dataTaskWithRequest(request) { data, response,
                    error in guard error == nil && data != nil else {
                        // check for fundamental networking error
                        print("error=\(error)")
                        return
                    }
                    
                    if let httpStatus = response as? NSHTTPURLResponse where httpStatus.statusCode != 200 {           // check for http errors
                        print("statusCode should be 200, but is \(httpStatus.statusCode)")
                        print("response = \(response)")
                    }
                    
                    let responseString = NSString(data: data!, encoding: NSUTF8StringEncoding)
                    print("responseString = \(responseString)")
                }
                task.resume()*/
             
               
               
               //run method here to send our imageData NSData to the server for analysis
               //now with the return data, segue to our tableview controller and populate the cells with the data
                
               if self.dataReady {
                  //performSegue to the tableview controller
                  self.performSegueWithIdentifier("ShowNutritionSegue", sender: sender)
                  
                  /* this code can possibly help transfer data from online to our model
                  prepareForSegue:(UIStoryboardSegue *)segue sender:(id)sender
                  {
                     if ([[segue identifier] isEqualToString:@"MySegue"]) {

                        // Get destination view
                        SecondView *vc = [segue destinationViewController];

                        // Get button tag number (or do whatever you need to do here, based on your object
                        NSInteger tagIndex = [(UIButton *)sender tag];

                        // Pass the information to your destination view
                        [vc setSelectedButton:tagIndex];
                     }
                  }
                  */
               }
               
             
            }
         })
      }
   }
   
   @IBAction func retakePhoto(sender: UIButton) {
      hidePreviewImage(false)
   }
   
   func hidePreviewImage(decision: Bool) -> Void {
      self.previewView.hidden = decision
      self.snapPhotoButton.hidden = decision
      self.takenImage.hidden = !decision
      //self.retakePhotoButton.hidden = !decision
   }
   

    @IBAction func myUnwindAction(unwindSegue: UIStoryboardSegue) {
    }

}

extension NSMutableData {
    
    func appendString(string: String) {
        let data = string.dataUsingEncoding(NSUTF8StringEncoding, allowLossyConversion: true)
        appendData(data!)
    }
}