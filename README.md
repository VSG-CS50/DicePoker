# DicePoker
#### Video Demo:  <[URL HERE](https://youtu.be/p_gfQXIV2BY)>
#### Description: A poker-like game played with dice

## The Game
DicePoker is a full-stack web application game that simulates a strategic dice based game of Poker. Developed with Flask, Python, HTML, CSS and SQLite, the game blends elements of chance and logic. The objective of the game is to make the best possible hand by rolling five dice that beats the AI's dice hand.

## Gameplay
Each round begins with the player and the AI rolling 5 dice randomly. The hand is then evaluated by the app to label and rank the hand based on poker logic as shown below:

Hand rank highest to lowest:
- Five of a Kind      (3,3,3,3,3)
- Four of a Kind      (3,3,3,3,5)
- Full House          (3,3,4,4,4)
- Straight            (1,2,3,4,5)
- Three of a Kind     (3,3,3,4,6)
- Two Pair            (3,3,4,5,5)
- One Pair            (3,3,4,5,6)
- High Die            (1,2,4,5,6)

Five of a Kind is the best hand possible, while High Die is the worst hand possible.

The dice can then be rerolled ONCE. This choice introduces a strategic layer. The AI has its own strategy to create winning dice hands. None, some, or all of the dice can be rerolled to create better dice hands.

Finally, after rerolling, the dice hands are evaluated again. The player's hand with higher rank wins the game. If the hands of the AI and player are the same, such as a Full House, then the game is a tie. The player can replay the level when tied, offering a chance to progress to the next level. Due to the probabilistic nature of the game, there is no ceiling on the level. In reality, the game ends around level 5 for most players, with a few going as high as 10.

## Design Rationale
Tie Game:
I considered calculating dice value for tie games. For instance (3,3,4,5,6) is a better Two Pair than (1,1,4,5,6) because the pair 3,3 has a higher dice value than the pair 1,1. However, I noticed this could potentially end the run early for players. Hence, I decided to offer a chance to replay the level when tied.

Level progression:
Instead of levels, early on I had thought about making a pool and allow the player to bet. But I didn't implement this as it had a ceiling on levels. I wanted to build a rogue-like game that could be replayed again.

AI Strategy:
I originally intended to force the AI to roll Four of a Kind and Five of a Kind  at levels of multiples of 5 and 10 respectively to ensure the game is challenging and not repetitive. But in reality, when I completed the game and started testing, I realized that the game naturally limited the levels due to the probabilistic nature of the game.

Best of 3 vs Best of 1:
I considered making each level a best of 3 to progress the level rather than its current implementation of just 1 round to progress to next level. I decided against it as it was a little confusing for new players to track rounds and levels separately and made the game time longer.

## Level Progression and Replayability

The game has a level system that tracks players progress. Each win against the AI increases the game level by 1. Losing to the AI offers to start a new game. The design provides short term goal in the form of winning the round and long term goal as attaining the highest possible level. It's akin to a rogue-like poker game using dice.

## Leaderboard

The progress of the player is stored in an SQL database. The game captures the name of the player when starting a game. If the name is skipped, the default name "Anonymous" is used to store the progress.

The leaderboard is saved and updated similar to an arcade game. The top 10 players based on the highest level attained is shown in the leaderboard page, allowing users to compare their performance with others. The SQL leaderboard is updated  whenever a player's run ends and the level is greater than 1 (this is to avoid leaderboard data to be filled with just 1 level wins)

## Files and Their Content
app.py:

It contains the backend of the game i.e. the Flask configuration, routes, methods, etc. Flask sessions are used to manage persistent data. Methods in this file:

- rolldice(n): returns a list of n dice of values between 1 and 6. n = 5 is used in game.

- evalhand(dice): Calculates the hand name and rank, for example: Four of a kind label and rank 7.

- aiplay(dice): AI strategy for rerolling the dice. It keeps hand if its straight or above. Rerolls dice that are not in pairs, threes, fours, fives.

- highlightdice(dice): Create a boolean list that indicates with a white halo around dice that are part of a pair, threes, straights, etc. I added this when I realized the hands were not immediately recognized.

- game(level): Manages level system and offers restart, replay, and next level.

templates/
- layout.html: Base template that defines title, main, etc to be used by other templates.

- index.html: The game UI is here. Shows the AI's and player's dice hand, allows reroll, replay level, next level and restart game. Jinja is used for conditional operation to update the UI dynamically.

- howtoplay.html: Instructions on how to play the game and ranking of dice hands.

- leaderboard.html: Shows the top 10 players.

static/
- styles.css: Manages the appearance of pages, tables, highlighting dice, etc.

- static/(AI)DieX.png: Images for dice representing faces 1 to 6.

leaderboard.db:

SQL database to store persistent data on player's best run.
