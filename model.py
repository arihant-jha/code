from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


@dataclass(frozen=True)  # frozen=True makes it immutable
class OrderLine:
    orderid: str
    sku: str
    qty: int


class Batch:
    def __init__(self, ref: str, sku: str, qty: int, eta: Optional[date]):
        self.reference = ref
        self.sku = sku
        self.eta = eta
        self._purchased_qty = qty
        self._allocations = set()
    
    @property
    def allocated_qty(self) -> int:
        return sum(line.qty for line in self._allocations)
    
    @property
    def available_qty(self) -> int:
        return self._purchased_qty - self.allocated_qty


    def can_allocate(self, line: OrderLine):
        return self.sku == line.sku and self.available_qty >= line.qty
    
    def allocate(self, line: OrderLine):
        if self.can_allocate(line):
            self._allocations.add(line)
    
    def deallocate(self, line: OrderLine):
        if line in self._allocations:
            self._allocations.remove(line)

def allocate(line: OrderLine, batches: List[Batch]) -> None:
    # allocate to the batch with smallest eta
    if len(batches) == 0:
        raise Exception("No Batches available for allocation")
    best_batch = None
    for i, batch in enumerate(batches):
        if best_batch is None and batch.available_qty > line.qty:
            best_batch = batch
        if batch.eta < best_batch.eta and batch.available_qty > line.qty:
            best_batch = batch
    if best_batch is None:
        raise Exception("No Batches available with requested quantity")
    best_batch.allocate(line)
    return