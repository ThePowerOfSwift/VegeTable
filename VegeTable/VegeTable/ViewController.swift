//
//  ViewController.swift
//  VegeTable
//
//  Created by Brian Tan on 2/23/16.
//  Copyright © 2016 Brian Tan. All rights reserved.
//

import UIKit

class ViewController: UIViewController, UIImagePickerControllerDelegate, UINavigationControllerDelegate {

   @IBOutlet weak var imageView: UIImageView!
   
   override func viewDidLoad() {
      super.viewDidLoad()
      // Do any additional setup after loading the view, typically from a nib.
   }

   override func didReceiveMemoryWarning() {
      super.didReceiveMemoryWarning()
      // Dispose of any resources that can be recreated.
   }

   @IBAction func chooseImageFromPhotoLibrary() {
      let picker = UIImagePickerController()
      
      picker.delegate = self
      //implement isSourceTypeAvailable to make sure it is safe to use the source
      picker.sourceType = .SavedPhotosAlbum
      presentViewController(picker, animated: true, completion: nil)
   }
   
   @IBAction func chooseFromCamera() {
      let picker = UIImagePickerController()
      
      picker.delegate = self
      //implement isSourceTypeAvailable to make sure it is safe to use the source
      picker.sourceType = .Camera
      presentViewController(picker, animated: true, completion: nil)
   }
   
   func imagePickerController(picker: UIImagePickerController, didFinishPickingImage image: UIImage, editingInfo: [String : AnyObject]?) {
      imageView.image = image
      dismissViewControllerAnimated(true, completion: nil)
   }
   
   
   

}

