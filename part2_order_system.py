# part2_order_system.py
# Assignment Part 2 - Data Structures
# Theme : Restaurant Menu & Order Management System
# building the whole thing using only lists, dicts and combinations of both
# no classes, no external libraries - just core python data structures

import copy


# ─────────────────────────────────────────────────────────────────────
# PROVIDED DATA  -  dont modify this, all tasks work on this directly
# ─────────────────────────────────────────────────────────────────────

menu = {
    "Paneer Tikka":  {"category": "Starters",  "price": 180.0, "available": True},
    "Chicken Wings": {"category": "Starters",  "price": 220.0, "available": False},
    "Veg Soup":      {"category": "Starters",  "price": 120.0, "available": True},
    "Butter Chicken":{"category": "Mains",     "price": 320.0, "available": True},
    "Dal Tadka":     {"category": "Mains",     "price": 180.0, "available": True},
    "Veg Biryani":   {"category": "Mains",     "price": 250.0, "available": True},
    "Garlic Naan":   {"category": "Breads",    "price": 40.0,  "available": True},
    "Gulab Jamun":   {"category": "Desserts",  "price": 90.0,  "available": True},
    "Rasgulla":      {"category": "Desserts",  "price": 80.0,  "available": True},
    "Ice Cream":     {"category": "Desserts",  "price": 110.0, "available": False},
}

inventory = {
    "Paneer Tikka":  {"stock": 10, "reorder_level": 3},
    "Chicken Wings": {"stock": 8,  "reorder_level": 2},
    "Veg Soup":      {"stock": 15, "reorder_level": 5},
    "Butter Chicken":{"stock": 12, "reorder_level": 4},
    "Dal Tadka":     {"stock": 20, "reorder_level": 5},
    "Veg Biryani":   {"stock": 6,  "reorder_level": 3},
    "Garlic Naan":   {"stock": 30, "reorder_level": 10},
    "Gulab Jamun":   {"stock": 5,  "reorder_level": 2},
    "Rasgulla":      {"stock": 4,  "reorder_level": 3},
    "Ice Cream":     {"stock": 7,  "reorder_level": 3},
}

sales_log = {
    "2025-01-01": [
        {"order_id": 1,  "items": ["Paneer Tikka", "Garlic Naan"],              "total": 220.0},
        {"order_id": 2,  "items": ["Gulab Jamun", "Veg Soup"],                  "total": 210.0},
        {"order_id": 3,  "items": ["Butter Chicken", "Garlic Naan"],            "total": 360.0},
    ],
    "2025-01-02": [
        {"order_id": 4,  "items": ["Dal Tadka", "Garlic Naan"],                 "total": 220.0},
        {"order_id": 5,  "items": ["Veg Biryani", "Gulab Jamun"],               "total": 340.0},
    ],
    "2025-01-03": [
        {"order_id": 6,  "items": ["Paneer Tikka", "Rasgulla"],                 "total": 260.0},
        {"order_id": 7,  "items": ["Butter Chicken", "Veg Biryani"],            "total": 570.0},
        {"order_id": 8,  "items": ["Garlic Naan", "Gulab Jamun"],               "total": 130.0},
    ],
    "2025-01-04": [
        {"order_id": 9,  "items": ["Dal Tadka", "Garlic Naan", "Rasgulla"],     "total": 300.0},
        {"order_id": 10, "items": ["Paneer Tikka", "Gulab Jamun"],              "total": 270.0},
    ],
}


# ─────────────────────────────────────────────────────────────────────
# TASK 1  -  Explore the Menu
# ─────────────────────────────────────────────────────────────────────

print("=" * 58)
print("TASK 1 - Explore the Menu")
print("=" * 58)

# first collect unique categories in the order they appear
categories = []
for info in menu.values():
    if info["category"] not in categories:
        categories.append(info["category"])

# now loop through each category and print items under it
for cat in categories:
    print(f"\n  [{cat}]")
    for item_name, item_info in menu.items():
        if item_info["category"] == cat:
            status = "Available" if item_info["available"] else "Unavailable"
            print(f"    {item_name:<18}  Rs.{item_info['price']:>7.2f}  [{status}]")

# some quick stats using dictionary methods
total_items     = len(menu)
available_count = sum(1 for v in menu.values() if v["available"])
most_exp        = max(menu.items(), key=lambda x: x[1]["price"])
cheap_items     = [(n, i["price"]) for n, i in menu.items() if i["price"] < 150]

