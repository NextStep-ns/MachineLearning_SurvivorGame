Installation :

	1-	Click on the following link: https://wetransfer.com/downloads/33268cc90bc57f27f6711f028d243bdf20240524212311/c59c327bb7107d6d8f9ce3f1e424ab4020240524212326/b13f48?trk=TRN_TDL_01&utm_campaign=TRN_TDL_01&utm_medium=email&utm_source=sendgrid
	2-	Download the .zip file
	3-	Unzip it

 
Launch:

To launch the game, you just launch main.py. Once main.py run, a menu is displayed, and you get many possibilities:

-	AI: An artificial intelligence will take control of the game

	o	Load: Use an already train model
			> Carrots:  Model with carrots only
			> Knife&Cows: Model with Knife&Cows
 	
	o	Train: Train the agent with an empty model
			> Carrots:  Train with carrots only
			> Knife&Cows: Train with Knife&Cows

-	Manual: You will play in manual mode.


Architecture:

CarrotGameAI
•	AI control --> Game controled by an AI.
 		- BestModel_Carrots
			- Tiled --> Folder containing all designs.
	  			- Island_map --> Tiled map and tilesets for the AI map.
	  			- […]
	  		2-   […]
•	Manual_game --> Game to play manually/solo.
  		- Map
 			- Designs_Candy
				- Designs of the game (PNG).
				- Tilesets --> Designs of the game (TMX).
			- Tiled_map --> Folder containing all documents used for the map.
		- Tiled --> Folder containing all images used in the code
		- […]
	
