"""Module to demonstrate various functions and classes for testing static checkers."""

import random

def fn(x, y):
    """A function which performs a sum."""
    return x + y

def find_optimal_route_to_my_office_from_home(start_time, expected_time,
                                              favorite_route='SBS1K',
                                              favorite_option='bus'):
    """Determine the optimal route to the office based on time."""
    d = (expected_time - start_time).total_seconds() / 60.0

    if d <= 30:
        return 'car'
    if 30 < d < 45:
        return ('car', 'metro')
    if d > 45:
        if d < 60:
            return ('bus:335E', 'bus:connector')
        if d > 80:
            return random.choice(('bus:330', 'bus:331', ':'.join((favorite_option, favorite_route))))
        if d > 90:
            return ':'.join((favorite_option, favorite_route))
    return None

class C:
    """A class which does almost nothing."""

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def f(self):
        """Placeholder function."""
        pass

    def g(self, x, y):
        """Perform a conditional sum."""
        if self.x > x:
            return self.x + self.y
        if x > self.x:
            return x + self.y
        return None

class D(C):
    """D class."""

    def __init__(self, x):
        super().__init__(x, 0)

    def f(self, x, y):
        """Perform a conditional subtraction or addition."""
        if x > y:
            return x - y
        return x + y

    def g(self, y):
        """Perform a conditional sum or subtraction."""
        if self.x > y:
            return self.x + y
        return y - self.x