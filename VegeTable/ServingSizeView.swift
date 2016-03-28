//
//  ServingSizeView.swift
//  VegeTable
//
//  Created by Brian Tan on 3/23/16.
//  Copyright © 2016 Brian Tan. All rights reserved.
//

import UIKit

class ServingSizeView: UIView {
   
   //MARK: Properties
   //var servingSizeLabel : UILabel
   
   
   //MARK: Initialization
   required init?(coder aDecoder: NSCoder) {
      super.init(coder: aDecoder)
      
      //Serving Size Message
      let servingSizeMessage = UILabel(frame: CGRect(x: 50, y: 10, width: 300, height: 50))
      servingSizeMessage.adjustsFontSizeToFitWidth = true
      servingSizeMessage.font = UIFont(name: "Damion", size: 32)
      servingSizeMessage.textColor = UIColor.whiteColor()
      servingSizeMessage.textAlignment = .Center
      servingSizeMessage.text = "One Serving Size"
      addSubview(servingSizeMessage)
      
      //Seving Size Label
      let servingSizeLabel = UILabel(frame:CGRect(x: 75, y: 70, width: 200, height: 50))
      servingSizeLabel.adjustsFontSizeToFitWidth = true
      servingSizeLabel.font = UIFont(name: "Damion", size: 32)
      servingSizeLabel.textColor = UIColor.whiteColor()
      servingSizeLabel.textAlignment = .Center
      servingSizeLabel.text = "100g"
      addSubview(servingSizeLabel) 
      
      //Serving Size Picture
      //let servingSizeImage = UIImage.init(named: "StrawberryServing")
      
   }
   
   /*
   func changeServingSize(size : String) -> Void {
      servingSizeLabel.text = size
   }
   */
}
