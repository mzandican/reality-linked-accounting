from dataclasses import dataclass

@dataclass
class AccountNode:
    id: str

@dataclass
class ObservationNode:
    value: float
    trust: float
