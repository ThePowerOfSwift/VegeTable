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
import SwiftyJSON

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

   var dataReady = true    //dummy bool that the pic analysis method will return
   var riderid = 0
   var nutritionFacts = [String]()
   
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

   override func didReceiveMemoryWarning() {
      super.didReceiveMemoryWarning()
      // Dispose of any resources that can be recreated.
   }

   override func viewWillAppear(animated: Bool) {
      super.viewWillAppear(animated);
      //Question to consider, can this code be put in the viewDidLoad? Because everytime we return from the nutrition screen, this all happens all over again. Is this inefficient?
      //Also, could I make this "previewView" a custom UIView and put all this code in there? Not sure if possible or necessary
     
   }
   
   override func viewDidAppear(animated: Bool) {
      super.viewDidAppear(animated)
      //set the bounds of the previewLayer to equal the same as the view on our screen
      previewLayer!.frame = previewView.bounds      
   }
   
   override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
      if segue.identifier == "ShowNutritionSegue" {
         if let destinationViewController = segue.destinationViewController as? NutritionViewController {
            if(dataReady) {
               destinationViewController.foundData = true
               destinationViewController.data = nutritionFacts
               //also send the data for the fruit image and meal inspiration images
            } else {
               destinationViewController.foundData = false
            }
         }
      }
   
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
                
                let my_ip = "192.168.1.7"
//                let my_ip = "52.90.45.148"  // EC2 instance

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
                var responseString:NSString?
                let task = NSURLSession.sharedSession().dataTaskWithRequest(request) {
                    data, response, error in
                    
                    if error != nil {
                        print("error=\(error)")
                        return
                    }
                    
                    // You can print out response object
                    print("******* response = \(response)")
                    // Print out reponse body
                    responseString = NSString(data: data!, encoding: NSUTF8StringEncoding)
                    
                    print("****** Server Response Data: \(responseString!)")
                    
                    var err: NSError?
                    do {
                        if let json = try NSJSONSerialization.JSONObjectWithData(data!, options: .MutableContainers) as? NSDictionary {
                            // Success block...
                        }
                    } catch {
                        print(error)
                    }
                }
                
                task.resume()
               
                // use responseString (type: NSString) ->
                
                /* Add your json code herer! */
               
                //dataReady = bool returned from server indicating if information was found
                self.dataReady = true   //this is a dummy statement used for testing
                self.nutritionFacts = ["Mango", "100g", "60", "0", "0.5g", "1%", "0g", "0%", "0g", "5mg", "2%", "30 mg", "1%", "15g", "5%", "0g", "0%", "14g", "2g", "Vitamin A 2%", "Vitamin C 16%", "Calcium 2%", "Iron 33%", "Vitamin D 3%", "Potassium 1%", "Thiacin 3%", "Folate 4%", "Vitamin B 0%", "Vitamin K 1%", "Mango Sorbet", "Fried Fish w/ Mango", "Sticky Rice w/ Mango"]
                self.performSegueWithIdentifier("ShowNutritionSegue", sender: sender)
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