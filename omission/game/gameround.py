"""
Gameplay Round [Omission]
"""

from enum import Enum

from omission.game.contentloader import ContentLoader
from omission.game.item import ContentItem
from omission.game.timer import GameTimer

class GameRound(object):
    """
    A single round of gameplay. Generates the content for the round and
    manages the score and gameplay dynamics.
    """
    # Ensure we don't use any passage more than once per round.

    # pylint: disable=R0902
    def __init__(self, life_signal, gameover_callback=None, tick_callback=None,
                 loader=None, settings=None):
        """
        Create a new gameplay round.
        """
        # pylint: disable=R0913

        # Store the game over callback.
        self._over_callback = gameover_callback
        self._tick_callback = tick_callback

        # Store the ContentLoader, generating a new one if necessary.
        if loader:
            self._loader = loader
        else:
            self._loader = ContentLoader()

        # Stores the setting or uses the defaults.
        if settings:
            self.settings = settings
        else:
            self.settings = GameRoundSettings()

        # If we're playing Timed mode...
        if self.settings.mode == GameMode.Timed:
            # Create the timer.
            self._timer = GameTimer(life_signal, self.settings.limit, self.game_over, self.tick)
        # Otherwise, for all other modes...
        else:
            # Create an infinite timer.
            self._timer = GameTimer(life_signal, 0, None, self.tick)

        # If we're playing Survival mode...
        if self.settings.mode == GameMode.Survival:
            # Create the life counter.
            self._lives = self.settings.limit

        # Whether we're paused.
        self._paused = False
        # The current puzzle item.
        self._item = None
        # The current attempt
        self._try = 0
        # The current score.
        self._score = 0
        # The last item score.
        self._item_score = 0

    def start_round(self):
        """
        Start the round.
        """
        # Load the first item.
        self.new_item()
        # Start the game timer.
        self._timer.start()

    def new_item(self):
        """
        Creates a new content item.
        """
        # Get the new item.
        self._item = None
        self._item = ContentItem(self._loader.get_next())
        # Reset tries.
        self._try = 0
        # Set a new bookmark on our timer (start of question).
        self._timer.bookmark()

    def get_status(self):
        """
        Returns the status of the game as (mode, percentage, seconds, lives).
        """
        remaining = 100
        lives = 0
        if self.settings.mode == GameMode.Survival:
            lives = self._lives
            remaining = (lives / self.settings.limit) * 100
        elif self.settings.mode == GameMode.Timed:
            remaining = self._timer.get_remaining_percent()
        else:
            lives = 0
        return (self.settings.mode, remaining,
                self._timer.get_seconds(), lives)

    def get_puzzle(self):
        """
        Returns the text of the current puzzle as a tuple (puzzle, removals),
        showing hints based on game settings and current tries.
        """
        # If the underscores are scheduled to appear on this or a prior try,
        # or if they're always shown...
        if self._try >= self.settings.clue_at or self.settings.clue_at == 0:
            # Get the puzzle text WITH the underscores.
            text = self._item.get_puzzle(True)
        # Otherwise...
        else:
            # Get the puzzle text WITHOUT the underscores.
            text = self._item.get_puzzle(False)

        # If the count is scheduled to appear on this or a prior try,
        # of it it's always shown...
        if self._try >= self.settings.count_at or self.settings.count_at == 0:
            count = self._item.get_removals()
        else:
            count = 0

        # Return the puzzle data.
        return (text, count)

    def get_tries(self):
        """
        Return the number of remaining tries.
        """
        return self.settings.tries - self._try

    def answer(self, letter, progress=False):
        """
        Pass answer in. Returns a GameStatus.
        If progress is True, it will automatically fetch the next item.
        """
        if self._item:
            # If the answer is correct.
            if self._item.check_answer(letter):
                # Calculate score.
                self.calculate_item_score()

                # If we're on Timed mode...
                if self.settings.mode == GameMode.Timed:
                    # Add five seconds to the time.
                    # Be sure to do this AFTER calculating score!
                    self._timer.add_time(self.settings.bonus)

                if progress:
                    # Get the next item.
                    self.new_item()

                # Indicate the answer was correct.
                return GameStatus.Correct
            else:
                # Give penalty.
                self._timer.remove_time(self.settings.penalty)
                # Mark the attempt.
                self._try += 1
                # If we've used all our tries...
                if self._try >= self.settings.tries:
                    # No attempts on this puzzle left.

                    # If we're on Survival mode...
                    if self.settings.mode == GameMode.Survival:
                        # Remove a life.
                        self._lives -= 1
                        # If we're out of lives...
                        if self._lives <= 0:
                            # End the game.
                            self.game_over()

                        if progress:
                            # Get the next item.
                            self.new_item()

                    # Indicate the answer was incorrect AND skipped.
                    return GameStatus.Skipped

                # Else, if we've still got tries left.
                else:
                    # Indicate the answer was incorrect.
                    return GameStatus.Incorrect

    def calculate_item_score(self):
        """
        Calculate the item score and add it to the main score.
        """
        # Get the number of letters that were removed.
        letters = self._item.get_removals()
        # If more than 10 letters were removed, just the score for "10".
        if letters > 10:
            letters = 10
        # Calculate the base score based on letters removed.
        # 1 letter = 100 points, 5 letters = 60 points, 10+ letters = 10 points
        base_score = 100-((letters-1)*10)
        # The attempt bonus.
        # +1x for each remaining try.
        try_bonus = self.settings.tries-self._try
        # The time bonus.
        # 5s = +1x, 4s = +2x...1s = +5x
        time = self._timer.since_bookmark()
        if time > 6:
            time = 6
        time_bonus = 6 - time
        self._item_score = base_score * (try_bonus + time_bonus)
        self._score += self._item_score

    def get_score(self):
        """
        Get score. Returns (score, item_score)
        """
        return (self._score, self._item_score)

    def get_solution(self):
        """
        Get the puzzle solution as (letter, puzzle).
        """
        return (self._item.get_answer(), self._item.get_solution())

    def pause(self):
        """
        Pause the game.
        """
        if not self._paused:
            self._paused = True
            self._timer.stop()

    def is_paused(self):
        """
        Returns True if the game is paused, else False.
        """
        return self._paused

    def resume(self):
        """
        Resume the game.
        """
        if self._paused:
            self._paused = False
            self._timer.start()

    def game_over(self):
        """
        End the game.
        """
        # Stop the timer.
        self._timer.stop()
        # If we have a gameover callback, call it now.
        if self._over_callback:
            self._over_callback()

    def tick(self):
        """
        Runs every second.
        """
        # If we have a tick callback, call it now...
        if self._tick_callback:
            self._tick_callback()

