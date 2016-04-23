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
   
   //Fruit Identity View
   @IBOutlet weak var databaseImage: UIImageView!
   @IBOutlet weak var fruitNameLabel: UILabel!
   @IBOutlet weak var errorLabel: UILabel!
   
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
   @IBOutlet weak var nutriMin5: UILabel!
   @IBOutlet weak var nutriMin6: UILabel!
   @IBOutlet weak var nutriMin7: UILabel!
   @IBOutlet weak var nutriMin8: UILabel!
   @IBOutlet weak var nutriMin9: UILabel!
   @IBOutlet weak var nutriMin10: UILabel!
   
   //Serving Size Images and Labels
   @IBOutlet weak var sSizeImage100g: UIImageView!
   @IBOutlet weak var sSizeImage1cup: UIImageView!
   @IBOutlet weak var sSize1cupLabel: UILabel!
   
   
   //Meal Inspirations Images and Labels
   @IBOutlet weak var mealInspImage1: UIImageView!
   @IBOutlet weak var mealInspImage2: UIImageView!
   @IBOutlet weak var mealInspImage3: UIImageView!
   @IBOutlet weak var mealInspLabel1: UILabel!
   @IBOutlet weak var mealInspLabel2: UILabel!
   @IBOutlet weak var mealInspLabel3: UILabel!
   
   //Nutrition Facts in a String array
   var data = [String]()
   var foundData = true
   
   
   override func viewDidLoad() {
      super.viewDidLoad()

      self.databaseImage.layer.cornerRadius = self.databaseImage.frame.size.height/2
      self.databaseImage.clipsToBounds = true
      self.databaseImage.layer.borderWidth = 4.0
      self.databaseImage.layer.borderColor = UIColor(red:15/255.0, green:243/255.0, blue:106/255.0, alpha: 1.0).CGColor
      
      if(foundData) {
         setNutritionFacts(data)
         grabPictures()
      } else {
         showError()
      }
      
   }

    override func didReceiveMemoryWarning() {
        super.didReceiveMemoryWarning()
        // Dispose of any resources that can be recreated.
    }
    
   //Will make the time and battery bar appear white in app
   override func  preferredStatusBarStyle()-> UIStatusBarStyle {
    return UIStatusBarStyle.LightContent
   } 

   @IBAction func backToCameraPress(sender: UIButton) {
      self.performSegueWithIdentifier("ShowCameraSegue", sender: sender)
      //HAVE THIS CALL THE HIDEPREVIEWIMAGE METHOD FROM VIEWCONTROLLER
      
      
   }
   
   func setNutritionFacts(facts: [String]) -> Void {
      if facts.count != 32 {
      //if we do not receive all facts, the placement of them on the view will be off
         return
      }
      
      fruitNameLabel.hidden = false
      errorLabel.hidden = true
      
      fruitNameLabel.text = facts[0]
      servingSizeValue.text = facts[1]
      calorieValue.text = facts[2]
      caloriesFromFat.text = facts[3]
      totalFatValue.text = facts[4]
      totalFatPercentage.text = facts[5]
      saturatedFatValue.text = facts[6]
      saturatedFatPercentage.text = facts[7]
      transFatValue.text = facts[8]
      cholesterolValue.text = facts[9]
      cholesterolPercentage.text = facts[10]
      sodiumValue.text = facts[11]
      sodiumPercentage.text = facts[12]
      totalCarbsValue.text = facts[13]
      totalCarbsPercentage.text = facts[14]
      fiberValue.text = facts[15]
      fiberPercentage.text = facts[16]
      sugarValue.text = facts[17]
      proteinValue.text = facts[18]
      nutriMin1.text = facts[19]
      nutriMin2.text = facts[20]
      nutriMin3.text = facts[21]
      nutriMin4.text = facts[22]
      nutriMin5.text = facts[23]
      nutriMin6.text = facts[24]
      nutriMin7.text = facts[25]
      nutriMin8.text = facts[26]
      nutriMin9.text = facts[27]
      nutriMin10.text = facts[28]
      mealInspLabel1.text = facts[29]
      mealInspLabel2.text = facts[30]
      mealInspLabel3.text = facts[31]
   }
   
   func grabPictures() -> Void {
      //find URLs in final iteration
      self.databaseImage.image = UIImage(named:"mango.jpg")
      
      self.sSizeImage100g.image = UIImage(named: "bowlOfMango.jpg")
      self.sSizeImage1cup.image = UIImage(named: "bowlOfMango.jpg")
      self.mealInspImage1.image = UIImage(named: "mangoSorbet.jpg")
      self.mealInspImage2.image = UIImage(named: "wholeFishWMango.jpg")
      self.mealInspImage3.image = UIImage(named: "stickyRiceWMango.jpg")
   }
   
   func showError() -> Void {
      fruitNameLabel.hidden = true
      errorLabel.hidden = false
      
      databaseImage.image = UIImage(named: "bananaPeel.jpg" )
      servingSizeValue.text = "100g"
      calorieValue.text = "0"
      caloriesFromFat.text = "0g"
      totalFatValue.text = "0g"
      totalFatPercentage.text = "0%"
      saturatedFatValue.text = "0g"
      saturatedFatPercentage.text = "0%"
      transFatValue.text = "0g"
      cholesterolValue.text = "0g";
      cholesterolPercentage.text = "0%"
      sodiumValue.text = "0g"
      sodiumPercentage.text = "0%"
      totalCarbsValue.text = "0g"
      totalCarbsPercentage.text = "0%"
      fiberValue.text = "0g"
      fiberPercentage.text = "0%"
      sugarValue.text = "0g"
      proteinValue.text = "0g"
      nutriMin1.text = "Vibranium 43g"
      nutriMin2.text = "Vitamin-C Yes"
      nutriMin3.text = "Cyanide 0.2mg"
      nutriMin4.text = "Fluff 500g"
      nutriMin5.text = "Midichlorians 0.1ug"
      nutriMin6.text = "X-factor 3.4g"
      nutriMin7.text = "Vitamin-Z 50g"
      nutriMin8.text = "Humanity 73mg"
      nutriMin9.text = "Mana 2 Points"
      nutriMin10.text = "Valyrium 6mg"
      
      self.sSizeImage100g.image = UIImage(named: "bananaPeel2.png");
      self.sSizeImage1cup.image = UIImage(named: "bananaPeel3.png");
      self.mealInspImage1.image = UIImage(named: "bananaPeel4.png")
      self.mealInspImage2.image = UIImage(named: "bananaPeel5.jpg")
      self.mealInspImage3.image = UIImage(named: "bananaPeel6.jpg")
      self.mealInspLabel1.text = "Chicken Cacciatore"
      self.mealInspLabel2.text = "Bangers and Mash"
      self.mealInspLabel3.text = "Eggplant Parmesan"
   }
}