print(f"\n  Total items on menu     : {total_items}")
print(f"  Items currently available : {available_count}")
print(f"  Most expensive item     : {most_exp[0]} (Rs.{most_exp[1]['price']:.2f})")
print(f"  Items under Rs.150      : {cheap_items}")


# ─────────────────────────────────────────────────────────────────────
# TASK 2  -  Cart Operations
# ─────────────────────────────────────────────────────────────────────

print("\n" + "=" * 58)
print("TASK 2 - Cart Operations")
print("=" * 58)

cart = []  # cart is a list of dicts, each dict is one line item


def add_to_cart(cart, item_name, qty=1):
    # first check if the item even exists in our menu
    if item_name not in menu:
        print(f"  '{item_name}' is not on the menu.")
        return
    # then check if its available right now
    if not menu[item_name]["available"]:
        print(f"  Sorry, '{item_name}' is not available at the moment.")
        return
    # if its already in cart just update the quantity instead of duplicating
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] += qty
            print(f"  '{item_name}' already in cart - quantity updated to {entry['quantity']}.")
            return
    # otherwise add it fresh
    cart.append({"item": item_name, "quantity": qty, "price": menu[item_name]["price"]})
    print(f"  Added '{item_name}' x{qty}.")


def remove_from_cart(cart, item_name):
    for i, entry in enumerate(cart):
        if entry["item"] == item_name:
            cart.pop(i)
            print(f"  Removed '{item_name}' from cart.")
            return
    print(f"  '{item_name}' wasnt found in the cart.")


def update_quantity(cart, item_name, new_qty):
    for entry in cart:
        if entry["item"] == item_name:
            entry["quantity"] = new_qty
            print(f"  Quantity for '{item_name}' changed to {new_qty}.")
            return
    print(f"  '{item_name}' is not in the cart.")


def print_cart(cart):
    if not cart:
        print("  [cart is empty]")
        return
    print(f"\n  {'Item':<18}  {'Qty':>4}  {'Price':>10}  {'Subtotal':>10}")
    print("  " + "-" * 48)
    for e in cart:
        sub = e["quantity"] * e["price"]
        print(f"  {e['item']:<18}  {e['quantity']:>4}  Rs.{e['price']:>7.2f}  Rs.{sub:>7.2f}")


# simulate the sequence from the assignment
print("\n-- Add Paneer Tikka x2 --")
add_to_cart(cart, "Paneer Tikka", 2)
print_cart(cart)

print("\n-- Add Gulab Jamun x1 --")
add_to_cart(cart, "Gulab Jamun", 1)
print_cart(cart)

print("\n-- Add Paneer Tikka x1 again (qty should go to 3, not a new row) --")
add_to_cart(cart, "Paneer Tikka", 1)
print_cart(cart)

print("\n-- Try Mystery Burger (doesnt exist) --")
add_to_cart(cart, "Mystery Burger")
print_cart(cart)

print("\n-- Try Chicken Wings (item exists but marked unavailable) --")
add_to_cart(cart, "Chicken Wings")
print_cart(cart)

print("\n-- Remove Gulab Jamun --")
remove_from_cart(cart, "Gulab Jamun")
print_cart(cart)

# final bill calculation
print("\n-- Final Bill --")
subtotal     = sum(e["quantity"] * e["price"] for e in cart)
tax          = round(subtotal * 0.05, 2)
total_amount = round(subtotal + tax, 2)
for e in cart:
    print(f"  {e['item']:<18}  Rs.{e['quantity'] * e['price']:.2f}")
print(f"\n  Subtotal    : Rs.{subtotal:.2f}")
print(f"  Tax (5%)    : Rs.{tax:.2f}")
print(f"  Total       : Rs.{total_amount:.2f}")


# ─────────────────────────────────────────────────────────────────────
# TASK 3  -  Inventory Tracker with Deep Copy
# ─────────────────────────────────────────────────────────────────────

print("\n" + "=" * 58)
print("TASK 3 - Inventory Tracker with Deep Copy")
print("=" * 58)

# deep copy the inventory before touching anything
# important - shallow copy wont work here because the values are dicts themselves
inventory_backup = copy.deepcopy(inventory)

