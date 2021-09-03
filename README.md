# FlappyBird 'AI'
![flappy (1)](https://user-images.githubusercontent.com/35065831/132073448-1a443c31-7f55-4751-9d0d-237cde674f44.gif)

###### The basic game is based on the YouTube tutorial from TechWithTim and the following tutorial:

https://www.youtube.com/watch?v=MMxFDaIOHsE&list=PLzMcBGfZo4-lwGZWXz5Qgta_YNX3_vLS2&ab_channel=TechWithTim

### Improvements:
- Added a main menu to decide between play the game yourself or let the AI play
- Added the classes Game and Swarm to stucture the game and make it more readable

### Super simple AI explained:
- I didn´t use the NEAT algorithm like in the original tutorial, but a much easier method called **linear function approximation** 
- Just using one feature **_x_**: difference between bird height and next pipe bottom position
- The feature is multiplied by a weight **_w_** and a bias **_b_** is added **_y = w x + b_**
- If y is larger than 0, the bird jumps

### How to determine weight and bias?
- Usually, gradient descent is used, but in this case it is challenging to determine the loss, why gradient descent is difficult to use
- Because I just use a single feature, trying several random initialized birds is already quite successful
- The weights of the best bird are randomly changed by a small amount
- After few epochs the bird already masters the game

<img src="https://user-images.githubusercontent.com/35065831/132067195-32992d4c-baa6-4b65-ae1a-650adf6eb541.png" alt="drawing" style="width:400px;"/>

