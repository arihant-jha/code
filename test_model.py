from datetime import date, timedelta
import pytest

from model import Batch, OrderLine

# from model import ...

today = date.today()
tomorrow = today + timedelta(days=1)
later = tomorrow + timedelta(days=10)


def make_batch_and_order_line(
    sku,
    batch_qty,
    line_qty
):
    return (
        Batch("Batch-001", sku, batch_qty, eta=today), 
        OrderLine("Order-1", sku, line_qty)
    )

def test_allocating_to_a_batch_reduces_the_available_quantity():
    batch, line = make_batch_and_order_line("sofa", 30, 20)
    batch.allocate(line)
    assert batch.available_qty == 10
    pytest.fail("todo")


def test_can_allocate_if_available_greater_than_required():
    batch, line = make_batch_and_order_line("sofa", 30, 20)
    assert batch.can_allocate(line) == True
    pytest.fail("todo")


def test_cannot_allocate_if_available_smaller_than_required():
    batch, line = make_batch_and_order_line("sofa", 10, 20)
    assert batch.can_allocate(line) == False
    pytest.fail("todo")


def test_can_allocate_if_available_equal_to_required():
    batch, line = make_batch_and_order_line("sofa", 20, 20)
    assert batch.can_allocate(line) == True
    pytest.fail("todo")


def test_prefers_warehouse_batches_to_shipments():
    warehouse_batch = Batch("batch-w", "sofa", 20, eta=today)
    shipment_batch = Batch("batch-s", "sofa", 20, eta=later)
    line = OrderLine("line-1", "sofa", 8)
    allocate(line, [warehouse_batch, shipment_batch])
    assert warehouse.available_qty == 12 and shipment_batch.available_qty == 20
    pytest.fail("todo")


def test_prefers_earlier_batches():
    early_batch = Batch("batch-w", "sofa", 20, eta=today-timedelta(days=10))
    today_batch = Batch("batch-s", "sofa", 20, eta=today)
    late_batch = Batch("batch-w", "sofa", 20, eta=today+timedelta(days=10))
    line = OrderLine("line-1", "sofa", 8)
    allocate(line, [early_batch, today_batch, late_batch])
    assert early_batch.availabe_qty == 12
    assert today_batch.available_qty == 20
    assert late_batch.available_qty == 20
    pytest.fail("todo")