# quick demo to show the deep copy is truly independent
print("\n  [demo] changing Garlic Naan stock in inventory to 999...")
inventory["Garlic Naan"]["stock"] = 999
print(f"  inventory['Garlic Naan']['stock']        = {inventory['Garlic Naan']['stock']}")
print(f"  inventory_backup['Garlic Naan']['stock'] = {inventory_backup['Garlic Naan']['stock']}  <- backup didnt change!")
inventory["Garlic Naan"]["stock"] = 30  # put it back before we continue
print("  reverted inventory to original values.\n")

# now deduct the final cart quantities from inventory
print("  Deducting cart items from stock...")
for entry in cart:
    item  = entry["item"]
    need  = entry["quantity"]
    have  = inventory[item]["stock"]

    if have >= need:
        inventory[item]["stock"] -= need
        print(f"  Deducted {need} of '{item}'. Stock remaining: {inventory[item]['stock']}")
    else:
        # not enough stock - deduct whatever we have, dont go negative
        print(f"  Warning - only {have} unit(s) of '{item}' in stock (needed {need}). Deducting what's available.")
        inventory[item]["stock"] = 0

# check for items that need reordering
print("\n  -- Reorder Alerts --")
any_alerts = False
for name, info in inventory.items():
    if info["stock"] <= info["reorder_level"]:
        print(f"  Reorder Alert: {name} - only {info['stock']} unit(s) left (reorder level: {info['reorder_level']})")
        any_alerts = True
if not any_alerts:
    print("  All stock levels are fine, no reorders needed.")

# side by side comparison of current vs backup to confirm deep copy worked
print("\n  -- Inventory vs Backup Comparison --")
print(f"  {'Item':<18}  {'Current':>8}  {'Backup':>8}")
print("  " + "-" * 38)
for name in inventory:
    cur = inventory[name]["stock"]
    bak = inventory_backup[name]["stock"]
    note = "  <- changed" if cur != bak else ""
    print(f"  {name:<18}  {cur:>8}  {bak:>8}{note}")


# ─────────────────────────────────────────────────────────────────────
# TASK 4  -  Daily Sales Log Analysis
# ─────────────────────────────────────────────────────────────────────

print("\n" + "=" * 58)
print("TASK 4 - Daily Sales Log Analysis")
print("=" * 58)


def print_revenue_table(log):
    """prints revenue per day and returns whichever day had the highest total"""
    print(f"\n  {'Date':<14}  {'Orders':>6}  {'Revenue':>10}")
    print("  " + "-" * 36)
    best_day = None
    best_rev = 0
    for date, orders in sorted(log.items()):
        daily = sum(o["total"] for o in orders)
        print(f"  {date:<14}  {len(orders):>6}  Rs.{daily:>8.2f}")
        if daily > best_rev:
            best_rev = daily
            best_day = date
    return best_day, best_rev


# 1 & 2 - print revenue per day and find the best day
best_day, best_rev = print_revenue_table(sales_log)
print(f"\n  Best selling day : {best_day} (Rs.{best_rev:.2f})")

# 3 - find item that appeared in the most individual orders
item_count = {}
for orders in sales_log.values():
    for order in orders:
        for item in order["items"]:
            item_count[item] = item_count.get(item, 0) + 1

top_item = max(item_count, key=item_count.get)
print(f"  Most ordered item: {top_item} (appeared in {item_count[top_item]} orders)")

# 4 - add jan 5 and rerun the table to show it updates correctly
new_day = {
    "2025-01-05": [
        {"order_id": 11, "items": ["Butter Chicken", "Gulab Jamun", "Garlic Naan"], "total": 490.0},
        {"order_id": 12, "items": ["Paneer Tikka", "Rasgulla"],                      "total": 260.0},
    ]
}
sales_log.update(new_day)

print("\n  [after adding 2025-01-05]")
best_day2, best_rev2 = print_revenue_table(sales_log)
print(f"\n  Best selling day : {best_day2} (Rs.{best_rev2:.2f})")

# 5 - enumerate through all orders across all dates
print("\n  -- All Orders (numbered with enumerate) --")
all_orders = []
for date, orders in sorted(sales_log.items()):
    for order in orders:
        all_orders.append((date, order))

for idx, (date, order) in enumerate(all_orders, start=1):
    items_str = ", ".join(order["items"])
    print(f"  {idx:>2}. [{date}] Order #{order['order_id']} - Rs.{order['total']:.2f} - Items: {items_str}")

print("\n" + "=" * 58)
print("Part 2 done.")
print("=" * 58)
