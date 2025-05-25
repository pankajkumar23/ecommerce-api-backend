from enum import IntEnum

class PaymentStatus(IntEnum):
    pending = 1
    processing = 2
    failed = 3
    