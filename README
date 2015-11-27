#AI Directions

Use arrow keys to move.

To tweak  most settings of the program, look for the #Config variables, 
located around line 62. Below the Function Declarations. 

REMEMBER WHEN CREATING TRAINING DATA WE NEED TO SET THE BEST POSSIBLE EXAMPLE FOR THE 
AI. IT IS LIKE A CHILD, AND WE HAVE TO BE THE BEST ROLE MODELS WE CAN BE. WITH THAT IN MIND,
IF YOU THINK A PREVIOUS PLAYTHROUGH COULD HAVE BEEN DONE BETTER, JUST DELETE IT FROM THE
FOLDER. NO SLOPPY PLAYTHROUGHS. :)

##Quick How tos:
  ####Save Current Play Data:
    Set humanTrain = True
    Once you die, the playthough is saved to a file with the name { Date Time (snake length) }

    ***The file only saves up until the last apple is gotten *** 
    This means that the file will not save the information of where the snake collides into
    a wall or itself.

  ####Loading Past Plays:
    Set loadData = true
    Set dataSrc = "Your file name"  
    *** If Human Train mode is on... then this will save the snakeframe queue to a DIFFERENT file, 
    but containing ONLY the data from the current play.

  ####Interpret Save File Data
    Each line of the file is one frame of the playthrough. The format looks like:
    (Snake X position) (snake Y position) (Apple Position) (Snake Length) (Snake Position)

  ####Play Game Normally:
    Set humanTrain = False

  ####Change Snake Starting Length:
    Set startSquares = (Length Desired)


##About Human Train Mode:
  How to activate Human Train Mode? Set humanTrain = true

  Human Train Mode will record the snake and the apples position, the direction
  of the snake and the the length of the snake for each frame. This will be placed
  in an object called SnakeFrame. There is a list of SnakeFrames that is saved to a file
  when the snake dies.
 
  ***The file only saves up until the last apple is gotten *** 
  This means that the file will not save the information of where the snake collides into
  a wall or itself.

  File Format:
  Each line of the file is one frame of the playthrough. The format looks like:
  (Snake X position) (snake Y position) (Apple Position) (Snake Length) (Snake Position)

##Other Controls:
  Spacebar : Toggle pause mode or not
