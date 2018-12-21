# Refactor Checklist

The following needs to be implemented in the factor. Because I am
doing this refactor solo, it is more expedient just to track this
here instead of cluttering up Maniphest. (After 2.0 is done, we
should resume use of Maniphest for issue tracking.)

## Non-GUI Game

NOTE: Be sure to add PyTest tests for everything! We're building
this new version respecting TDD.

* ~~Add GameMode and GameStatus enumerations (from gameround.py)~~

* ~~GameRoundSettings~~

* ~~Settings as a class with static data~~

* ~~Scoreboard as a class with static data~~

* ~~Data Loader should propegate Settings and Scoreboard~~

* ~~GameTimer class~~

* GameTimer tests

* GameItem class

* GameRound class

* Use dictionary for GameRound status, NOT a tuple!

* Font Loader (functions, not class)

* Sound Loader (functions, not class??)

* Image Loader (functions, not class??)

* Content Loader, perhaps as a generator?

