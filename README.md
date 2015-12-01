#AI Directions

Use arrow keys to move.

Command Line Options:
-train (will record all the data)
-pause (Pauses in between frames. Only works in train mode)
-replay (Watch Replay loaded game. Must Use with -dataSrc)
-loadData (Loads a game into )
-dataSrc:(x) (data file to be loaded and used, will start at the end of that data file
          if replay isnt enabled than performs like -loadData by defualt)
-sqaures:(x) (How many squares the snake starts with)
-saveas:(x) (Name of the saved file from -train)

REMEMBER WHEN CREATING TRAINING DATA WE NEED TO SET THE BEST POSSIBLE EXAMPLE FOR THE 
AI. IT IS LIKE A CHILD, AND WE HAVE TO BE THE BEST ROLE MODELS WE CAN BE. WITH THAT IN MIND,
IF YOU THINK A PREVIOUS PLAYTHROUGH COULD HAVE BEEN DONE BETTER, JUST DELETE IT FROM THE
FOLDER. NO SLOPPY PLAYTHROUGHS. :)

##Quick How tos:
####Save Data For Training:
    python snake.py -train -pause

    ***The file only saves up until the last apple is gotten *** 
    This means that the file will not save the information of where the snake collides into
    a wall or itself.

####Loading Past Plays:
    python snake.py -train -pause -dataSrc:(filename)

    *** If Human Train mode is on... then this will save the snakeframe queue to a DIFFERENT file, 
    but containing ONLY the data from the current play.

####Interpret Save File Data
    Each line of the file is one frame of the playthrough. The format looks like:
    (Snake X position) (snake Y position) (Apple Position) (Snake Length) (Snake Position)

####Play Game Normally:
    python snake.py

####Change Snake Starting Length:
    python snake.py -startsquares:(Length Desired)

##About Human Train Mode:
  How to activate Human Train Mode? Set humanTrain = true

  Human Train Mode will record the snake and the apples position, the direction
  of the snake and the the length of the snake for each frame. This will be placed
  in an object called SnakeFrame. There is a list of SnakeFrames that is saved to a file
  when the snake dies.
 
  *** The file only saves up until the last apple is gotten *** 
  This means that the file will not save the information of where the snake collides into
  a wall or itself.

  File Format:
  Each line of the file is one frame of the playthrough. The format looks like:
  > (Snake X position) (snake Y position) (Apple Position) (Snake Length) (Snake Position)

##Other Controls:
  Spacebar : Toggle pause mode or not
