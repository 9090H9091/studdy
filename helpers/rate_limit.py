from collections import defaultdict
import time
from helpers.logger import get_logger

logger = get_logger(__name__)

    # Limits users from spamming the bot, Will impliment ban/mute feature later
    
class RateLimiter:
    def __init__(self, cooldown=3):  # 3 seconds default cooldown
        self.cooldown = cooldown
        self.last_used = defaultdict(float)

    def can_process(self, user_id: int) -> bool:
        current_time = time.time()
        if current_time - self.last_used[user_id] < self.cooldown:
            return False
        
        self.last_used[user_id] = current_time
        return True
