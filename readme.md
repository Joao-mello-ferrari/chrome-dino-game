# About
On this file the role of each file of the project will be explained, as well as how it works and some issues/solutions found during development.
In the end, a way to be unbeatable will be shown, so stick to the end.
In case you wanna see how everything works together, here is the link to my youtube video about the project.
It was recorded in portuguese, but it is still possibile to get the feeling of it.
<br>
<a href="https://youtu.be/UwLFO1Di3Bg">Check it out!<a/>


# Role of each file
<ul>
  <li>
    imgs (file folder) -> Stores images used throughout the game
  </li>
  <li>
    commandHelpers.py -> Check every cenario of the game and output what need to be done
  </li>
  <li>
    demoSimulator.py -> Stores the code for de DEMO simulator functionality
  </li>
  <li>
    graphHelper.py -> Build the progress graph it self and handle stored progress data
  </li>
  <li>
    objectHelpers.py -> Create and destroys every single visual instance
  </li>
  <li>
    progress.txt -> Stores progress data
  </li>
  <li>
    errorHelpers -> Display customized error messages
  </li>
  <li>
    main.py -> Main file of the project
  </li>
  <li>
    mainComentada.py -> Same as main, but coomented
  </li>
</ul>

# How the game works
The original Chrome game has some extra functionalities, as well as this version.

The developed game has a DEMO mode, in which the dinossaur performs totally autonomously, so the user can get the allowed commands and how the game works.

The whole application is based on 2 moves: jump and lower, by using the keyboard keys 'space' and 'page down', respectively.

Still, the user can check his progress by requesting a graph, and change the game speed, which directly affects the difficulty.

# Issues
<strong>READING INCORRECT KEYS</strong>:
If a random key if kept down, the 'checkKey()' function does not return every single correspondent key readings. The function executes too fast, so that most of signals read are incorect.
To fix it, a time filter was developed, so that from the moment a key is pressed down, only after x mili seconds a new reading is considered. With that, unwished readings are cut off.

<strong>KEYBOARD BOUNCE</strong>:
As a key is pressed and kept down, a bounce effect is created, so that when the 'page down' key is pressed, there is still a time range during which the current key is considered off. This causes a bug, which leads the dinossaur to toggle its state.
In order to solve it, a time buffer was created, will cancels the key bounce time.

<strong>IDENTIFY COLLISION</strong>:
To check if there is a collision between the dinossaur and a obsctacle is harder than it looks like...
To add this functionality, a maping of strategic points of each image was produced.
Therefore, to check for a collision, every single point of the dinossaur runs into a logic block, which points out if the current dot is whitin a range from a specific obstacle.
If there only one dinossaur point whitin one single obstacle range, a collision is confirmed.

# How to be unbeatable?
Oh, that´s pretty dawn easy!
On the main.py file, on line 51, you will see the following words:
  
<strong>gameOver = checkColision(dino, obstacles, dinoType)</strong>

To become invencible, like a ghost, you just need to replace this whole line for:

<strong>gameOver = False</strong>

In case you think the game is complicated, there is this trick you can use :)
