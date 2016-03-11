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

   @IBOutlet weak var takenImage: UIImageView!
   @IBOutlet weak var previewView: UIView!
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
      //set the bounds of the previewLayr to equal the same as the view on our screen
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
               //a data provider is created with the JPEG formatted image
               let dataProvider = CGDataProviderCreateWithCFData(imageData)
               let cgImageRef = CGImageCreateWithJPEGDataProvider(dataProvider, nil, true, CGColorRenderingIntent.RenderingIntentDefault)
               //then the data provider is used to create a core graphics item to make a UIImage
               let image = UIImage(CGImage: cgImageRef!, scale: 1.0, orientation: UIImageOrientation.Right)
               //now finally, the UIImage is displayed on the imageView on our screen
               //NOTE: here is where you can send the image data to a server, or the VegeTable server for analysis
               //side note, to make the image fill the view I went to mainstoryboard and set the mode of the imageview to Scale to Fill
               self.takenImage.image = image
               
               self.takenImage.hidden = false
               self.previewView.hidden = true
               self.snapPhotoButton.hidden = true
               self.retakePhotoButton.hidden = false
               
            }
         })
      }
   }
   
   @IBAction func retakePhoto(sender: UIButton) {
      //Set availability of buttons
      self.snapPhotoButton.hidden = false
      self.retakePhotoButton.hidden = true
      
      //Set availability of camera preview and taken pic
      self.previewView.hidden = false
      self.takenImage.hidden = true
   
   }

}