class GameStatus(Enum):
    """
    The different responses to an answer.
    """
    Incorrect = 1,
    Skipped = 2,
    Correct = 3

class GameMode(Enum):
    """
    The different gameplay modes.
    """
    Timed = 1,
    Survival = 2,
    Infinite = 3

class GameRoundSettings(object):
    """
    The object containing the settings for a single round.
    """
    #pylint: disable=R0902
    def __init__(self):
        self.mode = GameMode.Timed
        # The timer length in timed mode OR the number of lives.
        self.limit = 30
        # The maximum, number of attempts before discarding a puzzle.
        self.tries = 3
        # The try number to display the clue at (underscores).
        self.clue_at = 2
        # The try number to display the count at.
        self.count_at = 1
        # The time to add to the clock on a correct guess in Timed mode.
        self.bonus = 3
        # The time to remove from the lock on a wrong guess in Timed mode.
        self.penalty = 1
        # Whether to pause on solution.
        self.solution_pause = True

    def set_timed(self, time=30, bonus=2, penalty=1, tries=3):
        """
        Switch to Timed mode.
        """
        self.mode = GameMode.Timed
        self.limit = time
        self.bonus = bonus
        self.penalty = penalty
        self.tries = tries

    def set_survival(self, lives=5, tries=1):
        """
        Switch to Survival mode.
        """
        self.mode = GameMode.Survival
        self.limit = lives
        self.tries = tries

    def set_infinite(self, tries=3):
        """
        Switch to Infinite mode.
        """
        self.mode = GameMode.Infinite
        self.tries = tries

    def set_solution_pause(self, solution_pause=True):
        """
        Set whether to show the solution.
        """
        self.solution_pause = solution_pause

    def set_clues(self, count_at=1, clue_at=3):
        """
        Define the clue timings.
        If count_at or clue_at are > tries, it won't ever be displayed.
        If count_at or clue_at is at 0, it'll always be displayed.
        """
        self.count_at = count_at
        self.clue_at = clue_at

    def get_datastring(self):
        """
        Get the datastring representing the settings.
        """
        output = ""

        # DEF=T:time:bonus:penalty:tries:hint:clue:solution
        if self.mode == GameMode.Timed:
            output += "T:" + \
                str(self.limit) + ":" + \
                str(self.bonus) + ":" + \
                str(self.penalty) + ":" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(int(self.solution_pause))

        # DEF=S:lives:tries:hint:clue:solution
        elif self.mode == GameMode.Survival:
            output += "S:" + \
                str(self.limit) + ":" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(int(self.solution_pause))


        # DEF=I:tries:hint:clue:solution
        elif self.mode == GameMode.Infinite:
            output += "I:" + \
                str(self.tries) + ":" + \
                str(self.count_at) + ":" + \
                str(self.clue_at) + ":" + \
                str(int(self.solution_pause))

        return output
