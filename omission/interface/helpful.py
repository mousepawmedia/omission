"""
Helpful Functions [Omission]
"""

def sec_to_timestring(seconds):
    """
    Converts seconds to time string (MM:SS).
    """
    # Prevent numbers less than zero.
    if seconds < 0:
        seconds = 0
    minutes = int(seconds/60)
    seconds -= (minutes*60)
    return str(minutes).zfill(2) + ":" + str(seconds).zfill(2)

def score_to_scorestring(score):
    """
    Converts score to the score string.
    """
    fill_depth = 10
    return str(score).zfill(fill_depth)
