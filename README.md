# Part 2 — Data Structures

**Theme:** Restaurant Menu & Order Management System | **Marks:** 25

## How to Run

```bash
python3 part2_order_system.py
```

No external dependencies — uses only `copy` from the standard library.

## Tasks Implemented

| Task | Description | Marks |
|------|-------------|-------|
| 1 | Explore the Menu — grouped by category, total/available count, most expensive, affordable items | 5 |
| 2 | Cart Operations — add/remove/update with duplicate-detection, unavailability check, final bill | 8 |
| 3 | Inventory Tracker — `copy.deepcopy()`, order fulfilment deduction, reorder alerts | 6 |
| 4 | Sales Log Analysis — revenue per day, best-selling day, most ordered item, `enumerate` | 6 |

## Key Concepts Demonstrated

- **Deep Copy:** `copy.deepcopy(inventory)` ensures `inventory_backup` is completely independent.  
  The demo explicitly mutates `inventory` then shows `inventory_backup` is unchanged.
- **Dictionary methods:** `.items()`, `.values()`, `.get()`, `.update()`
- **List of dicts:** Cart represented as `[{"item": ..., "quantity": ..., "price": ...}]`
