from dataclasses import dataclass
from typing import List


@dataclass
class NetworkConditions:
    delay: int  # in ms
    delay_delta: int  # in msd
    distribution_type: str
    loss: float  # in %
    bandwidth: int  # in mbit
    ports: List[int]
