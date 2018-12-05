"""
classproperty

Decorator to create a class-wide property.
Sourced from StackOverflow: https://stackoverflow.com/a/5192374/472647

Licensed under Creative Commons Share-Alike 4.0 (International)
https://creativecommons.org/licenses/by-sa/4.0/

Author(s): James Lingard (jchl)
"""

class classproperty(object):

    def __init__(self, f):
        self.f = f

    def __get__(self, obj, owner):
        return self.f(owner)
