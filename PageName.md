# Introduction #
We are mainly inspired and following [this description](http://ezide.com/games/writing-games.html)
We need a sandbox to test the steering behaviors. To do that we are planning to use a "Game container" as described in the link.

We identify the **classes**:
  * Controllers
  * Viewers
  * Mediators
  * Models

## Controllers ##

These are input devices like Keyboard and Mouse, but also **AI threads**.

## Viewers ##

These are the programs use to visualize (like pygame) and also the loggers (programs to store or log data)

## Model ##
This is the "wolrd" that the controllers make reference of. For example, the Game, as given in the link.

## Mediators ##
This in in general an Event Manager. Takes care of administrating the information (events, packets) flowing from Model to Viewers and Controllers, and from Controllers to Model.
We will not start here...we will eave the Mediators for the end.