from collections import defaultdict
import time
from helpers.logger import get_logger

logger = get_logger(__name__)

class RateLimiter:
    def __init__(self, cooldown=5):  # 5 seconds default cooldown
        self.cooldown = cooldown
        self.last_used = defaultdict(float)

    def can_process(self, user_id: int) -> bool:
        current_time = time.time()
        if current_time - self.last_used[user_id] < self.cooldown:
            return False
        
        self.last_used[user_id] = current_time
        return True
