from itertools import cycle
import os

# Load backends from environment variable
backends_list = os.getenv("BACKENDS", "hashi,azure").split(",")
backends = cycle(backends_list)

def assign_backend():
    """Assign a backend dynamically using round-robin logic."""
    return next(backends)
