from dataclasses import dataclass


@dataclass
class NetworkConditions:
    delay: int  # in ms
    delay_delta: int  # in msd
    distribution_type: str
    loss: float  # in %
    bandwidth: int  # in mbit
