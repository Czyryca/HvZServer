"""
Contains the models LongGame, PlayerList, Player and the enum Status
LongGame holds information about 1 weeklong and the settings for that game.
PlayerList is 1-1 with LongGame and handles counting players
Players live in a PlayerList and hold the state of one specific player.
Players are currently not users.
They take no information from user profiles and save no information to user profiles.

Status is one of HUMAN, ZOMBIE, OZHUMAN, OZZOMBIE. It makes counting statuses reliable,
and makes the status of unrevealed OZs print as human.
"""

from datetime import datetime, timedelta
from enum import Enum
from random import choice, sample

from django.db import models


class LongGame(models.Model):
    game_ID = "LG" + str("PLACEHOLDER")  # TODO Increment hex of most recent game
    # Get start and end times.
    # Start day is a Monday at least 14 days in the future, ensuring a week of preregisters and a week of pregames.
    # Start time set to midnight.
    start_date = datetime.now()
    day_of_week = start_date.isoweekday()  # Monday == 1, Sunday == 7
    start_date += timedelta(days=21 - day_of_week)  # += 14 through 20
    start_date = start_date.replace(hour=0, minute=0, second=0, microsecond=0)  # midnight

    # end date is Friday at 11:59:59
    end_date = start_date + timedelta(days=5, seconds=-1)

    # TODO unused right now
    oz_reveal_by_time = True
    oz_reveal_date = start_date + timedelta(days=2, seconds=-1)
    oz_reveal_by_kills = True
    oz_reveal_kills = 2

    # Returns a String summary of the form:
    # "LG00002f: Sep 31 - Oct 4
    def __str__(self):
        start = self.start_date.strftime("%B")[:3] + ' ' + str(self.start_date.day)
        end = self.end_date.strftime("%B")[:3] + ' ' + str(self.end_date.day)
        return self.game_ID + ": " + start + " - " + end


# Possible states of players during a long game
class Status(Enum):
    HUMAN = 0
    ZOMBIE = 1
    OZHUMAN = 2
    OZZOMBIE = 3

    def __str__(self):
        return ["Human", "Zombie", "Human*", "OZ"][self.value]  # TODO remove * when done testing


# Each game has 1 Player List containing the the humans and zombies playing.
class PlayerList(models.Model):
    game = models.OneToOneField(LongGame, on_delete=models.CASCADE, primary_key=True)


# Player class that describes a specific player's status and information in 1 game.
# Not to be confused with a user, and right now not linked to a user TODO
# Values here are likely placeholders or defaults
class Player(models.Model):
    player_list = models.ForeignKey(PlayerList, on_delete=models.CASCADE)
    name = choice(["Ana", "Bob", "Carol", "Dan", "Eve"])
    status = Status.HUMAN
    kills = 0

    # Generate a 7 char killcode of the form MKXXXXX
    killChars = "23456789QWERTYUPASDFGHJKZXCVBNM"
    while True:
        killcode = "MK"
        killcode += sample(killChars, 5)
        # If killcode is unique for this player_list, stop
        # Note: won't check for uniqueness against the player being generated because it isn't saved yet?
        # Needs to be tested.
        if killcode not in [player.killcode for player in player_list.objects.all()]:
            break

    OZ_opt_in = False  # TODO get value from last game? from user profile?
    bandanna_number = -1  # TODO


# Counts the statuses of each player
# Takes a PlayerList an input
# Outputs an integer number of humans, zombies, ozs as a 3-tuple
# Revealed OZs are counted as zombie
# Unrevealed OZs are counted as OZs AND humans AND zombies
def headcount(player_list):
    human, zombie, oz = 0, 0, 0
    for player in player_list.objects.all():
        if player.status == Status.HUMAN:
            human += 1
        if player.status == Status.ZOMBIE or player.status == Status.OZZOMBIE:
            zombie += 1
        if player.status == Status.OZHUMAN:
            oz += 1

    return human, zombie, oz


# Returns a string game summary of the form
# There are X humans and Y zombies, counting the Z OZs as both human and zombie.
def game_state(player_list):
    humans, zombies, ozs = headcount(player_list)
    state = "There are " + humans + ozs + "humans and " + zombies + " zombies"
    if ozs > 0:
        state += ", counting the " + ozs + " OZ" + 's' if ozs > 1 else '' + " as both human and zombie"
    state += '.'

    return state
