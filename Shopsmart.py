import json
import os
from datetime import datetime

# --- Configuration and Data Storage ---

# The name of the file where purchase data will be stored persistently.
DATA_FILE = 'purchases.json'

# Global list to hold all purchase items in memory during the session.
purchases = []

# --- Helper Functions ---

def validate_float_input(prompt, default_value=None):
    """Prompts for a float input and handles ValueError for robustness."""
    while True:
        value_input = input(prompt).strip()
        
        # If the input is empty and a default is provided (used for update)
        if not value_input and default_value is not None:
            return default_value
        # If the input is empty and no default (used for add)
        elif not value_input and default_value is None:
            print("[WARNING] Value cannot be empty.")
            continue
            
        try:
            # Ensure we treat '0' correctly as a float
            return float(value_input)
        except ValueError:
            print("[ERROR] Invalid input. Please enter a numerical value (e.g., 19.99).")

def display_purchases(items_list):
    """A helper function to display a list of purchase items clearly."""
    if not items_list:
        print("No purchases found matching your criteria.")
        return

    # Column formatting for clear display
    print("-" * 70)
    print(f"{'ID':<4} | {'Item Name':<25} | {'Category':<15} | {'Cost':>10} | {'Date':<10}")
    print("-" * 70)

    for item in items_list:
        # Format cost to two decimal places for currency
        cost_formatted = f"${item['cost']:.2f}"
        
        # Display the purchase details
        print(f"{item['id']:<4} | {item['item_name'][:25]:<25} | {item['category'][:15]:<15} | {cost_formatted:>10} | {item['purchase_date'][:10]:<10}")

    print("-" * 70)
    print(f"Displayed Purchases: {len(items_list)}")

# --- File Handling Functions (Persistent Storage) ---

def load_data():
    """Loads purchase items from the JSON file into the global list."""
    global purchases
    try:
        if os.path.exists(DATA_FILE) and os.path.getsize(DATA_FILE) > 0:
            with open(DATA_FILE, 'r') as f:
                purchases = json.load(f)
            print(f"\n[INFO] Loaded {len(purchases)} purchase records from {DATA_FILE}.")
        else:
            purchases = []
            print(f"\n[INFO] {DATA_FILE} not found or empty. Starting with an empty list.")
    except json.JSONDecodeError:
        print("\n[ERROR] Data file is corrupted (JSON Error). Starting with an empty list.")
        purchases = []
    except Exception as e:
        print(f"\n[ERROR] An unexpected error occurred while loading data: {e}")
        purchases = []

def save_data():
    """Saves the current purchase items from the global list to the JSON file."""
    try:
        with open(DATA_FILE, 'w') as f:
            json.dump(purchases, f, indent=4)
        print(f"\n[INFO] Successfully saved {len(purchases)} records to {DATA_FILE}.")
    except Exception as e:
        print(f"\n[ERROR] Could not save data: {e}")

# --- Core Operations (CRUD) ---

def add_purchase():
    """Prompts user for a new purchase item and adds it to the list."""
    print("\n--- Add New Purchase Record ---")
    
    item_name = input("Item Name: ").strip()
    category = input("Category (e.g., Groceries, Electronics, Clothes): ").strip()
    
    # Use helper function to validate cost input
    cost = validate_float_input("Cost ($): ")
    
    if not item_name or not category:
        print("[WARNING] Item Name and Category cannot be empty. Record not added.")
        return

    # Assign a new unique ID, ensuring it is sequential even after deletions
    new_id = (purchases[-1]['id'] + 1) if purchases else 1
    
    new_purchase = {
        "id": new_id,
        "item_name": item_name,
        "category": category if category else "General",
        "cost": cost,
        "purchase_date": datetime.now().strftime("%Y-%m-%d")
    }

    purchases.append(new_purchase)
    save_data()
    print(f"\n[SUCCESS] Purchase '{item_name}' added successfully with ID: {new_id}.")

def view_all_purchases():
    """Displays all stored purchase records."""
    print("\n--- All Purchase Records ---")
    if not purchases:
        print("Your purchase list is currently empty. Add some records!")
        return
    display_purchases(purchases)

def update_purchase():
    """Prompts user for a purchase ID and allows modification of its details."""
    print("\n--- Update Purchase Record ---")
    
    if not purchases:
        print("[WARNING] The purchase list is empty. Nothing to update.")
        return

    # Display items to help the user choose the ID
    view_all_purchases() 
    
    id_to_update_input = input("Enter the ID of the record to update (or press Enter to cancel): ").strip()

    if not id_to_update_input:
        print("[INFO] Update cancelled.")
        return
    
    try:
        id_to_update = int(id_to_update_input)
    except ValueError:
        print("[ERROR] Invalid input. Please enter a valid number ID.")
        return

    # Find the item
    record_to_update = next((p for p in purchases if p['id'] == id_to_update), None)

    if not record_to_update:
        print(f"[WARNING] Record with ID {id_to_update} not found.")
        return

    print(f"\nEditing record: '{record_to_update['item_name']}' (ID: {id_to_update})")
    print("--------------------------------------------------")
    print("💡 Tip: Leave a field blank to keep its current value.")
    
    # 1. Item Name
    new_name = input(f"New Item Name (Current: '{record_to_update['item_name']}'): ").strip()
    if new_name:
        record_to_update['item_name'] = new_name
    
    # 2. Category
    new_category = input(f"New Category (Current: '{record_to_update['category']}'): ").strip()
    if new_category:
        record_to_update['category'] = new_category
        
    # 3. Cost (Use helper function with current cost as default)
    print(f"Current Cost: ${record_to_update['cost']:.2f}")
    new_cost = validate_float_input("New Cost ($) (Press Enter to keep current): ", default_value=record_to_update['cost'])
    
    if new_cost != record_to_update['cost']:
        record_to_update['cost'] = new_cost
        record_to_update['purchase_date'] = datetime.now().strftime("%Y-%m-%d") # Update date on modification

    save_data()
    print(f"\n[SUCCESS] Record ID {id_to_update} updated successfully.")


