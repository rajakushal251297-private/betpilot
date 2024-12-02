

import time

def remaining_time():
    """Returns the remaining time until the next 2-minute cycle."""
    current_time = time.time()
    next_cycle = (int(current_time // 120) + 1) * 120
    return next_cycle - current_time
