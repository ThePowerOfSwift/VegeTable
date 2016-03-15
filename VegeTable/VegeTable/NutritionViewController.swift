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
   
   //Nutrition Facts Labels
   @IBOutlet weak var servingSizeValue: UILabel!
   @IBOutlet weak var calorieValue: UILabel!
   @IBOutlet weak var caloriesFromFat: UILabel!
   @IBOutlet weak var totalFatValue: UILabel!
   @IBOutlet weak var totalFatPercentage: UILabel!
   @IBOutlet weak var saturatedFatValue: UILabel!
   @IBOutlet weak var saturatedFatPercentage: UILabel!
   @IBOutlet weak var transFatValue: UILabel!
   @IBOutlet weak var cholesterolValue: UILabel!
   @IBOutlet weak var cholesterolPercentage: UILabel!
   @IBOutlet weak var sodiumValue: UILabel!
   @IBOutlet weak var sodiumPercentage: UILabel!
   @IBOutlet weak var totalCarbsValue: UILabel!
   @IBOutlet weak var totalCarbsPercentage: UILabel!
   @IBOutlet weak var fiberValue: UILabel!
   @IBOutlet weak var fiberPercentage: UILabel!
   @IBOutlet weak var sugarValue: UILabel!
   @IBOutlet weak var proteinValue: UILabel!
   
   //Dummy data
   var data = ["60", "0", "0.5g", "1%", "0g", "0%", "0g", "5mg", "2%", "30 mg", "1%", "15g", "5%", "0g", "0%", "14g", "2g", "100g"]
   
   
   override func viewDidLoad() {
      super.viewDidLoad()
      
      self.NutritionScrollView.scrollEnabled = true
      self.NutritionScrollView.contentSize.height = 1200
        
      self.databaseImage.layer.cornerRadius = self.databaseImage.frame.size.height/2
      self.databaseImage.clipsToBounds = true
      self.databaseImage.layer.borderWidth = 4.0
      self.databaseImage.layer.borderColor = UIColor(red:15/255.0, green:243/255.0, blue:106/255.0, alpha: 1.0).CGColor
      
      setNutritionFacts(data); 
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
   
   func setNutritionFacts(facts: [String]) -> Void {
      if facts.count != 18 {
      //if we do not receive all facts, the placement of them on the view will be off
         return
      }
      servingSizeValue.text = facts[17];
      calorieValue.text = facts[0];
      caloriesFromFat.text = facts[1];
      totalFatValue.text = facts[2];
      totalFatPercentage.text = facts[3];
      saturatedFatValue.text = facts[4];
      saturatedFatPercentage.text = facts[5];
      transFatValue.text = facts[6];
      cholesterolValue.text = facts[7];
      cholesterolPercentage.text = facts[8];
      sodiumValue.text = facts[9];
      sodiumPercentage.text = facts[10];
      totalCarbsValue.text = facts[11];
      totalCarbsPercentage.text = facts[12];
      fiberValue.text = facts[13];
      fiberPercentage.text = facts[14];
      sugarValue.text = facts[15];
      proteinValue.text = facts[16];
      
      
   }
}
