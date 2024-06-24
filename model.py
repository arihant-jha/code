from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional


@dataclass(frozen=True)#frozen=True makes it immutable
class OrderLine:
    orderid: str
    sku: str
    qty: int

class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self.available_qty = qty
        
    def allocate(self, line: OrderLine):
        self.available_qty -= line.qty
    
    def can_allocate(self, line: OrderLine):
        return (
            self.available_qty > line.qty
        )