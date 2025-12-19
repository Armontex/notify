from enum import Enum

class RepeatStatus(Enum):
    """
    Статус откладывания уведомлений
    
    Notification repeat status
    """
    OFF = 0
    HOURLY = 1
    DAILY = 2
    WEEKLY = 3
    MONTHLY = 4
    ANNUALLY = 5