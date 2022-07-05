# A Console Pacman game in Python

![pacman_gameplay_small](https://user-images.githubusercontent.com/5196925/45268661-70322600-b49d-11e8-94d9-aca9332fa2e4.gif)

For this exercise, we will practice the object-oriented programming principles we learned in the course using a famous video game from Japan, Pacman. The game itself is implemented except for two places. Follow the steps below to implement the remaining functionality, then try running the game!


## Objects

An object is simply a collection of data (variables) and methods (functions) that act on those data. Similarly, a class is a blueprint for that object. We can think of a class as a sketch (prototype) of a house. It contains all the details about the floors, doors, windows, etc.

From this blueprint, we can create reusable instances of an object and have clear expectations for the attributes of said object.


### Part 1: Class Attributes

**In our Pacman game**, both pacman and ghosts are "characters", however, they are represented by different colors and characters.

1. In `character.py` please prepare the **Character** class so that it can recieve a `color` attribute when instanced.
2. In `character.py`, for **Ghosts** please set override the default value of false for the `pass_over` attribute to `True`


### Part 2: Instancing Objects from Classes

In `pacman.py` we have imported our Pacman and Ghost instances. We've created the instances to- but we still need to set the colors.

**Be aware** that it is a positional parameter- so the order should match the order on the class with color being the second parameter.

1. Set Pacman's color to yellow, you can use the constant `COLOR.yellow`.
2. Set Blinky's color to red, you can use the constant `COLOR.red`.
3. Set Pinky's color to pink, you can use the constant `COLOR.pink`.
4. Set Inky's color to cyan, you can use the constant `COLOR.cyan`.
5. Set Clyde's color to orange, you can use the constant `COLOR.orange`.

### Part 3: Adding a Class Method

In `character.py`, let's implement the `die` method for `Pacman` so when he hits a ghost, his animation plays and we trigger a respawn.

1. Loop through the array `['O', 'o', '.', "'", '*', ' ']` to perform the character changes that act as our animations.
2. Pause on every iteration of the loop for `0.2` seconds using `time.sleep()`
3. Use the `self.draw_char()` method to draw the character in the animation sequence, the second parameter is `False`.
4. Finally, refresh the game_box/main screen with `self.game_box.map_box.refresh()`.


### Trying it out

When you have finished, try playing it! `cd` into project directory and run:

```
python3 pacman.py
```

Credits for PACMAN project: https://github.com/pratu16x7/pacman-console
