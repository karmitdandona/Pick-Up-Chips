# Pick-Up-Chips
[A small project to learn Amazon Alexa development.](https://www.amazon.com/Karmit-Dandona-Pick-Up-Chips/dp/B077RCVNWH "See this Skill on the Alexa Store")

### Game
* The objective is to *not* be the one to pick up the last chip on the table
* The number of chips a player has at the end of the game is irrelevant


* There are three difficulty modes: Easy, Medium, and Hard
* The game starts with a random number of chips on a table
* Turns alternate between Alexa and the user, with Alexa going first
* During the turn, the player must pick up either 1, 2, or 3 chips from the table


* After the game is over, the user is suggested to try again
* If the user won, the suggestion is to try again on Hard mode

#### Future Possibilities to Further this Project:
* Give the user the option of playing again once the game is over, instead of just suggesting it and ending the skill.
* [x] ~~When there's only 1 chip on the table, it should not say chip*s* in the plural form.~~
* Use SSML instead of text so the speech outputs are more natural (low priority).
* [x] ~~If user says a number (returns True for issnumber()) but the number is not a positive integer, prompt them accordingly (instead of reverting to the difficulty menu, as it currently does.)~~
* Add more print statements in pickUpChips.py so the logs in AWS CloudWatch Management Console provide me more information on Game State. (medium priority)
