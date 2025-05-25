from enum import IntEnum

class OrderStatus(IntEnum):
    pending = 1
    processing = 2
    confirm = 3
    shipped =4
    delivered =5
    cancelled = 6
    