"""
Helpful Functions [Omission]
"""

def sec_to_timestring(seconds):
    """
    Converts seconds to time string (MM:SS).
    """
    minutes = int(seconds/60)
    seconds -= (minutes*60)
    return str(minutes) + ":" + str(seconds).zfill(2)

def score_to_scorestring(score):
    """
    Converts score to the score string.
    """
    fill_depth = 8
    return str(score).zfill(fill_depth)
