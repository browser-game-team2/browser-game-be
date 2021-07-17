# Browser Game

## Project Structure
The project is built in Django.\
Three different Django apps were created 
to handle different features: *authentication*, *army*, *battle*.\
Database SQLite3 was used for local development, converted to
PostgreSQL in production (Heroku deploy).\
OOP and unit testing were used throughout the project.\
The back-end is deployed at https://browsergameteam2.herokuapp.com/

### authentication
oAuth is used, through Django *all-auth* package.\
The `UserAuth` class inside the *authentication_package* is used to
get authentication data from the database, for example the social token.\
Currently the user can login via Google.

### army
At the moment the *army_package* includes an `Army` class, which generates random
armies, and one class for each type of troup: `SpaceShip`, `SpaceCruiser`
and `SpaceDestroyer`. An instance of each class will return the
pricing of that specific troup.

### battle
This is the core feature for handling the battle phase of the game.\
The back-end will receive a JSON from the front-end, including the user army
as well as the cpu army. A battle will be then triggered, handled by the 
`Battle` class of the *battle_package*. The algorithm will generate the result
of the battle, with information about the winner, the remaining army of the winner and
a detailed report of what happened during the battle.

##### Battle Rules

The `battle()` function simulates a battle between two space fleets.

It takes in two parameters: \
`at` >>> attacking fleet composition (dictionary)\
`de` >>> defending fleet composition (dictionary)

Here is an example of the form of these dictionaries:\
`{'S': 3, 'C': 5, 'D': 7, 'F': 1}`\
where S, C and D represent different vessel types along with the amount of ships of each type,
while F represents one of three possible formations (i.e. strategies) and is therefore assigned a value of
1, 2 or 3 (more about that below)

It returns three values: \
a BOOLEAN, evaluating `True` if the attacker is victorious, `False` if it is defeated\
a DICTIONARY representing the composition of the winning fleet, organized the same way as the input parameters
(the other fleet is wiped out completely)\
a DICTIONARY representing a report of players' losses turn by turn. 
Ex.: {1: {'a': 2, 'd': 3}, 2: {'a': 6, 'd': 1}, ...}

The phases of the battle are as follows.

First, according to the battle formation chosen by each side, the `deploy()` function assigns *"focus"*
to a ship type and an *"advantage"* to either attacker, defender or none of them.\
For example, if the attacker chose formation 1 and the defender chose formation 3,
the function returns the tuple `('S', 'a')`.
This means spaceships (S) will be the focus of the battle and that the attacker (a) will enjoy a slight advantage.

The `deploy()` function affects a **special round** at the beginning of the battle.
During this round, only "focus" ships of the "advantaged" side can attack;
if no side is advantaged, all the "focus" ships of both sides will attack.\
In the example above, only the spaceships (S) of the attacker (a) will attempt to cause damage at the opposing fleet
(the details of how an attack is resolved will be made explicit in the next paragraph).\
This special round will be recorded in the battle report dictionary
(the third return value of the `battle()` function) with the key `"0"`.\
The formation value (F) of each fleet will have no further use throughout the battle.

Regular battle rounds are then carried on one after another, while one of the two fleets is destroyed.
A battle round works as follows:\
1 - Each fleet rolls 2 six-sided dice for each of its vessels. All the rolls happen at once\
2 - Each dice roll may or may not result in a *hit*, depending on the result and on the type of ship that rolled.
Spaceships (S) get a hit with a result of 5+, cruisers (C) with a result of 7+, destroyers (D) with a result of 9+
(see `rollToHit()` function)\
3 - Each hit inflicts a casualty on the opposing fleet (see `removeCasualties()` function)\
4 - Casualties are removed at the same time from both fleets. Weaker ships are removed first
(D gets hit before C which gets hit before S)\
5 - Casualties suffered from both sides are recorded in the battle record dictionary\
6 - If one of the two fleets is completely destroyed, the battle ends and the function returns.\
This sequence is repeated as long as there are ships on both sides.

It is possible, although very unlikely, that the defender may win with an empty fleet,
in case both contenders wiped each other out in the same round.

## REST APIs
Two main endpoints are used: */choose/* and */battle/*.\
After a successful login with oAuth, the /choose/ API will return
authentication data of that user, together with: the overall budget, 
the pricing of the available troups, the available planets,
the possible strategies to adopt during the battle.\
The /battle/ API will return the result of the battle. It requires
information to be passed in order to return the result. Those information
are the army of both the attacker and the defender.\
Both APIs require the user to be logged in in order to work.
If the user is not logged in, the API will redirect to the
*/not_authenticated/* endpoint.

## Tests
Unit tests were used. Each Test Case is written in its own
Django app.\
For example, tests for the battle algorithm were added inside
*battle/tests.py*.\
All tests can be launched with the single command: `python manage.py test`.
 