def search_filter_purchases():
    """Allows users to search by item name/category."""
    print("\n--- Search & Filter Purchases ---")
    
    if not purchases:
        print("[WARNING] The purchase list is empty. Nothing to search.")
        return
    
    search_term = input("Enter keyword to search (Item Name or Category): ").strip().lower()
    
    if not search_term:
        print("[INFO] Search cancelled.")
        return

    results = []

    for item in purchases:
        # Check if keyword is in item_name or category (case-insensitive)
        if (search_term in item['item_name'].lower() or
            search_term in item['category'].lower()):
            results.append(item)
    
    print(f"\n--- Search Results for '{search_term}' ---")
    display_purchases(results)


def summarize_report():
    """Generates summary reports (Total spent and average cost per category)."""
    print("\n--- Category Spending Summary Report ---")
    
    if not purchases:
        print("[WARNING] The purchase list is empty. No data to report.")
        return

    # Dictionary to store totals and counts for each category
    # Structure: {'CategoryName': {'total': 0.0, 'count': 0}}
    category_summary = {}
    grand_total = 0.0

    # 1. Aggregate Data
    for item in purchases:
        category = item['category'].strip()
        cost = item['cost']
        
        # Initialize category if it's the first time seeing it
        if category not in category_summary:
            category_summary[category] = {'total': 0.0, 'count': 0}
            
        category_summary[category]['total'] += cost
        category_summary[category]['count'] += 1
        grand_total += cost
        
    # 2. Display Report
    
    print("-" * 55)
    print(f"{'Category':<20} | {'Total Spent':>15} | {'Avg. Item Cost':>15}")
    print("-" * 55)

    for category, data in category_summary.items():
        total = data['total']
        count = data['count']
        average = total / count
        
        # Display formatted output
        print(f"{category:<20} | ${total:>14.2f} | ${average:>14.2f}")
    
    print("-" * 55)
    print(f"{'GRAND TOTAL':<20} | ${grand_total:>14.2f} |")
    print("-" * 55)


def delete_purchase():
    """Prompts user for a purchase ID and deletes the corresponding record."""
    print("\n--- Delete Purchase Record ---")
    global purchases

    if not purchases:
        print("[WARNING] The purchase list is empty. Nothing to delete.")
        return

    view_all_purchases()
    
    id_to_delete_input = input("Enter the ID of the record to delete (or press Enter to cancel): ").strip()

    if not id_to_delete_input:
        print("[INFO] Deletion cancelled.")
        return
    
    try:
        id_to_delete = int(id_to_delete_input)
    except ValueError:
        print("[ERROR] Invalid input. Please enter a valid number ID.")
        return

    initial_length = len(purchases)
    
    # Filter out the item with the matching ID
    purchases = [p for p in purchases if p['id'] != id_to_delete]

    if len(purchases) < initial_length:
        print(f"[SUCCESS] Record with ID {id_to_delete} has been deleted.")
        
        # Re-index remaining items to ensure IDs are contiguous
        for index, item in enumerate(purchases):
            item['id'] = index + 1
        
        save_data()
    else:
        print(f"[WARNING] Record with ID {id_to_delete} not found.")

# --- Menu Controller and Main Loop ---

def display_menu():
    """Prints the main menu options to the console."""
    print("\n" + "="*45)
    print("    ShopSmart - Smart Purchase Optimizer")
    print("="*45)
    print("1. Add New Purchase Record")
    print("2. View All Records")
    print("3. Search/Filter Records (by Item Name or Category)")
    print("4. Update Record Details")
    print("5. Delete Record")
    print("6. Generate Summary Report (Totals & Averages)")
    print("0. Exit and Save")
    print("="*45)

def main():
    """Main function that runs the application loop."""
    load_data()

    while True:
        display_menu()
        choice = input("Enter your choice (0-6): ").strip()

        if choice == '1':
            add_purchase()
        elif choice == '2':
            view_all_purchases()
        elif choice == '3':
            search_filter_purchases()
        elif choice == '4':
            update_purchase()
        elif choice == '5':
            delete_purchase() 
        elif choice == '6':
            summarize_report()
        elif choice == '0':
            print("\nExiting ShopSmart. Goodbye!")
            save_data()
            input("Press Enter to close the program...")
            break
        else:
            print("\n[WARNING] Invalid choice. Please enter a number between 0 and 6.")

if __name__ == "__main__":
    main()