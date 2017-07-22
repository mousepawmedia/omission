"""
Game Timer [Omission]
"""

from threading import Timer

class GameTimer(object):
    """
    The timer object for a game round.
    """

    def __init__(self, life_signal, length, over_callback=None, tick_callback=None):
        """
        Create a new GameTimer. length is the number of seconds. If 0,
        the GameTimer will be infinite until stopped.
        """
        # The length of the timer.
        self._length = length
        # The function to call when the timer is done.
        self.over_callback = over_callback
        # The function to call on each tick.
        self.tick_callback = tick_callback
        # Define a one-second timer.
        self._timer = Timer(1.0, self._timer_step)
        # The number of seconds that have elapsed.
        self._elapsed = 0
        # The last bookmark. Used for tracking time between answers.
        self._bookmark = 0
        # Death signal
        self._alive = True

        # Register my death function with the given lifespan signal.
        life_signal(self.die)

    def _timer_step(self):
        """
        Fires every second, updating the timer object.
        """
        self._elapsed += 1
        if self._length > 0 and self._elapsed >= self._length:
            self._timer_done()
        else:
            # If there's still time left...
            # If we have a tick callback...
            if self.tick_callback:
                # Call it now.
                self.tick_callback()
            # Elapse another second.
            self._timer = None
            self.start()

    def _timer_done(self):
        """
        The timer is finished.
        """
        print("End!")
        # If a callback was defined...
        if self.over_callback:
            # Call it now.
            self.over_callback()

    def get_remaining_percent(self):
        """
        Returns the number of seconds in the timer as a percentage.
        """
        # If the length is non-zero.
        if self._length > 0:
            return 100 - int(self._elapsed / self._length * 100)
        # Otherwise, if this is an infinite timer...
        else:
            # Always return 100%
            return 100

    def get_seconds(self):
        """
        Returns the remaning number of seconds remaining in a finite timer
        OR the number of seconds elapsed in an infinite timer.
        """
        # If the length is non-zero.
        if self._length > 0:
            # Return remaining seconds.
            return self._length - self._elapsed
        # Otherwise, if this is an infinite timer...
        else:
            # Return the time elapsed
            return self._elapsed


    def add_time(self, seconds):
        """
        Add the given number of seconds to remaining time.
        """
        # Remove the time from the elapsed variable.
        self._elapsed -= seconds
        # If we're less than zero, reset elapsed to zero.
        if self._elapsed <= 0:
            self._elapsed = 0

    def remove_time(self, seconds):
        """
        Remove the given number of seconds from remaining time.
        """
        # Add the time from the elapsed variable.
        self._elapsed += seconds
        # If we're greater than the max, reset elapsed to max.
        if self._length > 0 and self._elapsed >= self._length:
            self._elapsed = self._length

    def bookmark(self):
        """
        Set the bookmark to the current time.
        """
        self._bookmark = self._elapsed

    def since_bookmark(self):
        """
        Return the number of seconds elapsed since the last bookmark.
        """
        return self._elapsed - self._bookmark

    def reset(self):
        """
        Reset the timer.
        """
        self._elapsed = 0

    def stop(self):
        """
        Stop the timer without resetting anything.
        """
        if self._timer:
            self._timer.cancel()
        self._timer = None

    def start(self):
        """
        Start/resume the timer.
        """
        if not self._timer:
            self._timer = Timer(1.0, self._timer_step)
        if self._alive:
            self._timer.start()

    def die(self):
        """
        Order the timer to die.
        """
        self._alive = False
