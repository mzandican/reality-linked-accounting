from dataclasses import dataclass

@dataclass
class Edge:
    from_id: str
    to_id: str
    type: str   # CLAIMS, VERIFIED_BY, LINKS_TO
    weight: float
