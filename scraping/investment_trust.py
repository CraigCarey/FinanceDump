from dataclasses import dataclass

@dataclass
class InvestmentTrust:
    symbol: str
    name: str
    link: str
    tradeable: bool
    premium: float
