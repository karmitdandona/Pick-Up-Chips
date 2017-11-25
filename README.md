# Pick-Up-Chips
A small project to learn Amazon Alexa development.

### Game
* The objective is to *not* be the one to pick up the last chip on the table
* The number of chips a player has at the end of the game is irrelevant


* There are two difficulty modes: Easy and Hard
* The game starts with a random number of chips on a table
* Turns alternate between Alexa and the user, with Alexa going first
* During the turn, the player must pick up either 1, 2, or 3 chips from the table


* After the game is over, the user is given the option to play again
* If the user won, he/she is prompted to play again on Hard mode

#### To Do:
* get_welcome_response should only run first time the skill is launched (veteran users should not have to hear the full message every time)... Right now, is it setup so that saying difficulty as part of utterance skips the instructions??
* Give the user the option of playing again once the game is over, instead of just suggesting it and ending the skill.
