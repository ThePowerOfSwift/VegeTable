//
//  NutritionViewController.swift
//  VegeTable
//
//  Created by Brian Tan on 3/14/16.
//  Copyright © 2016 Brian Tan. All rights reserved.
//

import UIKit

class NutritionViewController: UIViewController {

   @IBOutlet weak var NutritionScrollView: UIScrollView!
   @IBOutlet weak var databaseImage: UIImageView!
   
   
    override func viewDidLoad() {
        super.viewDidLoad()
        self.databaseImage.layer.cornerRadius = self.databaseImage.frame.size.height/2
        self.databaseImage.clipsToBounds = true
    }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    

    /*
    // MARK: - Navigation

    // In a storyboard-based application, you will often want to do a little preparation before navigation
    override func prepareForSegue(segue: UIStoryboardSegue, sender: AnyObject?) {
        // Get the new view controller using segue.destinationViewController.
        // Pass the selected object to the new view controller.
    }
    */

   @IBAction func backToCameraPress(sender: UIButton) {
      self.performSegueWithIdentifier("ShowCameraSegue", sender: sender)
   }
}
