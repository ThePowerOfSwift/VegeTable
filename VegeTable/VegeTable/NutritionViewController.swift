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
   @IBOutlet weak var fruitNameLabel: UILabel!
   @IBOutlet weak var servingSizeImage: UIImageView!
   
   
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
   @IBOutlet weak var nutriMin1: UILabel!
   @IBOutlet weak var nutriMin2: UILabel!
   @IBOutlet weak var nutriMin3: UILabel!
   @IBOutlet weak var nutriMin4: UILabel!
   
   //Dummy data
   var data = ["100g", "60", "0", "0.5g", "1%", "0g", "0%", "0g", "5mg", "2%", "30 mg", "1%", "15g", "5%", "0g", "0%", "14g", "2g", "Vitamin A 2%", "Vitamin C 16%", "Calcium 2%", "Iron 3%"]
   
   
   override func viewDidLoad() {
      super.viewDidLoad()
      
      self.NutritionScrollView.scrollEnabled = true
      self.NutritionScrollView.contentSize.height = 1800
      
      //Fruit Identity View
      self.fruitNameLabel.text = "Strawberry"
      self.databaseImage.image = UIImage(named:"strawberry.jpg")
      self.databaseImage.layer.cornerRadius = self.databaseImage.frame.size.height/2
      self.databaseImage.clipsToBounds = true
      self.databaseImage.layer.borderWidth = 4.0
      self.databaseImage.layer.borderColor = UIColor(red:15/255.0, green:243/255.0, blue:106/255.0, alpha: 1.0).CGColor
      
      //Nutritional Facts View
      setNutritionFacts(data);
      
      
      //Serving Size View
      self.servingSizeImage.image = UIImage(named: "servingOfStrawberries.jpg");
      /*
      self.servingSizeImage.layer.cornerRadius = self.servingSizeImage.frame.size.height/2
      self.servingSizeImage.clipsToBounds = true
      self.servingSizeImage.layer.borderWidth = 2.0
      self.servingSizeImage.layer.borderColor = UIColor.whiteColor().CGColor
      */
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
      //HAVE THIS CALL THE HIDEPREVIEWIMAGE METHOD FROM VIEWCONTROLLER
      
      
   }
   
   func setNutritionFacts(facts: [String]) -> Void {
      if facts.count != 22 {
      //if we do not receive all facts, the placement of them on the view will be off
         return
      }
      servingSizeValue.text = facts[0];
      calorieValue.text = facts[1];
      caloriesFromFat.text = facts[2];
      totalFatValue.text = facts[3];
      totalFatPercentage.text = facts[4];
      saturatedFatValue.text = facts[5];
      saturatedFatPercentage.text = facts[6];
      transFatValue.text = facts[7];
      cholesterolValue.text = facts[8];
      cholesterolPercentage.text = facts[9];
      sodiumValue.text = facts[10];
      sodiumPercentage.text = facts[11];
      totalCarbsValue.text = facts[12];
      totalCarbsPercentage.text = facts[13];
      fiberValue.text = facts[14];
      fiberPercentage.text = facts[15];
      sugarValue.text = facts[16];
      proteinValue.text = facts[17];
      nutriMin1.text = facts[18];
      nutriMin2.text = facts[19];
      nutriMin3.text = facts[20];
      nutriMin4.text = facts[21];
   }
}
