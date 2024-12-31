import time
import random


def random_delay(min_seconds: float = 3.0, max_seconds: float = 20.0) -> None:
    """
    在操作之間添加隨機延遲

    Args:
        min_seconds: 最小延遲秒數
        max_seconds: 最大延遲秒數
    """
    delay_time = random.uniform(min_seconds, max_seconds)
    time.sleep(delay_time)
